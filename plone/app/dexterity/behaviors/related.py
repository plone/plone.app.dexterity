"""BBB import for 'Related Items' behavior that was moved to
plone.app.relationfield.
"""
from plone.app.relationfield.behavior import IRelatedItems as IBaseRelatedItems

from zope.interface import alsoProvides

from plone.supermodel.interfaces import FIELDSETS_KEY
from plone.supermodel.model import Fieldset

from plone.autoform.interfaces import IFormFieldProvider

from plone.app.dexterity import MessageFactory as _


class IRelatedItems(IBaseRelatedItems):
    pass

alsoProvides(IRelatedItems, IFormFieldProvider)
