from zope.publisher.interfaces.browser import IBrowserPage
from zope.schema import Object
from zope.schema.interfaces import IField

class ISchemaView(IBrowserPage):
    """ A publishable view of a zope 3 schema
    """

class IFieldEditingContext(IBrowserPage):
    """ A publishable view of a zope 3 schema field
    """

    field = Object(
        schema = IField
        )
