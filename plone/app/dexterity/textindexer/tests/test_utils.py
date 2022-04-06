from plone.app.dexterity.textindexer.tests.helpers import get_searchable_fields
from plone.app.dexterity.textindexer.utils import no_longer_searchable
from plone.app.dexterity.textindexer.utils import searchable
from plone.supermodel import model
from unittest import TestCase
from zope import schema


class IExample(model.Schema):

    foo = schema.TextLine(title="foo")


class IBar(model.Schema):
    pass


class IBaz(model.Schema):
    baz = schema.TextLine(title="baz")


class TestUtils(TestCase):
    """Test utils module."""

    def test_marking_field_as_searchable(self):
        self.assertEqual(get_searchable_fields(IExample), [])
        searchable(IExample, "foo")
        self.assertEqual(get_searchable_fields(IExample), ["foo"])

    def test_break_when_field_does_not_exist(self):
        with self.assertRaises(AttributeError) as cm:
            searchable(IBar, "foo")

        self.assertEqual(
            str(cm.exception),
            "plone.app.dexterity.textindexer.tests.test_utils.IBar"
            ' has no field "foo"',
        )

    def test_no_longer_searchable_removes_flag(self):
        self.assertEqual(get_searchable_fields(IBaz), [])
        searchable(IBaz, "baz")
        self.assertEqual(get_searchable_fields(IBaz), ["baz"])
        self.assertTrue(no_longer_searchable(IBaz, "baz"))
        self.assertFalse(no_longer_searchable(IBaz, "baz"))
        self.assertEqual(get_searchable_fields(IBaz), [])

    def test_no_longer_searchable_breaks_when_field_does_not_exist(self):
        with self.assertRaises(AttributeError) as cm:
            no_longer_searchable(IBar, "foo")

        self.assertEqual(
            str(cm.exception),
            "plone.app.dexterity.textindexer.tests.test_utils.IBar"
            ' has no field "foo"',
        )
