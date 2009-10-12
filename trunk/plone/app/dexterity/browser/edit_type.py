from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.schemaeditor.browser.schema.schema import SchemaListing
from plone.app.dexterity.browser.behaviors import BehaviorsForm
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
        if self.context.fti.hasDynamicSchema:
            return (
                ('Schema', None),
                ('Behaviors', '@@behaviors'),
                )
        else:
            return (
                ('Behaviors', None),
                )
    
    @property
    def form(self):
        if self.context.fti.hasDynamicSchema:
            return SchemaListing
        else:
            return BehaviorsForm
    
    @property
    def label(self):
        return u'Edit %s' % self.context.__name__
