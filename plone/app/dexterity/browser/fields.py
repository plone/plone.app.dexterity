from plone.schemaeditor.browser.schema.listing import SchemaListing
from plone.schemaeditor.browser.schema.listing import ReadOnlySchemaListing

from plone.app.dexterity.browser.layout import TypeFormLayout
from plone.app.dexterity import MessageFactory as _


class TypeFieldsPage(TypeFormLayout):
    label = _(u'Fields')

    @property
    def form(self):
        if self.context.fti.hasDynamicSchema:
            return SchemaListing
        else:
            return ReadOnlySchemaListing
