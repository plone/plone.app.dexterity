# -*- coding: utf-8 -*-
from plone.dexterity.interfaces import IDexterityContent
from plone.uuid.handlers import addAttributeUUID
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName


def add_missing_uuids(context):
    catalog = getToolByName(context, 'portal_catalog')
    query = {'object_provides': IDexterityContent.__identifier__}
    for brain in catalog.unrestrictedSearchResults(query):
        if getattr(brain, 'UID', None) is not None:
            continue
        ob = brain.getObject()
        if IUUID(ob, None) is None:
            addAttributeUUID(ob, None)
            ob.reindexObject(idxs=['UID'])
