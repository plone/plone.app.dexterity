from copy import deepcopy
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import adapts, getUtilitiesFor
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.lifecycleevent import modified

from z3c.form import field, form
from z3c.form.browser.checkbox import SingleCheckBoxFieldWidget

from plone.behavior.interfaces import IBehavior
from plone.app.dexterity.interfaces import ITypeSchemaContext
from plone.app.dexterity.browser.layout import TypeFormLayout
from plone.app.dexterity import MessageFactory as _

from plone.dexterity.fti import DexterityFTIModificationDescription

PMF = MessageFactory('plone')


def behaviorConfigurationModified(object, event):
    description = DexterityFTIModificationDescription("behaviors", "")
    modified(object.fti, description)


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


class TypeBehaviorsForm(form.EditForm):

    template = ViewPageTemplateFile('behaviors.pt')
    label = _(u'Behaviors')
    description = _(u'Select the behaviors to enable for this content type.')
    successMessage = _(u'Behaviors successfully updated.')
    noChangesMessage = _(u'No changes were made.')
    buttons = deepcopy(form.EditForm.buttons)
    buttons['apply'].title = PMF(u'Save')

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
                __name__=str(name),
                title=reg.title,
                description=reg.description,
                required=False
            )
            fields.append(f)
        fields = sorted(fields, key=lambda x: x.title)
        fields = field.Fields(*fields)

        for f in fields.values():
            f.widgetFactory = SingleCheckBoxFieldWidget
        return fields


class TypeBehaviorsPage(TypeFormLayout):
    form = TypeBehaviorsForm
    label = _(u'Behaviors')
