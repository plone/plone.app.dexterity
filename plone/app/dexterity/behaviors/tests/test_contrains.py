# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone.app.dexterity.behaviors.constrains import (
    ConstrainTypesBehavior,
    DISABLED,
    ACQUIRE,
)
from zope.interface import alsoProvides

import unittest


class Dummy:
    pass


class TestConstrains(unittest.TestCase):
    def test_parent_without_portal_type_with_constrain(self):
        parent = Dummy()
        alsoProvides(parent, ISelectableConstrainTypes)

        context = Dummy()
        context.__parent__ = parent
        context.portal_type = "my type"
        behavior = ConstrainTypesBehavior(context)
        self.assertEqual(DISABLED, behavior.getConstrainTypesMode())

    def test_parent_without_portal_type_not_constrained(self):
        parent = Dummy()

        context = Dummy()
        context.__parent__ = parent
        context.portal_type = "my type"
        behavior = ConstrainTypesBehavior(context)
        self.assertEqual(DISABLED, behavior.getConstrainTypesMode())

    def test_parent_same_portal_type_with_constrain(self):
        parent = Dummy()
        parent.portal_type = "my type"
        alsoProvides(parent, ISelectableConstrainTypes)

        context = Dummy()
        context.__parent__ = parent
        context.portal_type = "my type"
        behavior = ConstrainTypesBehavior(context)
        self.assertEqual(ACQUIRE, behavior.getConstrainTypesMode())

    def test_parent_same_portal_type_not_constrained(self):
        parent = Dummy()
        parent.portal_type = "my type"

        context = Dummy()
        context.__parent__ = parent
        context.portal_type = "my type"
        behavior = ConstrainTypesBehavior(context)
        self.assertEqual(DISABLED, behavior.getConstrainTypesMode())

    def test_parent_different_portal_type_with_constrain(self):
        parent = Dummy()
        parent.portal_type = "other type"
        alsoProvides(parent, ISelectableConstrainTypes)

        context = Dummy()
        context.__parent__ = parent
        context.portal_type = "my type"
        behavior = ConstrainTypesBehavior(context)
        self.assertEqual(DISABLED, behavior.getConstrainTypesMode())

    def test_parent_different_portal_type_not_constrained(self):
        parent = Dummy()
        parent.portal_type = "other type"

        context = Dummy()
        context.__parent__ = parent
        context.portal_type = "my type"
        behavior = ConstrainTypesBehavior(context)
        self.assertEqual(DISABLED, behavior.getConstrainTypesMode())

    def test_constrain_types_mode(self):
        context = Dummy()
        context.constrain_types_mode = "my mode"
        behavior = ConstrainTypesBehavior(context)
        self.assertEqual("my mode", behavior.getConstrainTypesMode())
