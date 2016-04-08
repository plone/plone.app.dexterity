# -*- coding: utf-8 -*-
from collections import Counter
from operator import attrgetter
from copy import deepcopy
from plone.app.dexterity import _
from plone.app.dexterity.browser.layout import TypeFormLayout
from plone.app.dexterity.interfaces import ITypeSchemaContext
from plone.behavior.interfaces import IBehavior
from plone.behavior.registration import lookup_behavior_registration
from plone.behavior.registration import BehaviorRegistrationNotFound
from plone.dexterity.fti import DexterityFTIModificationDescription
from z3c.form import field
from z3c.form import form
from z3c.form.browser.checkbox import SingleCheckBoxFieldWidget
from zope import schema
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.component import adapter
from zope.component import getUtilitiesFor
from zope.lifecycleevent import modified

TTW_BEHAVIOR_BLACKLIST = [
    # skip deprecated behavior
    'plone.app.dexterity.behaviors.related.IRelatedItems',
]


def behaviorConfigurationModified(object, event):
    description = DexterityFTIModificationDescription("behaviors", "")
    modified(object.fti, description)


@adapter(ITypeSchemaContext)
class BehaviorConfigurationAdapter(object):

    def __init__(self, context):
        self.__dict__['context'] = context
        self.__dict__['fti'] = self.context.fti

    def __getattr__(self, name):
        # be sure to get a valid value
        reg = lookup_behavior_registration(name=name)
        iid = reg.interface.__identifier__
        return (
            iid in self.fti.behaviors or
            reg.name.encode('utf8') in self.fti.behaviors
        )

    def __setattr__(self, name, value):
        # add or remove the behavior based on the value from the form
        behaviors = list(self.fti.behaviors)
        reg = lookup_behavior_registration(name=name)
        iid = reg.interface.__identifier__
        if reg.name and iid in self.fti.behaviors:
            behaviors.remove(iid)
            bname = reg.name.encode('utf8')
        else:
            bname = iid
        if value and bname not in behaviors:
            behaviors.append(bname)
        elif not value and bname in behaviors:
            behaviors.remove(bname)
        self.fti.behaviors = behaviors

    def __iter__(self):
        # iterate through the present behaviors
        for name in self.fti.behaviors:
            try:
                reg = lookup_behavior_registration(name=name)
            except BehaviorRegistrationNotFound:
                # ignore wrong names
                continue
            if reg.name:
                yield reg.name.encode('utf8')
            else:
                yield name


class TypeBehaviorsForm(form.EditForm):

    template = ViewPageTemplateFile('behaviors.pt')
    label = _(u'Behaviors')
    description = _(u'Select the behaviors to enable for this content type.')
    successMessage = _(u'Behaviors successfully updated.')
    noChangesMessage = _(u'No changes were made.')
    buttons = deepcopy(form.EditForm.buttons)
    buttons['apply'].title = _(u'Save')

    def getContent(self):
        return BehaviorConfigurationAdapter(self.context)

    @property
    def fields(self):
        counts = Counter(
            [reg.interface for name, reg in getUtilitiesFor(IBehavior)]
        )
        fields = []
        for name, reg in getUtilitiesFor(IBehavior):
            if name in TTW_BEHAVIOR_BLACKLIST:
                # skip blacklisted
                continue
            with_name = counts[reg.interface] == 2
            if with_name and reg.name != name:
                continue
            fname = reg.name if reg.name else name
            if isinstance(fname, unicode):
                fname = fname.encode('utf8')
            fields.append(
                schema.Bool(
                    __name__=fname,
                    title=reg.title,
                    description=reg.description,
                    required=False
                )
            )
        form_fields = field.Fields(*sorted(fields, key=attrgetter('title')))
        for ff in form_fields.values():
            ff.widgetFactory = SingleCheckBoxFieldWidget
        return form_fields


class TypeBehaviorsPage(TypeFormLayout):
    form = TypeBehaviorsForm
    label = _(u'Behaviors')
