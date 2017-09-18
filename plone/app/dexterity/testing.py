# -*- coding: utf-8 -*-
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class DexterityFixture(PloneSandboxLayer):
    defaultBases = (AUTOLOGIN_LIBRARY_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.dexterity
        self.loadZCML(name='meta.zcml', package=plone.app.dexterity)
        self.loadZCML(package=plone.app.dexterity)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'plone.app.dexterity:testing')


DEXTERITY_FIXTURE = DexterityFixture()

DEXTERITY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(DEXTERITY_FIXTURE,),
    name='dexterity:Integration'
)
DEXTERITY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(DEXTERITY_FIXTURE,),
    name='dexterity:Functional'
)
DEXTERITY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(DEXTERITY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='dexterity:Acceptance'
)
