# -*- coding: utf-8 -*-
from plone.app.dexterity.behaviors.metadata import ICategorization
from plone.app.dexterity.testing import DEXTERITY_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.interfaces import ConstraintNotSatisfied

import six
import unittest


class TestBasic(unittest.TestCase):

    def _makeOne(self):
        class Dummy(object):
            pass
        dummy = Dummy()
        from plone.app.dexterity.behaviors.metadata import Basic
        return Basic(dummy)

    def test_title_setter(self):
        b = self._makeOne()
        b.title = u'foo'
        self.assertEqual(u'foo', b.context.title)

    @unittest.skipUnless(six.PY2, 'Only for py2')
    def test_title_setter_rejects_bytestrings(self):
        b = self._makeOne()
        with self.assertRaises(ValueError):
            setattr(b, 'title', 'føø')

    def test_title_getter(self):
        b = self._makeOne()
        b.context.title = u'foo'
        self.assertEqual(u'foo', b.title)

    def test_description_setter(self):
        b = self._makeOne()
        b.description = u'foo'
        self.assertEqual(u'foo', b.context.description)

    @unittest.skipUnless(six.PY2, 'Only for py2')
    def test_description_setter_rejects_bytestrings(self):
        b = self._makeOne()
        with self.assertRaises(ValueError):
            setattr(b, 'description', 'føø')

    def test_description_getter(self):
        b = self._makeOne()
        b.context.description = u'foo'
        self.assertEqual(u'foo', b.description)

    def test_description_remains_newlines(self):
        b = self._makeOne()
        b.description = u'foo\r\nbar\nbaz\r'
        self.assertEqual(u'foo\r\nbar\nbaz\r', b.context.description)


class TestCategorization(unittest.TestCase):

    def _makeOne(self):
        class Dummy(object):
            pass
        dummy = Dummy()
        from plone.app.dexterity.behaviors.metadata import Categorization
        return Categorization(dummy)

    def test_subjects_setter(self):
        b = self._makeOne()
        b.subjects = (u'føø',)
        self.assertEqual((u'føø',), b.context.subject)

    def test_subjects_getter(self):
        b = self._makeOne()
        b.context.subject = (u'føø',)
        self.assertEqual((u'føø',), b.subjects)


class CategorizationIntegrationTests(unittest.TestCase):
    layer = DEXTERITY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_categorization_language(self):
        """The vocabulary of the language field in the ICategorization
        behavior should only allow to set, what was configured in
        ``plone.available_languages`` registry setting.
        """
        # set available languages
        registry = getUtility(IRegistry)
        registry['plone.available_languages'] = ['hu', 'sl']

        self.portal.invokeFactory('Folder', 'test')
        ob = self.portal.test
        cat = ICategorization(ob)

        cat.language = 'hu'
        self.assertEqual(ob.language, 'hu')

        cat.language = 'sl'
        self.assertEqual(ob.language, 'sl')

        with self.assertRaises(ConstraintNotSatisfied):
            cat.language = 'de'

        with self.assertRaises(ConstraintNotSatisfied):
            cat.language = 'en'


class TestDCFieldProperty(unittest.TestCase):

    def _makeOne(self):
        class Dummy(object):

            def addCreator(self, creator=None):
                self.creators = (creator or 'dummy_user', )

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
        b.creators = (u'føø',)
        self.assertEqual(('føø',), b.context.creators)

    def test_sequence_text_getter(self):
        b = self._makeOne()
        b.context.creators = ('føø',)
        self.assertEqual((u'føø',), b.creators)

    def test_text_setter(self):
        b = self._makeOne()
        b.rights = u'føø'
        self.assertEqual('føø', b.context.rights)

    def test_text_getter(self):
        b = self._makeOne()
        b.context.rights = 'føø'
        self.assertEqual(u'føø', b.rights)
