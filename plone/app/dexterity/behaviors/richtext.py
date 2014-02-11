# -*- coding: utf-8 -*-
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.app.widgets.fields import RichTextField
from plone.supermodel import model
from zope.component import adapts
from zope.interface import alsoProvides, implements

from plone.app.contenttypes import _


class IRichText(model.Schema):

    text = RichTextField(
        title=_(u'Text', default=u'Text'),
        description=u"",
        required=False,
    )
    model.primary('text')


alsoProvides(IRichText, IFormFieldProvider)


class RichText(object):
    implements(IRichText)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context
