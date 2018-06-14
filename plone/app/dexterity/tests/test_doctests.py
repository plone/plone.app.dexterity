# -*- coding: utf-8 -*-
from plone.app.dexterity.testing import DEXTERITY_FUNCTIONAL_TESTING
from plone.testing import layered

import doctest
import unittest
import re
import six

tests = (
    'discussion.txt',
    'editing.txt',
    'namefromtitle.txt',
    'metadata.txt',
    'nextprevious.txt',
    'filename.txt',
    'schema_events.txt',
)


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            got = re.sub('zExceptions.NotFound', 'NotFound', got)
            got = re.sub('zope.interface.interfaces.ComponentLookupError', 'ComponentLookupError', got)
            got = re.sub('zope.testbrowser.browser.LinkNotFoundError', 'LinkNotFoundError', got)
            got = re.sub("u'(.*?)'", "'\\1'", want)
            want = re.sub("b'(.*?)'", "'\\1'", want)
        return doctest.OutputChecker.check_output(self, want, got, optionflags)


def test_suite():
    suite = unittest.TestSuite()
    OPTIONFLAGS = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
    for testfile in tests:
        suite.addTest(
            layered(
                doctest.DocFileSuite(
                    testfile,
                    optionflags=OPTIONFLAGS,
                    # package='plone.app.dexterity.tests',
                    checker=Py23DocChecker(),
                ),
                layer=DEXTERITY_FUNCTIONAL_TESTING
            )
        )
    return suite
