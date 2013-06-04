# -*- coding: utf-8 -*-
from z3c.form.interfaces import IEditForm, IAddForm
from zope import schema
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from plone.app.dexterity import MessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform import directives as form
from plone.supermodel import model


options = SimpleVocabulary([
    SimpleTerm(value=True, title=_(u'Yes')),
    SimpleTerm(value=False, title=_(u'No')),
])


class IAllowDiscussion(model.Schema):

    model.fieldset(
        'settings',
        label=_(u"Settings"),
        fields=['allow_discussion'],
    )

    allow_discussion = schema.Choice(
        title=_(u'Allow discussion'),
        description=_(u'Allow discussion for this content object.'),
        vocabulary=options,
        required=False,
        default=None,
    )

    form.omitted('allow_discussion')
    form.no_omit(IEditForm, 'allow_discussion')
    form.no_omit(IAddForm, 'allow_discussion')


alsoProvides(IAllowDiscussion, IFormFieldProvider)
