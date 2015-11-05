# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.dexterity import _
from plone.z3cform.layout import FormWrapper


class TypeFormLayout(FormWrapper):

    index = ViewPageTemplateFile('tabbed_forms.pt')

    @property
    def tabs(self):
        return (
            (_('Overview'), '@@overview'),
            (_('Fields'), '@@fields'),
            (_('Behaviors'), '@@behaviors'),
        )
