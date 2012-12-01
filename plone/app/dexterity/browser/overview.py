from z3c.form import form, field
from z3c.form.interfaces import DISPLAY_MODE

from plone.app.dexterity.browser.layout import TypeFormLayout
from plone.app.dexterity.interfaces import ITypeSettings
from plone.app.dexterity import MessageFactory as _


class TypeOverviewForm(form.EditForm):
    fields = field.Fields(ITypeSettings).select('id', 'title', 'description')
    fields['id'].mode = DISPLAY_MODE

    def getContent(self):
        return self.context.fti


class TypeOverviewPage(TypeFormLayout):
    form = TypeOverviewForm
    label = _(u'Overview')
