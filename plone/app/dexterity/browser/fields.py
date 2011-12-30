from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from plone.schemaeditor.browser.schema.listing import SchemaListing
from plone.schemaeditor.browser.schema.listing import ReadOnlySchemaListing
from plone.schemaeditor.browser.schema.listing import SchemaListingPage

from plone.app.dexterity import MessageFactory as _


class TypeFieldsPage(SchemaListingPage):
    
    index = ViewPageTemplateFile('tabbed_forms.pt')
    label = _(u'Fields')

    @property
    def tabs(self):
        return (
            (_('Overview'), '@@overview'),
            (_('Fields'), None),
            (_('Behaviors'), '@@behaviors'),
            )
    
    @property
    def form(self):
        if self.context.fti.hasDynamicSchema:
            return SchemaListing
        else:
            return ReadOnlySchemaListing
