from AccessControl.SecurityManagement import getSecurityManager
from DateTime import DateTime
from datetime import datetime
from z3c.form.interfaces import IEditForm, IAddForm
from z3c.form.browser.textlines import TextLinesFieldWidget
from z3c.form.widget import ComputedWidgetAttribute
from zope.interface import alsoProvides
from zope.component import adapts
from zope import schema
from zope.schema.interfaces import IText, ISequence
from plone.autoform import directives as form
from plone.supermodel import model
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider
from plone.app.dexterity import PloneMessageFactory as _PMF

# Behavior interfaces to display Dublin Core metadata fields on Dexterity
# content edit forms.
#
# These schemata duplicate the fields of zope.dublincore.IZopeDublinCore,
# in order to annotate them with form hints and more helpful titles
# and descriptions.


class IBasic(model.Schema):

    # default fieldset
    title = schema.TextLine(
        title=_PMF(u'label_title', default=u'Title'),
        required=True
    )

    description = schema.Text(
        title=_PMF(u'label_description', default=u'Description'),
        description=_PMF(
            u'help_description',
            default=u'A short summary of the content.'
        ),
        required=False,
        missing_value=u'',
    )

    form.order_before(description='*')
    form.order_before(title='*')

    form.omitted('title', 'description')
    form.no_omit(IEditForm, 'title', 'description')
    form.no_omit(IAddForm, 'title', 'description')


class ICategorization(model.Schema):

    # categorization fieldset
    model.fieldset(
        'categorization',
        label=_PMF(u'label_schema_categorization', default=u'Categorization'),
        fields=['subjects', 'language'],
    )

    subjects = schema.Tuple(
        title=_PMF(u'label_tags', default=u'Tags'),
        description=_PMF(
            u'help_tags',
            default=u'Tags are commonly used for ad-hoc organization of ' +
                    u'content.'
        ),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )
    form.widget(subjects=TextLinesFieldWidget)

    language = schema.Choice(
        title=_PMF(u'label_language', default=u'Language'),
        vocabulary='plone.app.vocabularies.AvailableContentLanguages',
        required=False,
        missing_value='',
    )

    form.omitted('subjects', 'language')
    form.no_omit(IEditForm, 'subjects', 'language')
    form.no_omit(IAddForm, 'subjects', 'language')


class IPublication(model.Schema):
    # dates fieldset
    model.fieldset(
        'dates',
        label=_PMF(u'label_schema_dates', default=u'Dates'),
        fields=['effective', 'expires'],
    )

    effective = schema.Datetime(
        title=_PMF(u'label_effective_date', u'Publishing Date'),
        description=_PMF(
            u'help_effective_date',
            default=u"If this date is in the future, the content will "
                    u"not show up in listings and searches until this date."),
        required=False
    )

    expires = schema.Datetime(
        title=_PMF(u'label_expiration_date', u'Expiration Date'),
        description=_PMF(
            u'help_expiration_date',
            default=u"When this date is reached, the content will no"
                    u"longer be visible in listings and searches."),
        required=False
    )

    form.omitted('effective', 'expires')
    form.no_omit(IEditForm, 'effective', 'expires')
    form.no_omit(IAddForm, 'effective', 'expires')


class IOwnership(model.Schema):

    # ownership fieldset
    model.fieldset(
        'ownership',
        label=_PMF(
            'label_schema_ownership',
            default=u'Ownership'
        ),
        fields=['creators', 'contributors', 'rights'],
    )

    creators = schema.Tuple(
        title=_PMF(u'label_creators', u'Creators'),
        description=_PMF(
            u'help_creators',
            default=u"Persons responsible for creating the content of "
                    u"this item. Please enter a list of user names, one "
                    u"per line. The principal creator should come first."
        ),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )
    form.widget(creators=TextLinesFieldWidget)

    contributors = schema.Tuple(
        title=_PMF(u'label_contributors', u'Contributors'),
        description=_PMF(
            u'help_contributors',
            default=u"The names of people that have contributed "
                    u"to this item. Each contributor should "
                    u"be on a separate line."),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )
    form.widget(contributors=TextLinesFieldWidget)

    rights = schema.Text(
        title=_PMF(u'label_copyrights', default=u'Rights'),
        description=_PMF(
            u'help_copyrights',
            default=u'Copyright statement or other rights information on this '
                    u'item.'
        ),
        required=False,
    )

    form.omitted('creators', 'contributors', 'rights')
    form.no_omit(IEditForm, 'creators', 'contributors', 'rights')
    form.no_omit(IAddForm, 'creators', 'contributors', 'rights')


