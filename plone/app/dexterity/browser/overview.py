from z3c.form import form, field
from z3c.form.interfaces import HIDDEN_MODE

from plone.app.dexterity.browser.layout import TypeFormLayout
from plone.app.dexterity.interfaces import ITypeSettings
from plone.app.dexterity import MessageFactory as _


class TypeOverviewForm(form.EditForm):
    fields = field.Fields(ITypeSettings).select(
        'title', 'description',
        'allowed_content_types', 'filter_content_types')
    fields['filter_content_types'].mode = HIDDEN_MODE

    def getContent(self):
        return self.context.fti

    def updateWidgets(self):
        super(TypeOverviewForm, self).updateWidgets()

        if self.context.fti.klass != 'plone.dexterity.content.Container':
            del self.widgets['allowed_content_types']
            del self.widgets['filter_content_types']

    def applyChanges(self, data):
        """Handle allowed content types"""
        if self.context.fti.klass == 'plone.dexterity.content.Container':
            data['filter_content_types'] = False
            if data.get('allowed_content_types'):
                data['filter_content_types'] = True

        return super(TypeOverviewForm, self).applyChanges(data)

class TypeOverviewPage(TypeFormLayout):
    form = TypeOverviewForm
    label = _(u'Overview')
