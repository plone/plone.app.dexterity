from copy import deepcopy
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile as Zope2PageTemplateFile
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import adapts, getUtilitiesFor
from zope import schema
from zope.i18nmessageid import MessageFactory

from z3c.form import field, form
from z3c.form.browser.checkbox import SingleCheckBoxFieldWidget

from plone.z3cform.layout import FormWrapper
from plone.behavior.interfaces import IBehavior
from plone.app.dexterity.interfaces import ITypeSchemaContext
from plone.app.dexterity import MessageFactory as _


PMF = MessageFactory('plone')

class BehaviorConfigurationAdapter(object):
    adapts(ITypeSchemaContext)

    def __init__(self, context):
        self.__dict__['context'] = context
        self.__dict__['fti'] = self.context.fti

    def __getattr__(self, name):
        # return True if the behavior is present
        # (sanity check: don't try unless the name has a period in it)
        if '.' in name:
            return name in self.fti.behaviors
        else:
            raise AttributeError

    def __setattr__(self, name, value):
        # add or remove the behavior based on the value from the form
        behaviors = list(self.fti.behaviors)
        if value and name not in behaviors:
            behaviors.append(name)
        elif not value and name in behaviors:
            behaviors.remove(name)
        self.fti.behaviors = behaviors

    def __iter__(self):
        # iterate through the present behaviors
        for b in self.fti.behaviors:
            yield b

class BehaviorsForm(form.EditForm):

    template = ViewPageTemplateFile('behaviors.pt')
    label = _(u'Behaviors')
    description = _(u'Select the behaviors to enable for this content type.')
    successMessage = _(u'Behaviors successfully updated.')
    noChangesMessage = _(u'No changes were made.')
    buttons = deepcopy(form.EditForm.buttons)

    def getContent(self):
        return BehaviorConfigurationAdapter(self.context)

    @property
    def fields(self):
        fields = []
        for name, reg in getUtilitiesFor(IBehavior):
            if name == 'plone.app.dexterity.behaviors.related.IRelatedItems':
                # skip deprecated behavior
                continue

            f = schema.Bool(
                __name__ = str(name),
                title = reg.title,
                description = reg.description,
                required = False
                )
            fields.append(f)
        fields = sorted(fields, key=lambda x:x.title)
        fields = field.Fields(*fields)

        for f in fields.values():
            f.widgetFactory = SingleCheckBoxFieldWidget
        return fields

    def update(self):
        self.buttons['apply'].title = PMF(u'Save')
        form.EditForm.update(self)

class BehaviorsFormPage(FormWrapper):
    form = BehaviorsForm
    index = Zope2PageTemplateFile('tabbed_forms.pt')
    tabs = (
        (_('Fields'), '@@edit'),
        (_('Behaviors'), None),
        )

    @property
    def label(self):
        return _('label_behaviors_for',
                 default=u"Behaviors for ${title} (${name})",
                 mapping={'title': self.context.Title(),
                          'name': self.context.__name__})
