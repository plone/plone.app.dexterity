# -*- coding: utf-8 -*-
from Acquisition import aq_base
from plone.app.dexterity import _
from Products.CMFCore.utils import getToolByName
from z3c.form import validator
from zope import schema
from zope.filerepresentation.interfaces import IFileFactory
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import Invalid
from zope.publisher.interfaces.browser import IBrowserPage

import re


class ITypesContext(IBrowserPage):
    """ A non-persistent traversable item corresponding to a Dexterity FTI
    """


class ITypeSchemaContext(Interface):
    """ Marker interface for plone.schemaeditor schema contexts that are
        associated with a Dexterity FTI """

    fti = Attribute(u"The FTI object associated with this schema.")
    schemaName = Attribute(u"The name of this schema within its FTI's model.")


class InvalidIdError(schema.ValidationError):
    __doc__ = _(
        u'Please use only letters, numbers and the following characters: .-_')


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
        title=_(u'Type Name'),
    )

    id = schema.ASCIILine(
        title=_(u'Short Name'),
        description=_(u'Used for programmatic access to the type.'),
        required=True,
        constraint=isValidId,
    )

    description = schema.Text(
        title=_(u'Description'),
        required=False
    )

    container = schema.Bool(
        title=_(u'Container'),
        description=_(
            u'Items of this type will be able to contain other items.'),
        required=True,
        default=False,
    )

    filter_content_types = schema.Choice(
        title=_(u'Filter Contained Types'),
        description=_(
            'label_filter_contained_types',
            default=(
                u'Items of this type can act as a folder containing other '
                u' items. What content types should be allowed inside?')
        ),
        values=('none', 'all', 'some'),
        default='none',
        required=True
    )

    allowed_content_types = schema.Set(
        title=_(u'Allowed Content Types'),
        required=False,
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes',
            required=False
        )
    )


class ITypeStats(Interface):

    item_count = schema.Int(
        title=_(u'# of items'),
    )


class TypeIdValidator(validator.SimpleFieldValidator):

    def validate(self, value):
        super(TypeIdValidator, self).validate(value)

        ttool = getToolByName(self.context, 'portal_types')
        if value in ttool.objectIds():
            msg = u"There is already a content type named '${name}'"
            raise Invalid(_(msg, mapping={'name': value}))


validator.WidgetValidatorDiscriminators(
    TypeIdValidator,
    field=ITypeSettings['id']
)


class TypeTitleValidator(validator.SimpleFieldValidator):

    def validate(self, value):
        super(TypeTitleValidator, self).validate(value)

        ttool = getToolByName(self.context, 'portal_types')
        for existing_fti in ttool.objectValues():
            if aq_base(existing_fti) is aq_base(self.context):
                continue

            if existing_fti.Title() == value:
                msg = u"There is already a content type named '${name}'"
                raise Invalid(_(msg, mapping={'name': value}))


validator.WidgetValidatorDiscriminators(
    TypeTitleValidator,
    field=ITypeSettings['title']
)


class IDXFileFactory(IFileFactory):
    """ adapter factory for DX types
    """
