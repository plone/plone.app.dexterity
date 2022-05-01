from AccessControl import Unauthorized
from lxml import etree
from plone.app.dexterity import _
from plone.base.utils import safe_bytes
from plone.base.utils import safe_text
from plone.supermodel import loadString
from plone.supermodel import serializeModel
from plone.supermodel.parser import SupermodelParseError
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import queryMultiAdapter

import html


NAMESPACE = "{http://namespaces.plone.org/supermodel/schema}"


class ModelEditorView(BrowserView):
    """Editor view."""

    @property
    def escaped_model_source(self):
        # Return the HTML escaped model source.
        return html.escape(self.model_source, False)

    @property
    def model_source(self):
        # Return modified source from textarea or the original FTI source.
        source = self.request.form.get("source") or self.context.fti.model_source
        if source:
            return source

        # or serialize the model file
        model = self.context.fti.lookupModel()
        return serializeModel(model)

    def authorized(self, context, request):
        authenticator = queryMultiAdapter((context, request), name="authenticator")
        return authenticator and authenticator.verify()

    def __call__(self):
        """View and eventually save the form."""

        save = "form.button.save" in self.request.form
        source = self.request.form.get("source")
        if save and source:

            # First, check for authenticator
            if not self.authorized(self.context, self.request):
                raise Unauthorized

            # Is it valid XML?
            # Some safety measures.
            # We do not want to load entities, especially file:/// entities.
            # Also discard processing instructions.
            #
            source = safe_bytes(source)
            parser = etree.XMLParser(resolve_entities=False, remove_pis=True)
            try:
                root = etree.fromstring(source, parser=parser)
            except etree.XMLSyntaxError as e:
                IStatusMessage(self.request).addStatusMessage(
                    f"XMLSyntaxError: {html.escape(safe_text(e.args[0]))}",
                    "error",
                )
                return super().__call__()

            # a little more sanity checking, look at first two element levels
            if root.tag != NAMESPACE + "model":
                IStatusMessage(self.request).addStatusMessage(
                    _("Error: root tag must be 'model'"),
                    "error",
                )
                return super().__call__()

            for element in root.getchildren():
                if element.tag != NAMESPACE + "schema":
                    IStatusMessage(self.request).addStatusMessage(
                        _("Error: all model elements must be 'schema'"),
                        "error",
                    )
                    return super().__call__()

            # can supermodel parse it?
            # This is mainly good for catching bad dotted names.
            try:
                loadString(source, policy="dexterity")
            except SupermodelParseError as e:
                message = e.args[0].replace('\n  File "<unknown>"', "")
                IStatusMessage(self.request).addStatusMessage(
                    f"SuperModelParseError: {html.escape(message)}",
                    "error",
                )
                return super().__call__()

            # clean up formatting sins
            source = etree.tostring(
                root, pretty_print=True, xml_declaration=True, encoding="utf8"
            )

            # Save to FTI and also allow to clear the source
            fti = self.context.fti
            fti.manage_changeProperties(model_source=source)

            IStatusMessage(self.request).addStatusMessage(
                _("Changes saved."),
                "info",
            )

        return super().__call__()
