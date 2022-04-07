from plone.app.dexterity.textindexer.directives import SEARCHABLE_KEY
from plone.app.dexterity.textindexer.supermodel import IndexerSchema
from plone.supermodel.utils import ns
from xml.etree import ElementTree
from zope.interface import Interface

import unittest
import zope.schema


class TestIndexerSchema(unittest.TestCase):
    """Tests for the supermodel field metadata handler."""

    namespace = "http://namespaces.plone.org/supermodel/indexer"

    def test_read(self):
        field_node = ElementTree.Element("field")
        field_node.set(ns("searchable", self.namespace), "true")

        class IDummy(Interface):
            dummy = zope.schema.TextLine(title="dummy")

        handler = IndexerSchema()
        handler.read(field_node, IDummy, IDummy["dummy"])

        self.assertEqual(
            [(Interface, "dummy", "true")], IDummy.getTaggedValue(SEARCHABLE_KEY)
        )

    def test_read_multiple(self):
        field_node1 = ElementTree.Element("field")
        field_node1.set(ns("searchable", self.namespace), "true")

        field_node2 = ElementTree.Element("field")

        field_node3 = ElementTree.Element("field")
        field_node3.set(ns("searchable", self.namespace), "true")

        class IDummy(Interface):
            dummy1 = zope.schema.TextLine(title="dummy1")
            dummy2 = zope.schema.TextLine(title="dummy2")
            dummy3 = zope.schema.TextLine(title="dummy3")

        handler = IndexerSchema()
        handler.read(field_node1, IDummy, IDummy["dummy1"])
        handler.read(field_node2, IDummy, IDummy["dummy2"])
        handler.read(field_node3, IDummy, IDummy["dummy3"])

        self.assertEqual(
            [(Interface, "dummy1", "true"), (Interface, "dummy3", "true")],
            IDummy.getTaggedValue(SEARCHABLE_KEY),
        )

    def test_read_no_data(self):
        field_node = ElementTree.Element("field")

        class IDummy(Interface):
            dummy = zope.schema.TextLine(title="dummy1")

        handler = IndexerSchema()
        handler.read(field_node, IDummy, IDummy["dummy"])

        self.assertEqual(None, IDummy.queryTaggedValue(SEARCHABLE_KEY))

    def test_write(self):
        field_node = ElementTree.Element("field")

        class IDummy(Interface):
            dummy = zope.schema.TextLine(title="dummy1")

        IDummy.setTaggedValue(SEARCHABLE_KEY, [(Interface, "dummy", "true")])

        handler = IndexerSchema()
        handler.write(field_node, IDummy, IDummy["dummy"])

        self.assertEqual("true", field_node.get(ns("searchable", self.namespace)))

    def test_write_partial(self):
        field_node = ElementTree.Element("field")
        field_node2 = ElementTree.Element("field")

        class IDummy(Interface):
            dummy = zope.schema.TextLine(title="dummy1")
            dummy2 = zope.schema.TextLine(title="dummy2")

        IDummy.setTaggedValue(SEARCHABLE_KEY, [(Interface, "dummy", "true")])

        handler = IndexerSchema()
        handler.write(field_node, IDummy, IDummy["dummy"])
        handler.write(field_node2, IDummy, IDummy["dummy2"])

        self.assertEqual("true", field_node.get(ns("searchable", self.namespace)))
        self.assertEqual(None, field_node2.get(ns("searchable", self.namespace)))

    def test_write_no_data(self):
        field_node = ElementTree.Element("field")

        class IDummy(Interface):
            dummy = zope.schema.TextLine(title="dummy1")

        handler = IndexerSchema()
        handler.write(field_node, IDummy, IDummy["dummy"])

        self.assertEqual(None, field_node.get(ns("searchable", self.namespace)))


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestIndexerSchema))
    return suite
