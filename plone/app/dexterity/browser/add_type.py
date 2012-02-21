from z3c.form import form, field
from plone.z3cform.layout import wrap_form
from Products.CMFCore.utils import getToolByName

from plone.dexterity.fti import DexterityFTI
from plone.app.dexterity import MessageFactory as _
from plone.app.dexterity.interfaces import ITypeSettings

from plone.app.dexterity import PLONE40

class TypeAddForm(form.AddForm):

    label = _(u'Add Content Type')
    fields = field.Fields(ITypeSettings).select('title', 'id', 'description', 'container')
    id = 'add-type-form'

    def create(self, data):
        id = data.pop('id')

        fti = DexterityFTI(id)
        fti.id = id
        data['title'] = data['title'].encode('utf8')
        if data['description']:
            data['description'] = data['description'].encode('utf8')
        data['i18n_domain'] = 'plone'
        data['behaviors'] = "\n".join(['plone.app.dexterity.behaviors.metadata.IDublinCore',
                                       'plone.app.content.interfaces.INameFromTitle',
                                       ])
        data['model_source'] = """
<model xmlns="http://namespaces.plone.org/supermodel/schema">
    <schema>
    </schema>
</model>
"""
        if data['container']:
            data['klass'] = 'plone.dexterity.content.Container'
            data['filter_content_types'] = False
            del data['container']
            icon = 'folder_icon'
        else:
            icon = 'document_icon'
        if PLONE40:
            data['icon_expr'] = 'string:${portal_url}/' + icon + '.png'
        data['content_icon'] = icon + '.gif'
        fti.manage_changeProperties(**data)
        return fti

    def add(self, fti):
        ttool = getToolByName(self.context, 'portal_types')
        ttool._setObject(fti.id, fti)
        self.status = _(u"Type added successfully.")

    def nextURL(self):
        return self.context.absolute_url()

TypeAddFormPage = wrap_form(TypeAddForm)
