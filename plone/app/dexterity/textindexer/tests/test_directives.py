# -*- coding: utf-8 -*-
from collective.dexteritytextindexer.directives import searchable
from collective.dexteritytextindexer.directives import SEARCHABLE_KEY
from plone.supermodel import model
from plone.supermodel.utils import mergedTaggedValueList
from zope import schema
from zope.interface import Interface

import unittest
import zope.component.testing


class TestDirectives(unittest.TestCase):

    def tearDown(self):
        """Tear down the testing setup.
        """
        zope.component.testing.tearDown()

    def test_schema_directives_store_tagged_values(self):
        """Test, if the schema directive values are stored as tagged
        values.
        """

        class IDummy(model.Schema):
            """Dummy schema class.
            """
            searchable('foo')
            foo = schema.TextLine(title=u'Foo')

        self.assertEqual(
            [(Interface, 'foo', 'true')],
            mergedTaggedValueList(IDummy, SEARCHABLE_KEY))

    def test_inherited_schema_still_has_tagged_value(self):
        """An inherited schema should still have the tagged value information
        inherited from its superclass.
        """

        class IFoo(model.Schema):
            """Class with a searchable field
            """
            searchable('baz')
            baz = schema.TextLine(title=u'baz')

        class IBar(IFoo):
            """Schema class which inherits a field from IFoo.
            """

        self.assertEqual(
            [(Interface, 'baz', 'true')],
            mergedTaggedValueList(IFoo, SEARCHABLE_KEY))
        self.assertEqual(
            [(Interface, 'baz', 'true')],
            mergedTaggedValueList(IBar, SEARCHABLE_KEY))
