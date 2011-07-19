from AccessControl.SecurityManagement import getSecurityManager
from DateTime import DateTime
from datetime import datetime
from z3c.form.interfaces import IEditForm, IAddForm
from zope.interface import alsoProvides
from zope.component import adapts
from zope import schema
from plone.directives import form
from plone.dexterity.interfaces import IDexterityContent
from plone.autoform.interfaces import IFormFieldProvider

try:
    from z3c.form.browser.textlines import TextLinesFieldWidget
except ImportError:
    from plone.z3cform.textlines.textlines import TextLinesFieldWidget

from plone.app.dexterity import PloneMessageFactory as _

# Behavior interfaces to display Dublin Core metadata fields on Dexterity
# content edit forms.
#     
# These schemata duplicate the fields of zope.dublincore.IZopeDublinCore,
# in order to annotate them with form hints and more helpful titles
# and descriptions.

class IBasic(form.Schema):
    # default fieldset
    title = schema.TextLine(
        title = _(u'label_title', default=u'Title'),
        required = True
        )
        
    description = schema.Text(
        title=_(u'label_description', default=u'Description'),
        description = _(u'help_description', default=u'A short summary of the content.'),
        required = False,
        missing_value = u'',
        )
    
    form.order_before(description = '*')
    form.order_before(title = '*')
    
    form.omitted('title', 'description')
    form.no_omit(IEditForm, 'title', 'description')
    form.no_omit(IAddForm, 'title', 'description')

class ICategorization(form.Schema):
    # categorization fieldset
    form.fieldset(
        'categorization',
        label=_(u'Categorization'),
        fields=['subjects', 'language'],
        )

    subjects = schema.Tuple(
        title = _(u'label_categories', default=u'Categories'),
        description = _(u'help_categories', default=u'Also known as keywords, tags or labels, these help you categorize your content.'),
        value_type = schema.TextLine(),
        required = False,
        missing_value = (),
        )
    form.widget(subjects = TextLinesFieldWidget)

    language = schema.Choice(
        title = _(u'label_language', default=u'Language'),
        vocabulary = 'plone.app.vocabularies.AvailableContentLanguages',
        required = False,
        missing_value = '',
        )
    
    form.omitted('subjects', 'language')
    form.no_omit(IEditForm, 'subjects', 'language')
    form.no_omit(IAddForm, 'subjects', 'language')

class IPublication(form.Schema):
    # dates fieldset
    form.fieldset(
        'dates',
        label=_(u'Dates'),
        fields=['effective', 'expires'],
        )
    
    effective = schema.Datetime(
        title = _(u'label_effective_date', u'Publishing Date'),
        description = _(u'help_effective_date',
                          default=u"If this date is in the future, the content will "
                                   "not show up in listings and searches until this date."),
        required = False
        )
        
    expires = schema.Datetime(
        title = _(u'label_expiration_date', u'Expiration Date'),
        description = _(u'help_expiration_date',
                              default=u"When this date is reached, the content will no"
                                       "longer be visible in listings and searches."),
        required = False
        )
    
    form.omitted('effective', 'expires')
    form.no_omit(IEditForm, 'effective', 'expires')
    form.no_omit(IAddForm, 'effective', 'expires')

class IOwnership(form.Schema):
    # ownership fieldset
    form.fieldset(
        'ownership',
        label=_(u'Ownership'),
        fields=['creators', 'contributors', 'rights'],
        )

    creators = schema.Tuple(
        title = _(u'label_creators', u'Creators'),
        description = _(u'help_creators',
                          default=u"Persons responsible for creating the content of "
                                   "this item. Please enter a list of user names, one "
                                   "per line. The principal creator should come first."),
        value_type = schema.TextLine(),
        required = False,
        missing_value = (),
        )
    form.widget(creators = TextLinesFieldWidget)
    
    contributors = schema.Tuple(
        title = _(u'label_contributors', u'Contributors'),
        description = _(u'help_contributors',
                          default=u"The names of people that have contributed "
                                   "to this item. Each contributor should "
                                   "be on a separate line."),
        value_type = schema.TextLine(),
        required = False,
        missing_value = (),
        )
    form.widget(contributors = TextLinesFieldWidget)
    
    rights = schema.Text(
        title=_(u'label_copyrights', default=u'Rights'),
        description=_(u'help_copyrights',
                          default=u'Copyright statement or other rights information on this item.'),
        required = False,
        )
    
    form.omitted('creators', 'contributors', 'rights')
    form.no_omit(IEditForm, 'creators', 'contributors', 'rights')
    form.no_omit(IAddForm, 'creators', 'contributors', 'rights')

# make sure the add form shows the default creator
@form.default_value(field=IOwnership['creators'])
def creatorsDefault(data):
    user = getSecurityManager().getUser()
    return user and (user.getId(),)

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
    """ This adapter uses DCFieldProperty to store metadata directly on an object
        using the standard CMF DefaultDublinCoreImpl getters and setters.
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

    language = DCFieldProperty(ICategorization['language'], get_name = 'Language', set_name = 'setLanguage')
    
class Publication(MetadataBase):
    effective = DCFieldProperty(IPublication['effective'], get_name = 'effective_date')
    expires = DCFieldProperty(IPublication['expires'], get_name = 'expiration_date')

class Ownership(MetadataBase):
    creators = DCFieldProperty(IOwnership['creators'], get_name = 'listCreators', set_name = 'setCreators')
    contributors = DCFieldProperty(IOwnership['contributors'], get_name = 'Contributors', set_name = 'setContributors')
    rights = DCFieldProperty(IOwnership['rights'], get_name = 'Rights', set_name = 'setRights')

    def __init__(self, *args, **kwargs):
        super(Ownership, self).__init__(*args, **kwargs)
        self.context.addCreator()

class DublinCore(Basic, Categorization, Publication, Ownership):
    pass
