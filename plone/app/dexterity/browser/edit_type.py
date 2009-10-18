from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.schemaeditor.browser.schema.schema import SchemaListing, ReadOnlySchemaListing
from plone.schemaeditor.browser.jsform.jsform import JavascriptFormWrapper

class TypeEditPage(JavascriptFormWrapper):
    """ Form wrapper so we can get a form with layout.
    
        We define an explicit subclass rather than using the wrap_form method
        from plone.z3cform.layout so that we can inject the type name into
        the form label.
    """
    index = ViewPageTemplateFile('tabbed_forms.pt')

    @property
    def tabs(self):
        return (
            ('Schema', None),
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
        return self.context.__name__
