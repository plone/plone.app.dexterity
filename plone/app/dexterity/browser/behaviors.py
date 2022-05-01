from collections import Counter
from copy import deepcopy
from operator import attrgetter
from plone.app.dexterity import _
from plone.app.dexterity.browser.layout import TypeFormLayout
from plone.app.dexterity.interfaces import ITypeSchemaContext
from plone.base.utils import safe_text
from plone.behavior.interfaces import IBehavior
from plone.behavior.registration import BehaviorRegistrationNotFound
from plone.behavior.registration import lookup_behavior_registration
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
    "plone.app.dexterity.behaviors.related.IRelatedItems",
]


def behaviorConfigurationModified(object, event):
    description = DexterityFTIModificationDescription("behaviors", "")
    modified(object.fti, description)


@adapter(ITypeSchemaContext)
class BehaviorConfigurationAdapter:
    def __init__(self, context):
        self.__dict__["context"] = context
        self.__dict__["fti"] = self.context.fti

    def __getattr__(self, name):
        # be sure to get a valid value
        reg = lookup_behavior_registration(name=name)
        iid = reg.interface.__identifier__
        return iid in self.fti.behaviors or safe_text(reg.name) in self.fti.behaviors

    def __setattr__(self, name, value):
        # add or remove the behavior based on the value from the form
        behaviors = list(self.fti.behaviors)
        reg = lookup_behavior_registration(name=name)
        iid = reg.interface.__identifier__
        if reg.name:
            # behavior has a name -> use it
            # but first remove the dotted behavior if present
            if iid in self.fti.behaviors:
                behaviors.remove(iid)
            # prepare named behavior for add/remove
            bname = safe_text(reg.name)
        else:
            # no name found -> prepare dotted behavior for add/remove instead
            bname = iid

        # add/remove bname if based on value True false
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
                yield safe_text(reg.name)
            else:
                yield name


class TypeBehaviorsForm(form.EditForm):

    template = ViewPageTemplateFile("behaviors.pt")
    label = _("Behaviors")
    description = _("Select the behaviors to enable for this content type.")
    successMessage = _("Behaviors successfully updated.")
    noChangesMessage = _("No changes were made.")
    buttons = deepcopy(form.EditForm.buttons)
    buttons["apply"].title = _("Save")

    def getContent(self):
        return BehaviorConfigurationAdapter(self.context)

    @property
    def fields(self):
        counts = Counter([id(reg) for name, reg in getUtilitiesFor(IBehavior)])
        fields = []
        for name, reg in getUtilitiesFor(IBehavior):
            if name in TTW_BEHAVIOR_BLACKLIST:
                # skip blacklisted
                continue
            with_name = counts[id(reg)] > 1
            if with_name and reg.name != name:
                continue
            fname = safe_text(reg.name if reg.name else name)
            fields.append(
                schema.Bool(
                    __name__=fname,
                    title=reg.title,
                    description=reg.description,
                    required=False,
                )
            )
        form_fields = field.Fields(*sorted(fields, key=attrgetter("title")))
        for ff in form_fields.values():
            ff.widgetFactory = SingleCheckBoxFieldWidget
        return form_fields


class TypeBehaviorsPage(TypeFormLayout):
    form = TypeBehaviorsForm
    label = _("Behaviors")
