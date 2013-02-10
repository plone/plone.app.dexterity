from plone.autoform.form import AutoExtensibleForm
from Products.CMFPlone import PloneMessageFactory as PC_
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import button
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope.interface import implements
from zope.interface import Interface
from zope.interface import invariant
from zope.interface.exceptions import Invalid
from zope.schema import List, Choice
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

#XXX
ACQUIRE = -1  # acquire locallyAllowedTypes from parent (default)
DISABLED = 0  # use default behavior of PortalFolder which uses the
              # FTI information
ENABLED = 1   # allow types from locallyAllowedTypes only

ST = lambda key, txt, default: SimpleTerm(value=key,
                                          title=PC_(txt, default=default))
possible_constrain_types = SimpleVocabulary(
    [ST(ACQUIRE, u'constraintypes_acquire_label',
                 u'Use parent folder settings'),
     ST(DISABLED, 'constraintypes_disable_label', u'Use portal default'),
     ST(ENABLED, u'constraintypes_enable_label', u'Select manually')
     ])


class ValidTypes(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        constrain_aspect = ISelectableConstrainTypes(context)
        items = []
        for type_ in constrain_aspect.getDefaultAddableTypes():
            items.append(SimpleTerm(value=type_.getId(), title=type_.Title()))
        return SimpleVocabulary(items)

ValidTypesFactory = ValidTypes()


class IConstrainForm(Interface):

    constrain_types_mode = Choice(
        title=PC_("label_type_restrictions", default="Type restrictions"),
        description=PC_("help_add_restriction_mode",
                        default="Select the restriction policy "
                        "in this location"),
        vocabulary=possible_constrain_types
    )

    current_prefer = List(
        title=PC_("label_immediately_addable_types", default="Allowed types"),
        description=PC_("help_immediately_addable_types",
                        default="Controls what types are addable "
                        "in this location"),
        value_type=Choice(
            source="plone.app.contenttypes.constrains.validtypes"),
    )

    current_allow = List(
        title=PC_("label_locally_allowed_types", default="Secondary types"),
        description=PC_("help_locally_allowed_types", default=""
                        "Select which types should be available in the "
                        "'More&hellip;' submenu <em>instead</em> of in the "
                        "main pulldown. "
                        "This is useful to indicate that these are not the "
                        "preferred types "
                        "in this location, but are allowed if your really "
                        "need them."
                        ),
        value_type=Choice(
            source="plone.app.contenttypes.constrains.validtypes"),
    )

    @invariant
    def legal_not_immediately_addable(data):
        missing = []
        for one_allowed in data.current_allow:
            if one_allowed not in data.current_prefer:
                missing.append(one_allowed)
        if missing:
            raise Invalid(
                PC_("You cannot have a type as a secondary type without "
                    "having it allowed. You have selected ${types}s.",
                    mapping=dict(types=", ".join(missing))))
        return True


class ConstrainsFormView(AutoExtensibleForm, form.EditForm):

    schema = IConstrainForm
    ignoreContext = True
    label = PC_("heading_set_content_type_restrictions",
                default="Restrict what types of content can be added")
    template = ViewPageTemplateFile("constrainsform.pt")

    def updateFields(self):
        super(ConstrainsFormView, self).updateFields()
        self.fields['current_prefer'].widgetFactory = CheckBoxFieldWidget
        self.fields['current_allow'].widgetFactory = CheckBoxFieldWidget

    def updateWidgets(self):
        super(ConstrainsFormView, self).updateWidgets()
        self.widgets['current_prefer'].addClass('current_prefer_form')
        self.widgets['current_allow'].addClass('current_allow_form')
        self.widgets['constrain_types_mode'].addClass(
            'constrain_types_mode_form')

    @button.buttonAndHandler(u'Save')
    def handleSave(self, action):
        data, errors = self.extractData()

        if errors:
            return

        immediately_addable_types = [t for t in data['current_prefer']
                                     if t not in data['current_allow']]
        locally_allowed_types = data['current_prefer']
        aspect = ISelectableConstrainTypes(self.context)
        aspect.setConstrainTypesMode(data['constrain_types_mode'])
        aspect.setLocallyAllowedTypes(locally_allowed_types)
        aspect.setImmediatelyAddableTypes(immediately_addable_types)

