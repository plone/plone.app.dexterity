# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName


BAD_GUY = ('zope.intid.interfaces.IIntIds', '')


def fix_installed_products(context):
    qi = getToolByName(context, 'portal_quickinstaller', None)
    if qi is None:
        # Nothing to do.
        return
    for installed_product in qi.objectValues(spec='Installed Product'):
        if installed_product.getId() == 'plone.app.intid':
            continue
        utilities = getattr(aq_base(installed_product), 'utilities', [])
        if BAD_GUY in utilities:
            installed_product.utilities.remove(BAD_GUY)
