"""Containing a tests suite for testing the behaviors.
"""

from plone.app.dexterity.textindexer import testing
from plone.app.dexterity.textindexer.directives import searchable
from plone.supermodel import model
from plone.testing import layered
from zope import schema

import doctest
import unittest as unittest


def test_suite():
    """Test suite testing the behaviors with a doctest from behaviors.txt"""
    suite = unittest.TestSuite()
    suite.addTests(
        [
            layered(
                doctest.DocFileSuite("behaviors.rst"),
                layer=testing.TEXT_INTEXER_INTEGRATION_TESTING,
            ),
        ]
    )
    return suite


class ITestingSchema(model.Schema):

    searchable("testing_field")
    testing_field = schema.TextLine(title="Testing field")
