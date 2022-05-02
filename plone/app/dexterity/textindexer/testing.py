"""Testing setup providing layers and fixtures
TextIndexerLayer                   basic text indexer layer
TEXT_INDEXER_FIXTURE               text indexer fixture
TEXT_INTEXER_INTEGRATION_TESTING   integration testing layer
TEXT_INDEXER_FUNCTIONAL_TESTING    functional testing layer
"""

from io import StringIO
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import logging


class TextIndexerLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = None
        self.log_handler = None

    def setUpZope(self, app, configurationContext):
        """After setting up zope, load all necessary zcml files."""
        import plone.app.dexterity.textindexer

        self.loadZCML(
            package=plone.app.dexterity.textindexer, context=configurationContext
        )
        import plone.app.dexterity.textindexer.tests

        self.loadZCML(
            package=plone.app.dexterity.textindexer.tests, context=configurationContext
        )

    def setUpPloneSite(self, portal):
        """After setting up plone, give Manager role to the test user."""
        setRoles(portal, TEST_USER_ID, ["Manager"])

    def testSetUp(self):
        super().testSetUp()
        self.log = StringIO()
        self.log_handler = logging.StreamHandler(self.log)
        logging.root.addHandler(self.log_handler)
        self["read_log"] = self.read_log

    def testTearDown(self):
        super().testTearDown()
        logging.root.removeHandler(self.log_handler)

    def read_log(self):
        self.log.seek(0)
        return self.log.read().strip()


TEXT_INDEXER_FIXTURE = TextIndexerLayer()
TEXT_INTEXER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(TEXT_INDEXER_FIXTURE,), name="plone.app.dexterity.textindexer:Integration"
)


class TextIndexerFunctionalLayer(PloneSandboxLayer):

    defaultBases = (TEXT_INDEXER_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import plone.app.dexterity

        self.loadZCML(package=plone.app.dexterity, context=configurationContext)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "plone.app.dexterity:default")


TEXT_INDEXER_FUNCTIONAL_FIXTURE = TextIndexerFunctionalLayer()

TEXT_INDEXER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(TEXT_INDEXER_FUNCTIONAL_FIXTURE,),
    name="plone.app.dexterity.textindexer:Functional",
)
