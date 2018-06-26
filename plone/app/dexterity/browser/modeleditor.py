# -*- coding: utf-8 -*-
from AccessControl import Unauthorized
from lxml import etree
from plone.app.dexterity import _
from plone.supermodel.parser import SupermodelParseError
from Products.CMFPlone.utils import safe_unicode
from Products.Five import BrowserView
from zope.component import queryMultiAdapter

import json
import plone.supermodel


NAMESPACE = '{http://namespaces.plone.org/supermodel/schema}'


class ModelEditorView(BrowserView):
    """Editor view.
    """

    def modelSource(self):
        return self.context.fti.model_source


def authorized(context, request):
    authenticator = queryMultiAdapter((context, request),
                                      name=u'authenticator')
    return authenticator and authenticator.verify()


class AjaxSaveHandler(BrowserView):
    """Handle AJAX save posts.
    """

    def __call__(self):
        """Handle AJAX save post.
        """

        if not authorized(self.context, self.request):
            raise Unauthorized

        source = self.request.form.get('source')
        if source:
            # Is it valid XML?
            try:
                root = etree.fromstring(source)
            except etree.XMLSyntaxError as e:
                return json.dumps({
                    'success': False,
                    'message': 'XMLSyntaxError: {0}'.format(
                        safe_unicode(e.args[0])
                    )
                })

            # a little more sanity checking, look at first two element levels
            if root.tag != NAMESPACE + 'model':
                return json.dumps({
                    'success': False,
                    'message': _(u"Error: root tag must be 'model'")
                })
            for element in root.getchildren():
                if element.tag != NAMESPACE + 'schema':
                    return json.dumps({
                        'success': False,
                        'message': _(
                            u"Error: all model elements must be 'schema'"
                        )
                    })

            # can supermodel parse it?
            # This is mainly good for catching bad dotted names.
            try:
                plone.supermodel.loadString(source, policy=u'dexterity')
            except SupermodelParseError as e:
                message = e.args[0].replace('\n  File "<unknown>"', '')
                return json.dumps({
                    'success': False,
                    'message': u'SuperModelParseError: {0}'.format(message)
                })

            # clean up formatting sins
            source = etree.tostring(
                root,
                pretty_print=True,
                xml_declaration=True,
                encoding='utf8'
            )
            # and save to FTI
            fti = self.context.fti
            fti.manage_changeProperties(model_source=source)

            self.request.response.setHeader('Content-Type', 'application/json')
            return json.dumps({'success': True, 'message': _(u'Saved')})
