# -*- coding: utf-8 -*-
from zope import schema

from zope.interface import alsoProvides

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.autoform.interfaces import IFormFieldProvider

from plone.supermodel import model

from plone.app.dexterity import MessageFactory as _


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


alsoProvides(IAllowDiscussion, IFormFieldProvider)
