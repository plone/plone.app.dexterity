"""BBB import for 'Related Items' behavior that was moved to
plone.app.relationfield.
"""
from plone.app.relationfield.behavior import IRelatedItems
IRelatedItems # pyflakes

from zope.component import queryUtility
from plone.behavior.interfaces import IBehavior

def related_items_behavior_BBB():
    return queryUtility(IBehavior, name=u'plone.app.relationfield.behavior.IRelatedItems')
