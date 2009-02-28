from z3c.form.form import Form
from plone.z3cform.layout import FormWrapper
from plone.schemaeditor.browser.schema.schema import SchemaListing
from plone.app.dexterity.browser.behaviors import BehaviorsForm
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

class TypeEditForm(Form):
    template = ViewPageTemplateFile('tabbed_subforms.pt')

    def update(self):
        super(TypeEditForm, self).update()

        schemaform = SchemaListing(self.context, self.request)
        behaviorsform = BehaviorsForm(self.context, self.request)
        schemaform.update()
        behaviorsform.update()
        self.subforms = [schemaform, behaviorsform]
        # hack so we can reuse the template for tabbed fieldsets
        self.groups = self.subforms

class TypeEditPage(FormWrapper):
    """ Form wrapper so we can get a form with layout.
    
        We define an explicit subclass rather than using the wrap_form method
        from plone.z3cform.layout so that we can inject the type name into
        the form label.
    """
    form = TypeEditForm
    
    @property
    def label(self):
        return u'Edit %s' % self.context.__name__
