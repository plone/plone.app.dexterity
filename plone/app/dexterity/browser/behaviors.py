from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import Interface, implements
from zope.component import adapts
from zope import schema
from z3c.form import field, form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone.z3cform.layout import FormWrapper
from plone.app.dexterity.interfaces import ITypeSchemaContext

class IBehaviorConfiguration(Interface):
    
    behaviors = schema.Set(
        title = u'Behaviors',
        value_type = schema.Choice(
                vocabulary = 'Behaviors'
            )
        )

class BehaviorConfigurationAdapter(object):
    implements(IBehaviorConfiguration)
    adapts(ITypeSchemaContext)
    
    def __init__(self, context):
        self.context = context
        self.fti = self.context.fti

    def get_behaviors(self):
        return self.fti.behaviors

    def set_behaviors(self, value):
        self.fti.behaviors = list(value)

    behaviors = property(get_behaviors, set_behaviors)

class BehaviorsForm(form.EditForm):
    
    label = u'Behaviors'
    fields = field.Fields(IBehaviorConfiguration)
    fields['behaviors'].widgetFactory = CheckBoxFieldWidget

class BehaviorsFormPage(FormWrapper):
    form = BehaviorsForm
    index = ViewPageTemplateFile('tabbed_forms.pt')
    tabs = (
        ('Schema', '@@edit'),
        ('Behaviors', None),
        )
    
    @property
    def label(self):
        return u'Edit %s' % self.context.__name__
