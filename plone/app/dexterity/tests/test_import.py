# -*- coding: utf-8 -*-
"""Test the types import."""

from DateTime.DateTime import DateTime
from plone.app.dexterity.testing import DEXTERITY_INTEGRATION_TESTING
from plone.app.dexterity.browser.importtypes import TypesZipFileImportContext
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

import os.path
import unittest2 as unittest


class TestDexterityTypesImport(unittest.TestCase):
    """Test import."""

    layer = DEXTERITY_INTEGRATION_TESTING

    def testZipFileImportContext(self):
        portal = self.layer['portal']
        types_tool = getToolByName(portal, 'portal_types')

        zname = os.path.join(
            os.path.dirname(__file__),
            'import',
            'dexterity_export.zip',
        )
        f = open(zname, 'r')
        icontext = TypesZipFileImportContext(types_tool, f)

        types_xml = icontext.readDataFile('types.xml')
        self.assertTrue(
            types_xml,
            msg='Unable to read types.xml in sample import file',
        )

        self.assertTrue(
            isinstance(
                icontext.getLastModified('types.xml'),
                DateTime
            )
        )

        self.assertEqual(
            set(icontext.listDirectory('')),
            set(['types', 'types.xml'])
        )

        self.assertEqual(
            set(icontext.listDirectory('types')),
            set(['test_type_two.xml', 'test_type_one.xml'])
        )

        # test importIsTypesOnly check
        # self.assertTrue(icontext.importIsTypesOnly())

        f.close()

    def testSampleImportStep(self):
        """ Import our sample file
        """

        portal = self.layer['portal']
        setup_tool = getToolByName(portal, 'portal_setup')
        types_tool = getToolByName(portal, 'portal_types')
        old_types = set(types_tool.listContentTypes())

        handler = setup_tool.getImportStep(u'typeinfo')

        zname = os.path.join(
            os.path.dirname(__file__),
            'import',
            'dexterity_export.zip'
        )
        with open(zname, 'r') as f:
            icontext = TypesZipFileImportContext(types_tool, f)
            handler(icontext)

        # Our types list should have our two new types
        self.assertEqual(
            set(types_tool.listContentTypes()) - old_types,
            set(['test_type_one', 'test_type_two'])
        )

        # trying to create the context again should fail, since
        # it would be importing existing types.
        with open(zname, 'r') as f:
            self.assertRaises(ValueError,
                TypesZipFileImportContext,
                types_tool,
                f
            )


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
