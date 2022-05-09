from AccessControl.SecurityManagement import getSecurityManager
from datetime import datetime
from DateTime import DateTime
from plone.app.dexterity import _
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.app.z3cform.widget import DatetimeFieldWidget
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.base.interfaces.siteroot import IPloneSiteRoot
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.utils import safe_unicode
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from z3c.form.widget import ComputedWidgetAttribute
from zope import schema
from zope.component import adapter
from zope.component.hooks import getSite
from zope.interface import Invalid
from zope.interface import invariant
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


# Behavior interfaces to display Dublin Core metadata fields on Dexterity
# content edit forms.
#
# These schemata duplicate the fields of zope.dublincore.IZopeDublinCore,
# in order to annotate them with form hints and more helpful titles
# and descriptions.


@provider(IContextAwareDefaultFactory)
def default_language(context):
    # If we are adding a new object, context will be the folderish object where
    # this new content is being added
    language = None

    # Try to get the language from context or parent(s)
    while not language and context is not None and not IPloneSiteRoot.providedBy(context):
        language = getattr(context.aq_base, 'language', None)

        if not language:
            # If we are here, it means we were editing an object that didn't
            # have its language set or that the container where we were adding
            # the new content didn't have a language set. So we check its
            # parent.
            context = context.__parent__

    language_tool = getToolByName(getSite(), 'portal_languages')
    default_language = language_tool.getDefaultLanguage()

    if not language:
        language = default_language

    # Is the language supported/enabled at all?
    if language not in language_tool.getAvailableLanguages():
        language = default_language

    return language


@provider(IFormFieldProvider)
class IBasic(model.Schema):

    # default fieldset
    title = schema.TextLine(title=_("label_title", default="Title"), required=True)

    description = schema.Text(
        title=_("label_description", default="Summary"),
        description=_(
            "help_description", default="Used in item listings and search results."
        ),
        required=False,
        missing_value="",
    )

    directives.order_before(description="*")
    directives.order_before(title="*")

    directives.omitted("title", "description")
    directives.no_omit(IEditForm, "title", "description")
    directives.no_omit(IAddForm, "title", "description")


@provider(IFormFieldProvider)
class ICategorization(model.Schema):

    # categorization fieldset
    model.fieldset(
        "categorization",
        label=_("label_schema_categorization", default="Categorization"),
        fields=["subjects", "language"],
    )

    subjects = schema.Tuple(
        title=_("label_tags", default="Tags"),
        description=_(
            "help_tags",
            default="Tags are commonly used for ad-hoc organization of " + "content.",
        ),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )
    directives.widget(
        "subjects", AjaxSelectFieldWidget, vocabulary="plone.app.vocabularies.Keywords"
    )

    language = schema.Choice(
        title=_("label_language", default="Language"),
        vocabulary="plone.app.vocabularies.SupportedContentLanguages",
        required=False,
        missing_value="",
        defaultFactory=default_language,
    )
    directives.widget("language", SelectFieldWidget)

    directives.omitted("subjects", "language")
    directives.no_omit(IEditForm, "subjects", "language")
    directives.no_omit(IAddForm, "subjects", "language")


class EffectiveAfterExpires(Invalid):
    __doc__ = _(
        "error_invalid_publication", default="Invalid effective or expires date"
    )


@provider(IFormFieldProvider)
class IPublication(model.Schema):
    # dates fieldset
    model.fieldset(
        "dates",
        label=_("label_schema_dates", default="Dates"),
        fields=["effective", "expires"],
    )

    effective = schema.Datetime(
        title=_("label_effective_date", "Publishing Date"),
        description=_(
            "help_effective_date",
            default="If this date is in the future, the content will "
            "not show up in listings and searches until this date.",
        ),
        required=False,
    )
    directives.widget("effective", DatetimeFieldWidget)

    expires = schema.Datetime(
        title=_("label_expiration_date", "Expiration Date"),
        description=_(
            "help_expiration_date",
            default="When this date is reached, the content will no "
            "longer be visible in listings and searches.",
        ),
        required=False,
    )
    directives.widget("expires", DatetimeFieldWidget)

    @invariant
    def validate_start_end(data):
        if data.effective and data.expires and data.effective > data.expires:
            raise EffectiveAfterExpires(
                _(
                    "error_expiration_must_be_after_effective_date",
                    default="Expiration date must be after publishing date.",
                )
            )

    directives.omitted("effective", "expires")
    directives.no_omit(IEditForm, "effective", "expires")
    directives.no_omit(IAddForm, "effective", "expires")


