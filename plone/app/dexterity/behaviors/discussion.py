# -*- coding: utf-8 -*-
from plone.app.dexterity import _
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import provider
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


options = SimpleVocabulary([
    SimpleTerm(value=True, title=_(u'Yes')),
    SimpleTerm(value=False, title=_(u'No')),
])


@provider(IFormFieldProvider)
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

    directives.omitted('allow_discussion')
    directives.no_omit(IEditForm, 'allow_discussion')
    directives.no_omit(IAddForm, 'allow_discussion')
