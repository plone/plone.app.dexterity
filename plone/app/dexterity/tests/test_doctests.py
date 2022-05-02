from plone.app.dexterity.testing import DEXTERITY_FUNCTIONAL_TESTING
from plone.testing import layered

import doctest
import re
import unittest


tests = (
    "discussion.txt",
    "editing.rst",
    "namefromtitle.txt",
    "metadata.txt",
    "nextprevious.txt",
    "filename.txt",
    "schema_events.txt",
)


def test_suite():
    suite = unittest.TestSuite()
    OPTIONFLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE
    for testfile in tests:
        suite.addTest(
            layered(
                doctest.DocFileSuite(
                    testfile,
                    optionflags=OPTIONFLAGS,
                    # package='plone.app.dexterity.tests',
                ),
                layer=DEXTERITY_FUNCTIONAL_TESTING,
            )
        )
    return suite