@provider(IFormFieldProvider)
class IOwnership(model.Schema):

    # ownership fieldset
    model.fieldset(
        "ownership",
        label=_("label_schema_ownership", default="Ownership"),
        fields=["creators", "contributors", "rights"],
    )

    creators = schema.Tuple(
        title=_("label_creators", "Creators"),
        description=_(
            "help_creators",
            default="Persons responsible for creating the content of "
            "this item. Please enter a list of user names, one "
            "per line. The principal creator should come first.",
        ),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )
    directives.widget(
        "creators", AjaxSelectFieldWidget, vocabulary="plone.app.vocabularies.Users"
    )

    contributors = schema.Tuple(
        title=_("contributors", "Contributors"),
        description=_(
            "help_contributors",
            default="The names of people that have contributed "
            "to this item. Each contributor should "
            "be on a separate line.",
        ),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )
    directives.widget(
        "contributors", AjaxSelectFieldWidget, vocabulary="plone.app.vocabularies.Users"
    )

    rights = schema.Text(
        title=_("label_copyrights", default="Rights"),
        description=_(
            "help_copyrights",
            default="Copyright statement or other rights information on this " "item.",
        ),
        required=False,
    )

    directives.omitted("creators", "contributors", "rights")
    directives.no_omit(IEditForm, "creators", "contributors", "rights")
    directives.no_omit(IAddForm, "creators", "contributors", "rights")


# make sure the add form shows the default creator
def creatorsDefault(data):
    user = getSecurityManager().getUser()
    # NB: CMF users are UTF-8 encoded bytes, decode them before inserting
    return user and (safe_unicode(user.getId()),)


CreatorsDefaultValue = ComputedWidgetAttribute(
    creatorsDefault, field=IOwnership["creators"]
)


@provider(IFormFieldProvider)
class IDublinCore(IOwnership, IPublication, ICategorization, IBasic):
    """Metadata behavior providing all the DC fields"""

    pass


@adapter(IDexterityContent)
class MetadataBase:
    """This adapter uses DCFieldProperty to store metadata directly on an
    object using the standard CMF DefaultDublinCoreImpl getters and
    setters.
    """

    def __init__(self, context):
        self.context = context


_marker = object()


class DCFieldProperty:
    """Computed attributes based on schema fields.
    Based on zope.schema.fieldproperty.FieldProperty.
    """

    def __init__(self, field, get_name=None, set_name=None):
        if get_name is None:
            get_name = field.__name__
        self._field = field
        self._get_name = get_name
        self._set_name = set_name

    def __get__(self, inst, klass):
        if inst is None:
            return self

        attribute = getattr(inst.context, self._get_name, _marker)
        if attribute is _marker:
            field = self._field.bind(inst)
            attribute = getattr(field, "default", _marker)
            if attribute is _marker:
                raise AttributeError(self._field.__name__)
        elif callable(attribute):
            attribute = attribute()

        if isinstance(attribute, DateTime):
            # Ensure datetime value is stripped of any timezone and seconds
            # so that it can be compared with the value returned by the widget
            return datetime(*list(map(int, attribute.parts()[:6])))

        if attribute is None:
            return

        return attribute

    def __set__(self, inst, value):
        field = self._field.bind(inst)
        field.validate(value)
        if field.readonly:
            raise ValueError(self._field.__name__, "field is readonly")
        if isinstance(value, datetime):
            # The ensures that the converted DateTime value is in the
            # server's local timezone rather than GMT.
            value = DateTime(
                value.year, value.month, value.day, value.hour, value.minute
            )

        if self._set_name:
            getattr(inst.context, self._set_name)(value)
        elif inst.context.hasProperty(self._get_name):
            inst.context._updateProperty(self._get_name, value)
        else:
            setattr(inst.context, self._get_name, value)

    def __getattr__(self, name):
        return getattr(self._field, name)


class Basic(MetadataBase):
    def _get_title(self):
        return self.context.title

    def _set_title(self, value):
        if not isinstance(value, str):
            raise ValueError("Title must be text.")
        self.context.title = value

    title = property(_get_title, _set_title)

    def _get_description(self):
        return self.context.description

    def _set_description(self, value):
        if not isinstance(value, str):
            raise ValueError("Description must be text.")

        self.context.description = value

    description = property(_get_description, _set_description)


class Categorization(MetadataBase):
    def _get_subjects(self):
        return self.context.subject

    def _set_subjects(self, value):
        self.context.subject = value

    subjects = property(_get_subjects, _set_subjects)

    language = DCFieldProperty(
        ICategorization["language"], get_name="Language", set_name="setLanguage"
    )


class Publication(MetadataBase):
    effective = DCFieldProperty(IPublication["effective"], get_name="effective_date")
    expires = DCFieldProperty(IPublication["expires"], get_name="expiration_date")


class Ownership(MetadataBase):
    creators = DCFieldProperty(
        IOwnership["creators"], get_name="listCreators", set_name="setCreators"
    )
    contributors = DCFieldProperty(
        IOwnership["contributors"], get_name="Contributors", set_name="setContributors"
    )
    rights = DCFieldProperty(
        IOwnership["rights"], get_name="Rights", set_name="setRights"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context.addCreator()


class DublinCore(Basic, Categorization, Publication, Ownership):
    pass
