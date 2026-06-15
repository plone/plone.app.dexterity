import unittest

from zope.interface import Interface
from zope import schema as zs

from plone.app.testing import setRoles, TEST_USER_ID
from plone.app.dexterity.testing import DEXTERITY_INTEGRATION_TESTING
from plone.dexterity.fti import DexterityFTI


class IWarmTestSchema(Interface):
    foo = zs.TextLine(title="foo", required=False)


def _add_dexterity_type(portal, type_id, behaviors=()):
    fti = DexterityFTI(type_id)
    fti.klass = "plone.dexterity.content.Item"
    fti.schema = "plone.app.dexterity.tests.test_warmup.IWarmTestSchema"
    fti.behaviors = tuple(behaviors)
    portal.portal_types._setObject(type_id, fti)
    return fti


class WarmSiteTest(unittest.TestCase):
    layer = DEXTERITY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_warm_site_warms_type_and_behavior(self):
        from plone.app.dexterity.warmup import warm_site
        from plone.dexterity.schema import SCHEMA_CACHE

        _add_dexterity_type(
            self.portal,
            "warmtype",
            behaviors=("plone.app.dexterity.behaviors.metadata.IBasic",),
        )
        report = warm_site(self.portal)
        # our type counted, no errors
        self.assertIn("warmtype", report.warmed_types)
        self.assertEqual(report.errors, [])
        # main schema is now cached (and is our test schema)
        self.assertIs(SCHEMA_CACHE.get("warmtype"), IWarmTestSchema)
        # behavior schemata were yielded too (>1 schema for the type)
        self.assertGreaterEqual(report.schemata, 2)


class WarmErrorIsolationTest(unittest.TestCase):
    layer = DEXTERITY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_one_failing_type_does_not_stop_the_rest(self):
        from plone.app.dexterity import warmup

        _add_dexterity_type(self.portal, "goodtype")
        _add_dexterity_type(self.portal, "badtype")

        real = warmup.iterSchemataForType

        def fake(portal_type):
            if portal_type == "badtype":
                raise RuntimeError("boom")
            return real(portal_type)

        warmup.iterSchemataForType = fake
        try:
            report = warmup.warm_site(self.portal)
        finally:
            warmup.iterSchemataForType = real

        self.assertIn("goodtype", report.warmed_types)
        self.assertNotIn("badtype", report.warmed_types)
        self.assertEqual(len(report.errors), 1)
        self.assertEqual(report.errors[0][0], "badtype")


class WarmAllTest(unittest.TestCase):
    layer = DEXTERITY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.app = self.layer["app"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_warm_all_finds_the_plone_site(self):
        from plone.app.dexterity.warmup import warm_all

        _add_dexterity_type(self.portal, "warmtype2")
        report = warm_all(self.app)
        self.assertIn("warmtype2", report.warmed_types)
