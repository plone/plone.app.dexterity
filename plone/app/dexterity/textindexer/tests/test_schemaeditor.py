from plone import api
from plone.app.dexterity.textindexer.testing import TEXT_INDEXER_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.dexterity.fti import DexterityFTI
from plone.testing.z2 import Browser

import transaction
import unittest


class TestSchemaEditor(unittest.TestCase):

    layer = TEXT_INDEXER_FUNCTIONAL_TESTING

    def setUp(self):
        portal_types = api.portal.get_tool("portal_types")

        # Define new portal type without behavior
        fti = DexterityFTI("without_behavior", title="Without Behavior")
        fti.behaviors = ("plone.basic",)
        fti.model_source = """\
<model xmlns="http://namespaces.plone.org/supermodel/schema">
<schema>
<field name="custom" type="zope.schema.TextLine">
  <description />
  <required>False</required>
  <title>Custom field</title>
</field>
</schema>
</model>"""
        portal_types._setObject("without_behavior", fti)

        # Define new portal type with behavior
        fti = DexterityFTI("with_behavior", title="With Behavior")
        fti.behaviors = (
            "plone.basic",
            "plone.textindexer",
        )
        fti.model_source = """\
<model xmlns="http://namespaces.plone.org/supermodel/schema">
<schema>
<field name="custom" type="zope.schema.TextLine">
  <description />
  <required>False</required>
  <title>Custom field</title>
</field>
</schema>
</model>"""
        portal_types._setObject("with_behavior", fti)

        setRoles(self.layer["portal"], TEST_USER_ID, ["Manager"])
        transaction.commit()

        self.browser = Browser(self.layer["app"])
        self.browser.addHeader(
            "Authorization", f"Basic {TEST_USER_NAME}:{TEST_USER_PASSWORD}"
        )
        self.portal_url = self.layer["portal"].absolute_url()

    def test_searchable_field_is_not_visible_without_behavior(self):
        self.browser.open(self.portal_url + "/dexterity-types/without_behavior/custom")
        self.assertRaises(LookupError, self.browser.getControl, "Searchable")

    def test_searchable_field_is_visible_with_behavior(self):
        self.browser.open(self.portal_url + "/dexterity-types/with_behavior/custom")
        control = self.browser.getControl("Searchable")
        self.assertEqual(control.control.type, "checkbox")

    def test_searchable_field_is_disabled_by_default(self):
        self.browser.open(self.portal_url + "/dexterity-types/with_behavior/custom")
        self.assertFalse(self.browser.getControl("Searchable").selected)

    def test_searchable_field_change_is_saved(self):
        portal_types = api.portal.get_tool("portal_types")
        fti = portal_types["with_behavior"]
        self.assertNotIn('indexer:searchable="true"', fti.model_source)

        self.browser.open(self.portal_url + "/dexterity-types/with_behavior/custom")
        self.browser.getControl("Searchable").click()
        self.browser.getControl("Save").click()

        self.browser.open(self.portal_url + "/dexterity-types/with_behavior/custom")
        self.assertTrue(self.browser.getControl("Searchable").selected)

        fti._p_jar.sync()
        self.assertIn('indexer:searchable="true"', fti.model_source)

        self.browser.getControl("Searchable").click()
        self.browser.getControl("Save").click()

        self.browser.open(self.portal_url + "/dexterity-types/with_behavior/custom")
        self.assertFalse(self.browser.getControl("Searchable").selected)

        fti._p_jar.sync()
        self.assertNotIn('indexer:searchable="true"', fti.model_source)
