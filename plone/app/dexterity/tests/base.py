from Products.PloneTestCase import PloneTestCase as ptc
from plone.app.dexterity.tests.layer import DexterityLayer

ptc.setupPloneSite()

class DexterityTestCase(ptc.PloneTestCase):
    layer = DexterityLayer

class DexterityFunctionalTestCase(ptc.FunctionalTestCase):
    layer = DexterityLayer
