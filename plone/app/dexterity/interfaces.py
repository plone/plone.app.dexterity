import re
from Acquisition import aq_base
from zope.interface import Interface, Attribute, Invalid
from zope.publisher.interfaces.browser import IBrowserPage
from zope import schema
from z3c.form import validator
from plone.app.dexterity import MessageFactory as _
from Products.CMFCore.utils import getToolByName


class ITypesContext(IBrowserPage):
    """ A non-persistent traversable item corresponding to a Dexterity FTI
    """


class ITypeSchemaContext(Interface):
    """ Marker interface for plone.schemaeditor schema contexts that are
        associated with a Dexterity FTI """

    fti = Attribute(u"The FTI object associated with this schema.")
    schemaName = Attribute(u"The name of this schema within its FTI's model.")


class InvalidIdError(schema.ValidationError):
    __doc__ = _(u'Please use only letters, numbers, and the following characters: .-_')

# a letter followed by letters, numbers, period, hyphen, or underscore
ID_RE = re.compile(r'^[a-z][\w\d\.-]*$')

def isValidId(value):
    if ID_RE.match(value):
        return True
    raise InvalidIdError


class ITypeSettings(Interface):
    """ Define the fields for the content type add form
    """

    title = schema.TextLine(
        title = _(u'Type Name'),
        )

    id = schema.ASCIILine(
        title = _(u'Short Name'),
        description = _(u'Used for programmatic access to the type.'),
        required = True,
        constraint = isValidId,
        )

    description = schema.Text(
        title = _(u'Description'),
        required = False
        )

    container = schema.Bool(
        title = _(u'Container'),
        description = _(u'Items of this type will be able to contain other items.'),
        required = True,
        default = False,
        )

    allowed_content_types = schema.Set(
        title=_(u'Allowed Content Types'),
        description=_(
            u'The content that may be added if this type is a container.'),
        required=False,
        value_type=schema.Choice(
            title=_(u'Content Type'),
            description=_(u'Select each content type that may be added.'),
            vocabulary=(
                'plone.app.vocabularies.ReallyUserFriendlyTypes'),
        required=False))

    filter_content_types = schema.Bool(
        title=_(u'Filter Content Types'),
        description=_(
            u'Should the container restrict which content may be added '
            u'according to "Allowed Content Types"?'),
        default=False,
        required=False)


class ITypeStats(Interface):
    
    item_count = schema.Int(
        title = _(u'# of items'),
        )


class TypeIdValidator(validator.SimpleFieldValidator):

    def validate(self, value):
        super(TypeIdValidator, self).validate(value)

        ttool = getToolByName(self.context, 'portal_types')
        if value in ttool.objectIds():
            raise Invalid(_(u"There is already a content type named '${name}'",
                          mapping={'name': value}))

validator.WidgetValidatorDiscriminators(TypeIdValidator, field=ITypeSettings['id'])


class TypeTitleValidator(validator.SimpleFieldValidator):

    def validate(self, value):
        super(TypeTitleValidator, self).validate(value)

        ttool = getToolByName(self.context, 'portal_types')
        for existing_fti in ttool.objectValues():
            if aq_base(existing_fti) is aq_base(self.context):
                continue

            if existing_fti.Title() == value:
                raise Invalid(_(u"There is already a content type named '${name}'",
                              mapping={'name': value}))

validator.WidgetValidatorDiscriminators(TypeTitleValidator, field=ITypeSettings['title'])
