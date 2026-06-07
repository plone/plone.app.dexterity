from plone.app.dexterity.behaviors.metadata import ICategorization
from plone.app.dexterity.testing import DEXTERITY_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.interfaces import ConstraintNotSatisfied

import unittest


class TestBasic(unittest.TestCase):
    def _makeOne(self):
        class Dummy:
            pass

        dummy = Dummy()
        from plone.app.dexterity.behaviors.metadata import Basic

        return Basic(dummy)

    def test_title_setter(self):
        b = self._makeOne()
        b.title = "foo"
        self.assertEqual("foo", b.context.title)

    def test_title_getter(self):
        b = self._makeOne()
        b.context.title = "foo"
        self.assertEqual("foo", b.title)

    def test_description_setter(self):
        b = self._makeOne()
        b.description = "foo"
        self.assertEqual("foo", b.context.description)

    def test_description_getter(self):
        b = self._makeOne()
        b.context.description = "foo"
        self.assertEqual("foo", b.description)

    def test_description_remains_newlines(self):
        b = self._makeOne()
        b.description = "foo\r\nbar\nbaz\r"
        self.assertEqual("foo\r\nbar\nbaz\r", b.context.description)


class TestIBasicMaxLength(unittest.TestCase):
    def test_title_max_length(self):
        from plone.app.dexterity.behaviors.metadata import IBasic

        self.assertEqual(IBasic["title"].max_length, 1024)

    def test_description_max_length(self):
        from plone.app.dexterity.behaviors.metadata import IBasic

        self.assertEqual(IBasic["description"].max_length, 10000)

    def test_title_too_long_fails_validation(self):
        from plone.app.dexterity.behaviors.metadata import IBasic
        from zope.schema import ValidationError

        with self.assertRaises(ValidationError):
            IBasic["title"].validate("x" * 1025)

    def test_description_too_long_fails_validation(self):
        from plone.app.dexterity.behaviors.metadata import IBasic
        from zope.schema import ValidationError

        with self.assertRaises(ValidationError):
            IBasic["description"].validate("x" * 10001)

    def test_title_at_max_length_passes(self):
        from plone.app.dexterity.behaviors.metadata import IBasic

        IBasic["title"].validate("x" * 1024)  # must not raise

    def test_description_at_max_length_passes(self):
        from plone.app.dexterity.behaviors.metadata import IBasic

        IBasic["description"].validate("x" * 10000)  # must not raise

    def test_title_max_length_can_be_overridden(self):
        from plone.app.dexterity.behaviors.metadata import IBasic

        original = IBasic["title"].max_length
        try:
            IBasic["title"].max_length = 5000
            IBasic["title"].validate("x" * 5000)  # must not raise
        finally:
            IBasic["title"].max_length = original


class TestCategorization(unittest.TestCase):
    def _makeOne(self):
        class Dummy:
            pass

        dummy = Dummy()
        from plone.app.dexterity.behaviors.metadata import Categorization

        return Categorization(dummy)

    def test_subjects_setter(self):
        b = self._makeOne()
        b.subjects = ("føø",)
        self.assertEqual(("føø",), b.context.subject)

    def test_subjects_getter(self):
        b = self._makeOne()
        b.context.subject = ("føø",)
        self.assertEqual(("føø",), b.subjects)


class CategorizationIntegrationTests(unittest.TestCase):
    layer = DEXTERITY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_categorization_language(self):
        """The vocabulary of the language field in the ICategorization
        behavior should only allow to set, what was configured in
        ``plone.available_languages`` registry setting.
        """
        # set available languages
        registry = getUtility(IRegistry)
        registry["plone.available_languages"] = ["hu", "sl"]

        self.portal.invokeFactory("Folder", "test")
        ob = self.portal.test
        cat = ICategorization(ob)

        cat.language = "hu"
        self.assertEqual(ob.language, "hu")

        cat.language = "sl"
        self.assertEqual(ob.language, "sl")

        with self.assertRaises(ConstraintNotSatisfied):
            cat.language = "de"

        with self.assertRaises(ConstraintNotSatisfied):
            cat.language = "en"


class TestDCFieldProperty(unittest.TestCase):
    def _makeOne(self):
        class Dummy:
            def addCreator(self, creator=None):
                self.creators = (creator or "dummy_user",)

            def setRights(self, rights):
                self.rights = rights

            def Rights(self):
                return self.rights

            def setCreators(self, creators):
                self.creators = creators

            def listCreators(self):
                return self.creators

        dummy = Dummy()
        from plone.app.dexterity.behaviors.metadata import DublinCore

        return DublinCore(dummy)

    def test_sequence_text_setter(self):
        b = self._makeOne()
        b.creators = ("føø",)
        self.assertEqual(("føø",), b.context.creators)

    def test_sequence_text_getter(self):
        b = self._makeOne()
        b.context.creators = ("føø",)
        self.assertEqual(("føø",), b.creators)

    def test_text_setter(self):
        b = self._makeOne()
        b.rights = "føø"
        self.assertEqual("føø", b.context.rights)

    def test_text_getter(self):
        b = self._makeOne()
        b.context.rights = "føø"
        self.assertEqual("føø", b.rights)
