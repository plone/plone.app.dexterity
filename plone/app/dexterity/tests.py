import unittest

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

import plone.app.dexterity

ptc.setupPloneSite(extension_profiles=['plone.app.dexterity:default'])

class DexterityLayer(PloneSite):
    
    @classmethod
    def setUp(cls):
        zcml.load_config('meta.zcml', plone.app.dexterity)
        zcml.load_config('configure.zcml', plone.app.dexterity)

    @classmethod
    def tearDown(cls):
        pass

class DexterityTestCase(ptc.PloneTestCase):
    layer = DexterityLayer

class DexterityFunctionalTestCase(ptc.FunctionalTestCase):
    layer = DexterityLayer

doc_tests = (
    'schema_events.txt',
    )
functional_tests = (
    'editing.txt',
    'installation.txt',
    'namefromtitle.txt',
    'metadata.txt',    
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