# make sure the add form shows the default creator
def creatorsDefault(data):
    user = getSecurityManager().getUser()
    return user and (user.getId(),)
CreatorsDefaultValue = ComputedWidgetAttribute(
    creatorsDefault,
    field=IOwnership['creators']
)


class IDublinCore(IOwnership, IPublication, ICategorization, IBasic):
    """ Metadata behavior providing all the DC fields
    """
    pass

# Mark these interfaces as form field providers
alsoProvides(IBasic, IFormFieldProvider)
alsoProvides(ICategorization, IFormFieldProvider)
alsoProvides(IPublication, IFormFieldProvider)
alsoProvides(IOwnership, IFormFieldProvider)
alsoProvides(IDublinCore, IFormFieldProvider)


class MetadataBase(object):
    """ This adapter uses DCFieldProperty to store metadata directly on an
        object using the standard CMF DefaultDublinCoreImpl getters and
        setters.
    """
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context


_marker = object()
class DCFieldProperty(object):
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
            attribute = getattr(field, 'default', _marker)
            if attribute is _marker:
                raise AttributeError(self._field.__name__)
        elif callable(attribute):
            attribute = attribute()

        if isinstance(attribute, DateTime):
            # Ensure datetime value is stripped of any timezone and seconds
            # so that it can be compared with the value returned by the widget
            return datetime(*map(int, attribute.parts()[:6]))

        if attribute is None:
            return

        if IText.providedBy(self._field):
            return attribute.decode('utf-8')

        if ISequence.providedBy(self._field):
            if IText.providedBy(self._field.value_type):
                return type(attribute)(
                    item.decode('utf-8') for item in attribute
                )

        return attribute

    def __set__(self, inst, value):
        field = self._field.bind(inst)
        field.validate(value)
        if field.readonly:
            raise ValueError(self._field.__name__, 'field is readonly')
        if isinstance(value, datetime):
            # The ensures that the converted DateTime value is in the
            # server's local timezone rather than GMT.
            value = DateTime(value.year, value.month, value.day,
                             value.hour, value.minute)
        elif value is not None:
            if IText.providedBy(self._field):
                value = value.encode('utf-8')

            elif ISequence.providedBy(self._field):
                if IText.providedBy(self._field.value_type):
                    value = type(value)(
                        item.encode('utf-8') for item in value
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
        if isinstance(value, str):
            raise ValueError('Title must be unicode.')
        self.context.title = value
    title = property(_get_title, _set_title)

    def _get_description(self):
        return self.context.description

    def _set_description(self, value):
        if isinstance(value, str):
            raise ValueError('Description must be unicode.')
        self.context.description = value
    description = property(_get_description, _set_description)


class Categorization(MetadataBase):

    def _get_subjects(self):
        return self.context.subject

    def _set_subjects(self, value):
        self.context.subject = value
    subjects = property(_get_subjects, _set_subjects)

    language = DCFieldProperty(
        ICategorization['language'],
        get_name='Language',
        set_name='setLanguage'
    )


class Publication(MetadataBase):
    effective = DCFieldProperty(
        IPublication['effective'],
        get_name='effective_date'
    )
    expires = DCFieldProperty(
        IPublication['expires'],
        get_name='expiration_date'
    )


class Ownership(MetadataBase):
    creators = DCFieldProperty(
        IOwnership['creators'],
        get_name='listCreators',
        set_name='setCreators'
    )
    contributors = DCFieldProperty(
        IOwnership['contributors'],
        get_name='Contributors',
        set_name='setContributors'
    )
    rights = DCFieldProperty(
        IOwnership['rights'],
        get_name='Rights',
        set_name='setRights'
    )

    def __init__(self, *args, **kwargs):
        super(Ownership, self).__init__(*args, **kwargs)
        self.context.addCreator()


class DublinCore(Basic, Categorization, Publication, Ownership):
    pass
