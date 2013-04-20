from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.z3cform.layout import FormWrapper

from plone.app.dexterity import MessageFactory as _


class TypeFormLayout(FormWrapper):

    index = ViewPageTemplateFile('tabbed_forms.pt')

    @property
    def tabs(self):
        return (
            (_('Overview'), '@@overview'),
            (_('Fields'), '@@fields'),
            (_('Behaviors'), '@@behaviors'),
        )
