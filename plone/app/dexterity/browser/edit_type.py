from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.schemaeditor.browser.schema.listing import SchemaListing, ReadOnlySchemaListing
from plone.schemaeditor.browser.schema.listing import SchemaListingPage
from plone.app.dexterity import MessageFactory as _

class TypeEditPage(SchemaListingPage):
    """ Form wrapper so we can get a form with layout.

        We define an explicit subclass rather than using the wrap_form method
        from plone.z3cform.layout so that we can inject the type name into
        the form label.
    """
    index = ViewPageTemplateFile('tabbed_forms.pt')

    @property
    def tabs(self):
        return (
            (_('Fields'), None),
            (_('Behaviors'), '@@behaviors'),
            )

    @property
    def form(self):
        if self.context.fti.hasDynamicSchema:
            return SchemaListing
        else:
            return ReadOnlySchemaListing
