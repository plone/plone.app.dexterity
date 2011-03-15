import unittest
from Testing import ZopeTestCase as ztc
from plone.app.dexterity.tests.base import DexterityFunctionalTestCase

doc_tests = (
    'schema_events.txt',
    )
functional_tests = (
    'editing.txt',
    'installation.txt',
    'namefromtitle.txt',
    'metadata.txt',
    'nextprevious.txt',
    'filename.txt',
    )

def test_suite():
    return unittest.TestSuite(
        [ztc.FunctionalDocFileSuite(
            'tests/%s' % f, package='plone.app.dexterity',
            test_class=DexterityFunctionalTestCase)
            for f in functional_tests] + 
        [ztc.ZopeDocFileSuite(
            'tests/%s' % f, package='plone.app.dexterity',
            test_class=DexterityFunctionalTestCase)
            for f in doc_tests],
        )

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
