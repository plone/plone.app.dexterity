"""
DefaultDexterityTextIndexFieldConverter    the default field converter
NamedfileFieldConverter                    an optional namedfile field
converter only enabled when plone.namedfile is installed
"""

from plone.app.dexterity.textindexer import interfaces
from plone.app.textfield.interfaces import IRichText
from plone.base.utils import safe_text
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile.interfaces import INamedFileField
from Products.CMFCore.utils import getToolByName
from z3c.form.interfaces import IWidget
from ZODB.POSException import ConflictError
from zope.component import adapter
from zope.interface import implementer
from zope.schema.interfaces import IField
from zope.schema.interfaces import IInt
from zope.schema.interfaces import ITuple

import logging


LOGGER = logging.getLogger("plone.app.dexterity.textindexer")


@implementer(interfaces.IDexterityTextIndexFieldConverter)
@adapter(IDexterityContent, IField, IWidget)
class DefaultDexterityTextIndexFieldConverter:
    """Fallback field converter which uses the rendered widget in display
    mode for generating a indexable string.
    """

    def __init__(self, context, field, widget):
        """Initialize field converter"""
        self.context = context
        self.field = field
        self.widget = widget

    def convert(self):
        """Convert the adapted field value to text/plain for indexing"""
        html = self.widget.render().strip()
        transforms = getToolByName(self.context, "portal_transforms")
        stream = transforms.convertTo("text/plain", html, mimetype="text/html")
        return stream.getData().strip()


@implementer(interfaces.IDexterityTextIndexFieldConverter)
@adapter(IDexterityContent, IRichText, IWidget)
class DexterityRichTextIndexFieldConverter:
    """Fallback field converter which uses the rendered widget in display
    mode for generating a indexable string.
    """

    def __init__(self, context, field, widget):
        """Initialize field converter"""
        self.context = context
        self.field = field

    def convert(self):
        """Convert a rich text field value to text/plain for indexing"""
        textvalue = self.field.get(self.context)
        if textvalue is None:
            return ""
        html = safe_text(textvalue.output)
        transforms = getToolByName(self.context, "portal_transforms")
        stream = transforms.convertTo("text/plain", html, mimetype=textvalue.mimeType)
        return stream.getData().strip()


@implementer(interfaces.IDexterityTextIndexFieldConverter)
@adapter(IDexterityContent, INamedFileField, IWidget)
class NamedfileFieldConverter(DefaultDexterityTextIndexFieldConverter):
    """Converts the file data of a named file using portal_transforms."""

    def convert(self):
        """Transforms file data to text for indexing safely."""
        storage = self.field.interface(self.context)
        data = self.field.get(storage)

        # if there is no data, do nothing
        if not data or data.getSize() == 0:
            return ""

        # if data is already in text/plain, just return it
        if data.contentType == "text/plain":
            return data.data

        # if there is no path to text/plain, do nothing
        transforms = getToolByName(self.context, "portal_transforms")

        # pylint: disable=W0212
        # W0212: Access to a protected member _findPath of a client class
        if not transforms._findPath(data.contentType, "text/plain"):
            return ""
        # pylint: enable=W0212

        # convert it to text/plain
        try:
            datastream = transforms.convertTo(
                "text/plain",
                data.data,
                mimetype=data.contentType,
                filename=data.filename,
            )
            return datastream.getData()

        except (ConflictError, KeyboardInterrupt):
            raise

        except Exception as e:
            LOGGER.error(
                "Error while trying to convert file contents " 'to "text/plain": %s',
                str(e),
            )


@implementer(interfaces.IDexterityTextIndexFieldConverter)
@adapter(IDexterityContent, IInt, IWidget)
class IntFieldConverter(DefaultDexterityTextIndexFieldConverter):
    """Converts the data of a int field"""

    def convert(self):
        """return the adapted field value"""
        storage = self.field.interface(self.context)
        value = self.field.get(storage)
        return str(value)


@implementer(interfaces.IDexterityTextIndexFieldConverter)
@adapter(IDexterityContent, ITuple, IWidget)
class TupleFieldConverter(DefaultDexterityTextIndexFieldConverter):
    """Converts the data of a tuple field"""

    def convert(self):
        """return the adapted field value"""
        storage = self.field.interface(self.context)
        result = []
        if self.field.get(storage):
            for value in self.field.get(storage):
                result.append(value)
        return " ".join(result)
