# -*- coding: utf-8 -*-
"""Test the types import."""
from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from plone.app.dexterity.browser.import_types import ITypeProfileImport
from plone.app.dexterity.browser.import_types import TypeProfileImport
from plone.app.dexterity.browser.import_types import ZipFileImportContext
from plone.app.dexterity.testing import DEXTERITY_INTEGRATION_TESTING
import os.path
import plone.namedfile
import unittest
import zope.interface


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
        icontext = ZipFileImportContext(types_tool, f)

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
            icontext = ZipFileImportContext(types_tool, f)
            handler(icontext)

        # Our types list should have our two new types
        self.assertEqual(
            set(types_tool.listContentTypes()) - old_types,
            set(['test_type_one', 'test_type_two'])
        )

        # Trying to import now should fail, since
        # it would be importing existing types.
        # This is tested in an invariant.
        data = TypeProfileImport(profile_file=plone.namedfile.NamedFile())
        with open(zname, 'r') as f:
            data.profile_file.data = f.read()
        self.assertRaises(
            zope.interface.Invalid,
            ITypeProfileImport.validateInvariants,
            data
        )


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
