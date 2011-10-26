from Products.CMFCore.utils import getToolByName
from plone.dexterity.interfaces import IDexterityContent

try:
    from plone.uuid.handlers import addAttributeUUID
    from plone.uuid.interfaces import IUUID
    HAS_UUID = True
except ImportError:
    HAS_UUID = False


def add_missing_uuids(context):
    if HAS_UUID:
        catalog = getToolByName(context, 'portal_catalog')
        query = {'object_provides': IDexterityContent.__identifier__}
        for b in catalog.unrestrictedSearchResults(query):
            ob = b._unrestrictedGetObject()
            if IUUID(ob, None) is None:
                addAttributeUUID(ob, None)
                ob.reindexObject(idxs=['UID'])
