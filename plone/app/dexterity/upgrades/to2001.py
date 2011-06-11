from Products.CMFCore.utils import getToolByName
from plone.dexterity.interfaces import IDexterityContent
from plone.uuid.handlers import addAttributeUUID
from plone.uuid.interfaces import IUUID


def add_missing_uuids(context):
    catalog = getToolByName(context, 'portal_catalog')
    query = {'object_provides': IDexterityContent.__identifier__}
    for b in catalog.unrestrictedSearchResults(query):
        ob = b.getObject()
        if IUUID(ob, None) is None:
            addAttributeUUID(ob, None)
            ob.reindexObject(idxs=['UID'])
