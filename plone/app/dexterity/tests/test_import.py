# -*- coding: utf-8 -*-
"""Test the types import."""

from DateTime.DateTime import DateTime
from plone.app.dexterity.testing import DEXTERITY_INTEGRATION_TESTING
from plone.app.dexterity.browser.importtypes import ZipFileImportContext
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

import os.path
import StringIO
import unittest2 as unittest
import zipfile


class TestDexterityTypesImport(unittest.TestCase):
    """Test import."""

    layer = DEXTERITY_INTEGRATION_TESTING

    def testZipFileImportContext(self):
        portal = self.layer['portal']
        types_tool = getToolByName(portal, 'portal_types')

        zname = os.path.join(os.path.dirname(__file__), 'import', 'dexterity_export.zip')
        f = open(zname, 'r')
        icontext = ZipFileImportContext(types_tool, f)

        types_xml = icontext.readDataFile('types.xml')
        if not types_xml:
            self.fail('Unable to read types.xml in sample import file')

        if not isinstance(icontext.getLastModified('types.xml'), DateTime):
            self.fail('Bad modification time from zip import')

        f.close()



def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
