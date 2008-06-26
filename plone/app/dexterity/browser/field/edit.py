from zope.component import getUtility
from z3c.form import form, field, button, group, subform
from zope.schema.interfaces import IField
from plone.z3cform import base

class FieldEditForm(form.EditForm):

    def __init__(self, context, request):
        super(form.EditForm, self).__init__(context, request)
        self.field = context.field
        self.schema = [s for s in self.field.__provides__.__iro__ if s.isOrExtends(IField)][0]
    
    @property
    def fields(self):
        # omitting default and missing_value for now, until we figure out how to
        # make z3c.form find the right widget
        return field.Fields(self.schema).omit('default', 'missing_value', 'order')

# form wrapper to use Plone form template
class EditView(base.FormWrapper):
    form = FieldEditForm

    def __init__(self, context, request):
        super(EditView, self).__init__(context, request)
        self.field = context.field

    @property
    def label(self):
        return u"Edit Field '%s'" % self.field.__name__
