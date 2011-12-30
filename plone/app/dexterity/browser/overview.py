from z3c.form import form

from plone.app.dexterity.browser.layout import TypeFormLayout
from plone.app.dexterity import MessageFactory as _


class TypeOverviewForm(form.EditForm):
    pass


class TypeOverviewPage(TypeFormLayout):
    form = TypeOverviewForm
    label = _(u'Overview')