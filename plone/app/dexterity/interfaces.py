from zope.publisher.interfaces.browser import IBrowserPage
from zope.schema import Object
from zope.schema.interfaces import IField
from z3c.form.interfaces import IFieldWidget, IEditForm

class ISchemaView(IBrowserPage):
    """ A publishable view of a zope 3 schema
    """

class IFieldEditingContext(IBrowserPage):
    """ A publishable view of a zope 3 schema field
    """

    field = Object(
        schema = IField
        )

class IFieldEditForm(IEditForm):
    """ Marker interface for field edit forms
    """

class IMetaFieldWidget(IFieldWidget):
    """ Marker interface for a z3c.form widget that is a meta field widget.
    """
