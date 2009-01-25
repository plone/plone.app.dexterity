import unittest

from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

import plone.app.dexterity

@onsetup
def setup_product():
    zcml.load_config('meta.zcml', plone.app.dexterity)
    zcml.load_config('configure.zcml', plone.app.dexterity)

setup_product()
ptc.setupPloneSite(products=['plone.app.dexterity'])

functional_tests = (
    'editing.txt',
    'schema_events.txt',
    )

def test_suite():
    return unittest.TestSuite([
        ztc.FunctionalDocFileSuite(
            'tests/%s' % f, package='plone.app.dexterity',
            test_class=ptc.FunctionalTestCase)
        for f in functional_tests])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
