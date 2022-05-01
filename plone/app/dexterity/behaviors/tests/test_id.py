from DateTime import DateTime
from plone.app.dexterity.testing import DEXTERITY_FUNCTIONAL_TESTING
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.zope import Browser

import transaction
import unittest


class TestShortNameBehavior(unittest.TestCase):

    layer = DEXTERITY_FUNCTIONAL_TESTING

    def setUp(self):
        # add IShortName behavior to Page
        behaviors = list(self.layer["portal"].portal_types.Document.behaviors)
        behaviors.append("plone.app.dexterity.behaviors.id.IShortName")
        self.layer["portal"].portal_types.Document.behaviors = tuple(behaviors)
        transaction.commit()

        # prepare browser
        self.browser = Browser(self.layer["app"])
        self.browser.addHeader(
            "Authorization",
            "Basic {}:{}".format(
                SITE_OWNER_NAME,
                SITE_OWNER_PASSWORD,
            ),
        )
        self.browser.open("http://nohost/plone")

    def test_add_item_w_id_specified(self):
        self.browser.getLink("Page").click()
        self.browser.getControl("Title").value = "title"
        self.browser.getControl("Short name").value = "foo"
        self.browser.getControl("Save").click()
        self.assertEqual(self.browser.url, "http://nohost/plone/foo")

        # adding another item should append a suffix
        self.browser.open("http://nohost/plone")
        self.browser.getLink("Page").click()
        self.browser.getControl("Title").value = "title"
        self.browser.getControl("Short name").value = "foo"
        self.browser.getControl("Save").click()
        self.assertEqual(self.browser.url, "http://nohost/plone/foo-1")

    def test_add_item_w_reserved_name(self):
        self.browser.getLink("Page").click()
        self.browser.getControl("Title").value = "title"
        self.browser.getControl("Short name").value = "login"  # naughty
        self.browser.getControl("Save").click()
        self.assertEqual(self.browser.url, "http://nohost/plone/login-1")

    def test_add_item_w_title_only(self):
        self.browser.getLink("Page").click()
        self.browser.getControl("Title").value = "Id from Title"
        self.browser.getControl("Save").click()
        self.assertEqual(self.browser.url, "http://nohost/plone/id-from-title")

    def test_edit_item_renames(self):
        self.browser.getLink("Page").click()
        self.browser.getControl("Title").value = "title"
        self.browser.getControl("Short name").value = "foo"
        self.browser.getControl("Save").click()
        self.browser.getLink("Edit").click()
        self.assertEqual(self.browser.getControl("Short name").value, "foo")
        # spaces should get stripped
        self.browser.getControl("Short name").value = " bar "
        self.browser.getControl("Save").click()
        self.assertEqual(self.browser.url, "http://nohost/plone/bar")

    def test_edit_item_doesnt_rename_if_id_blank(self):
        self.browser.getLink("Page").click()
        self.browser.getControl("Title").value = "title"
        self.browser.getControl("Short name").value = "foo"
        self.browser.getControl("Save").click()
        self.browser.getLink("Edit").click()
        self.browser.getControl("Short name").value = ""
        self.browser.getControl("Save").click()
        self.assertEqual(self.browser.url, "http://nohost/plone/foo")

    def test_edit_item_doesnt_rename_if_same_id(self):
        self.browser.getLink("Page").click()
        self.browser.getControl("Title").value = "title"
        self.browser.getControl("Short name").value = "foo"
        self.browser.getControl("Save").click()
        mtime = DateTime(self.layer["portal"].foo._p_mtime)
        self.browser.getLink("Edit").click()
        self.browser.getControl("Short name").value = "foo"
        self.browser.getControl("Save").click()
        self.assertEqual(self.browser.url, "http://nohost/plone/foo")
        # assert that object has not been modified
        self.assertEqual(mtime, DateTime(self.layer["portal"].foo._p_mtime))

        behaviors = list(self.layer["portal"].portal_types.Document.behaviors)
        behaviors.append("plone.app.lockingbehavior.behaviors.ILocking")

    def test_rename_works_with_lockingbehavior(self):
        """Test if the object is unlocked before renaming"""
        behaviors = list(self.layer["portal"].portal_types.Document.behaviors)
        behaviors.append("plone.app.lockingbehavior.behaviors.ILocking")
        self.layer["portal"].portal_types.Document.behaviors = tuple(behaviors)
        transaction.commit()

        self.browser.getLink("Page").click()
        self.browser.getControl("Title").value = "title"
        self.browser.getControl("Short name").value = "foo"
        self.browser.getControl("Save").click()
        self.browser.getLink("Edit").click()
        self.assertEqual(self.browser.getControl("Short name").value, "foo")
        self.browser.getControl("Short name").value = "bar"
        self.browser.getControl("Save").click()
        self.assertEqual(self.browser.url, "http://nohost/plone/bar")
