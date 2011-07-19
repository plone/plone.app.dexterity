# -*- coding: utf-8 -*-

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
    
    def test_title_setter_rejects_bytestrings(self):
        b = self._makeOne()
        self.assertRaises(ValueError, setattr, b, 'title', 'føø')
    
    def test_title_getter(self):
        b = self._makeOne()
        b.context.title = u'foo'
        self.assertEqual(u'foo', b.title)
    
    def test_description_setter(self):
        b = self._makeOne()
        b.description = u'foo'
        self.assertEqual(u'foo', b.context.description)

    def test_description_setter_rejects_bytestrings(self):
        b = self._makeOne()
        self.assertRaises(ValueError, setattr, b, 'description', 'føø')

    def test_description_getter(self):
        b = self._makeOne()
        b.context.description = u'foo'
        self.assertEqual(u'foo', b.description)


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
