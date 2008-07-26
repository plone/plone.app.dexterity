from zope.interface import implements, implementer, alsoProvides, Interface
from zope.component import getUtility, getMultiAdapter, queryMultiAdapter, adapter, adapts
from z3c.form import form, field, button, group, subform, validator
from z3c.form.interfaces import IFieldWidget, IDataConverter
from zope.schema.interfaces import IField
from zope.schema._bootstrapinterfaces import RequiredMissing
from plone.z3cform import layout
from plone.app.dexterity.interfaces import IFieldEditForm, IMetaFieldWidget

class FieldEditForm(form.EditForm):
    implements(IFieldEditForm)

    def __init__(self, context, request):
        super(form.EditForm, self).__init__(context, request)
        self.field = context.field
        self.schema = [s for s in self.field.__provides__.__iro__ if s.isOrExtends(IField)][0]
    
    @property
    def fields(self):
        # omit the order attribute since it's managed elsewhere
        fields = field.Fields(self.schema).omit('order')
        
        # The 'default' and 'missing_value' metafields are just a generic Field in the
        # zope.schema.interfaces.IField schema, so let's use the widget for the actual
        # field we're editing.
        fields['default'].widgetFactory = MetaFieldWidgetFactory(self.field)
        fields['missing_value'].widgetFactory = MetaFieldWidgetFactory(self.field)
        return fields

# form wrapper to use Plone form template
class EditView(layout.FormWrapper):
    form = FieldEditForm

    def __init__(self, context, request):
        super(EditView, self).__init__(context, request)
        self.field = context.field

    @property
    def label(self):
        return u"Edit Field '%s'" % self.field.__name__

class MetaFieldWidgetFactory(object):
    """ Factory for creating meta field widgets.
        A "meta field" is a field belonging to the schema of a field.
        A "meta field widget" is found based on the schema of the (outer) field,
           but most of its settings are based on the (inner) meta field.
           
        We use this to handle the 'default' and 'missing_value' meta fields,
        which simply use the zope.schema.Field schema -- but we still want to
        look up a sensible widget to use with them.
    """
    
    def __init__(self, outer_field):
        self.outer_field = outer_field
        
    def __call__(self, inner_field, request):
        # use the field class from the outer field, but the field settings
        # from the inner field
        clone_field = self.outer_field.__class__.__new__(self.outer_field.__class__)
        clone_field.__dict__.update(inner_field.__dict__)
                
        # look up the widget for the interfaces provided by the outer field
        widget = getMultiAdapter((clone_field, request), IFieldWidget)
        
        # zope.schema.interfaces.IField marks 'default' and 'missing_value' as required,
        # but they aren't really
        widget.required = False
        
        return widget

@adapter(IMetaFieldWidget)
@implementer(IDataConverter)
def MetaFieldWidgetDataConverter(widget):
    """Provide a data converter based on a meta field widget."""
    return queryMultiAdapter((widget.outer_field, widget), IDataConverter)

class MetaFieldValidator(validator.SimpleFieldValidator):
    """ Wrap the normal form validator to disable the 'required' check for the
        'default' and 'missing_value' metafields (which are incorrectly marked as required
        in zope.schema.interfaces)
    """
    adapts(Interface, Interface, IFieldEditForm, IField, Interface)
    
    def validate(self, value):
        try:
            return super(MetaFieldValidator, self).validate(value)
        except RequiredMissing:
            if self.field.__name__ not in ('default', 'missing_value'):
                raise
            