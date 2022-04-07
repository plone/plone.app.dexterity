from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.dexterity.textindexer.tests.helpers import get_searchable_fields
from unittest import TestCase


class TestBasicBehaviorIsSearchable(TestCase):
    def test_title_is_searchable(self):
        self.assertIn("title", get_searchable_fields(IBasic))

    def test_description_is_searchable(self):
        self.assertIn("description", get_searchable_fields(IBasic))
