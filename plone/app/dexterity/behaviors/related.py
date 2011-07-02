"""BBB import for 'Related Items' behavior that was moved to
plone.app.relationfield.
"""
from plone.app.relationfield.behavior import IRelatedItems as IBaseRelatedItems

class IRelatedItems(IBaseRelatedItems):
    pass
