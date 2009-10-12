from zope.interface import Interface, Attribute
from zope.publisher.interfaces.browser import IBrowserPage

class ITypesContext(IBrowserPage):
    """ A non-persistent traversable item corresponding to a Dexterity FTI
    """

class ITypeSchemaContext(Interface):
    """ Marker interface for plone.schemaeditor schema contexts that are
        associated with a Dexterity FTI """

    fti = Attribute(u'The FTI object associated with this schema.')
