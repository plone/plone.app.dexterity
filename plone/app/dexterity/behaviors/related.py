"""BBB import for 'Related Items' behavior that was moved to
plone.app.relationfield in Dexterity 2.0.
"""
try:
    from plone.app.relationfield.behavior import IRelatedItems  # noqa
except ImportError:
    pass

from plone.behavior.interfaces import IBehavior
from zope.component import queryUtility


def related_items_behavior_BBB():
    return queryUtility(
        IBehavior, name="plone.app.relationfield.behavior.IRelatedItems"
    )
