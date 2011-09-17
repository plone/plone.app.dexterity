from z3c.form import form, field
from plone.z3cform.layout import wrap_form
from Products.CMFCore.utils import getToolByName

from plone.dexterity.fti import DexterityFTI
from plone.app.dexterity import MessageFactory as _
from plone.app.dexterity.interfaces import ITypeSettings

class TypeCloneForm(form.AddForm):

    label = _(u'Clone Content Type')
    fields = field.Fields(ITypeSettings).select('title', 'id')
    id = 'clone-type-form'

    def create(self, data):
        id = data.pop('id')
        props = dict(self.context.fti.propertyItems())
        # make sure we don't share the factory
        if props['factory'] == self.context.fti.getId():
            del props['factory']
        props['title'] = data['title']
        fti = DexterityFTI(id, **props)
        return fti

    def add(self, fti):
        ttool = getToolByName(self.context, 'portal_types')
        ttool._setObject(fti.id, fti)
        self.status = _(u"Type cloned successfully.")

    def nextURL(self):
        return self.context.aq_parent.absolute_url()

TypeCloneFormPage = wrap_form(TypeCloneForm)
