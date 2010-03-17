from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.schemaeditor.browser.schema.listing import SchemaListing, ReadOnlySchemaListing
from plone.z3cform.layout import FormWrapper

class TypeEditPage(FormWrapper):
    """ Form wrapper so we can get a form with layout.
    
        We define an explicit subclass rather than using the wrap_form method
        from plone.z3cform.layout so that we can inject the type name into
        the form label.
    """
    index = ViewPageTemplateFile('tabbed_forms.pt')

    @property
    def tabs(self):
        return (
            ('Fields', None),
            ('Behaviors', '@@behaviors'),
            )
    
    @property
    def form(self):
        if self.context.fti.hasDynamicSchema:
            return SchemaListing
        else:
            return ReadOnlySchemaListing
    
    @property
    def label(self):
        return u'Fields for %s (%s)' % (self.context.Title(), self.context.__name__)
