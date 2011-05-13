from zope.interface import Interface, Attribute
from zope.publisher.interfaces.browser import IBrowserPage
from zope import schema


class ITypesContext(IBrowserPage):
    """ A non-persistent traversable item corresponding to a Dexterity FTI
    """


class ITypeSchemaContext(Interface):
    """ Marker interface for plone.schemaeditor schema contexts that are
        associated with a Dexterity FTI """

    fti = Attribute(u"The FTI object associated with this schema.")
    schemaName = Attribute(u"The name of this schema within its FTI's model.")


class ITypeSettings(Interface):
    """ Define the fields for the content type add form
    """

    title = schema.TextLine(
        title = u'Type Name'
        )

    id = schema.ASCIILine(
        title = u'Short Name',
        description = u'Used for programmatic access to the type.',
        required=True,
        )

    description = schema.Text(
        title = u'Description',
        required = False
        )

    container = schema.Bool(
        title = u'Container',
        description = u'Items of this type will be able to contain other items.',
        required = True,
        default = False,
        )
