from plone.app.dexterity import _
from plone.app.dexterity.interfaces import ITypeSettings
from plone.base.utils import safe_text
from plone.dexterity.fti import DexterityFTI
from plone.z3cform.layout import wrap_form
from Products.CMFCore.utils import getToolByName
from z3c.form import field
from z3c.form import form


class TypeAddForm(form.AddForm):

    label = _("Add Content Type")
    fields = field.Fields(ITypeSettings).select("title", "id", "description")
    id = "add-type-form"
    fti_id = None

    def create(self, data):
        id = data.pop("id")

        fti = DexterityFTI(id)
        fti.id = id
        data["title"] = safe_text(data["title"])
        if data["description"]:
            data["description"] = safe_text(data["description"])
        data["i18n_domain"] = "plone"
        data["behaviors"] = "\n".join(
            [
                "plone.dublincore",
                "plone.namefromtitle",
            ]
        )
        data[
            "model_source"
        ] = """
<model xmlns="http://namespaces.plone.org/supermodel/schema">
    <schema>
    </schema>
</model>
"""

        data["klass"] = "plone.dexterity.content.Container"
        data["filter_content_types"] = True
        data["icon_expr"] = "string:file-earmark-text"
        fti.manage_changeProperties(**data)
        return fti

    def add(self, fti):
        ttool = getToolByName(self.context, "portal_types")
        ttool._setObject(fti.id, fti)
        self.fti_id = fti.id
        self.status = _("Type added successfully.")

    def nextURL(self):
        url = self.context.absolute_url()
        if self.fti_id is not None:
            url += f"/{self.fti_id}/@@fields"
        return url


TypeAddFormPage = wrap_form(TypeAddForm)
