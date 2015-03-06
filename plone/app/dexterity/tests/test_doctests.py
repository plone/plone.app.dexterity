# -*- coding: utf-8 -*-
from plone.app.dexterity.testing import DEXTERITY_FUNCTIONAL_TESTING
from plone.testing import layered
import doctest
import unittest


tests = (
    'discussion.txt',
    'editing.txt',
    'namefromtitle.txt',
    'metadata.txt',
    'nextprevious.txt',
    'filename.txt',
    'schema_events.txt',
)


def test_suite():
    return unittest.TestSuite(
        [layered(doctest.DocFileSuite(f, optionflags=doctest.ELLIPSIS),
                 layer=DEXTERITY_FUNCTIONAL_TESTING)
            for f in tests]
    )
