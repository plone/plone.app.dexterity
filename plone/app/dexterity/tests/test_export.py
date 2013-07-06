# -*- coding: utf-8 -*-
"""Test the @@types-export view."""

from plone.app.dexterity.testing import DEXTERITY_INTEGRATION_TESTING
from plone.app.dexterity.tests.test_constrains import add_item_type
from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError
from zope.component import getMultiAdapter

import StringIO
import unittest2 as unittest
import zipfile


class TestExportXMLValidity(unittest.TestCase):
    """Test that exported XML is valid."""

    layer = DEXTERITY_INTEGRATION_TESTING

    def test_exported_XML_valid_for_GS(self):
        """Test that exported XMLs can be parsed by GenericSetup's parser."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        # create a Dexterity item that we can export
        self.item = add_item_type(self.portal)

        # request is expected to have the 'selected' parameter set
        self.request['selected'] = 'item'

        # get the export view
        dexterity_control_panel = getMultiAdapter(
            (self.portal, self.request), name='dexterity-types')
        types_export_view = getMultiAdapter(
            (dexterity_control_panel, self.request), name='types-export')

        # export the 'item' type and try to parse all XMLs
        fd = StringIO.StringIO(types_export_view.__call__())
        archive = zipfile.ZipFile(fd, mode='r')
        filenames = archive.namelist()
        for filename in filenames:
            file_xml = archive.read(filename)

            # if this passes then GenericSetup will be able to use this XML
            try:
                parseString(file_xml)
            except ExpatError as e:
                self.fail("Parsing XML failed with ExpatError: " + e.message)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
