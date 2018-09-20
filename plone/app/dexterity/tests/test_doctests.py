# -*- coding: utf-8 -*-
from plone.app.dexterity.testing import DEXTERITY_FUNCTIONAL_TESTING
from plone.testing import layered

import doctest
import re
import six
import unittest


tests = (
    'discussion.txt',
    'editing.rst',
    'namefromtitle.txt',
    'metadata.txt',
    'nextprevious.txt',
    'filename.txt',
    'schema_events.txt',
)


class Py23DocChecker(doctest.OutputChecker):
    def check_output(self, want, got, optionflags):
        if six.PY2:
            want = re.sub('zExceptions.NotFound', 'NotFound', want)
            want = re.sub('zope.interface.interfaces.ComponentLookupError', 'ComponentLookupError', want)
            want = re.sub('zope.testbrowser.browser.LinkNotFoundError', 'LinkNotFoundError', want)
            want = re.sub('AccessControl.unauthorized.Unauthorized', 'Unauthorized', want)
            got = re.sub("u'(.*?)'", "'\\1'", got)
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
