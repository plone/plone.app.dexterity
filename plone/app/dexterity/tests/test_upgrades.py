from plone.app.dexterity.testing import DEXTERITY_INTEGRATION_TESTING

import unittest


class TestUpgrades(unittest.TestCase):

    layer = DEXTERITY_INTEGRATION_TESTING

    def test_add_missing_uuids(self):
        from plone.app.dexterity.upgrades.to2001 import add_missing_uuids
        from plone.dexterity.fti import DexterityFTI
        from plone.dexterity.utils import createContentInContainer
        from plone.uuid.interfaces import ATTRIBUTE_NAME
        from plone.uuid.interfaces import IUUID

        # create a type and item and remove its UUID
        self.layer["portal"].portal_types._setObject("page", DexterityFTI("page"))
        page = createContentInContainer(
            self.layer["portal"], "page", checkConstraints=False
        )
        setattr(page, ATTRIBUTE_NAME, None)
        self.assertTrue(IUUID(page, None) is None)
        # reindex to remove the UUID it got when the page was created
        page.reindexObject(idxs=["UID"])

        # run the migration
        add_missing_uuids(self.layer["portal"])
        # make sure we have a new UUID
        uuid = IUUID(page, None)
        self.assertTrue(uuid is not None)
        # make sure the catalog was updated
        b = self.layer["portal"].portal_catalog.unrestrictedSearchResults(
            portal_type="page"
        )[0]
        self.assertTrue(b.UID == uuid)

        # make sure running the upgrade again doesn't change the UUID
        add_missing_uuids(self.layer["portal"])
        uuid2 = IUUID(page, None)
        self.assertEqual(uuid2, uuid, "Upgrade changes existing uuids.")

    def test_upgrade_2003(self):
        from plone.app.dexterity.upgrades.to2003 import fix_installed_products
        from Products.CMFCore.utils import getToolByName

        try:
            from Products.CMFQuickInstallerTool.InstalledProduct import InstalledProduct
        except ImportError:
            # nothing to test
            return
        qi = getToolByName(self.layer["portal"], "portal_quickinstaller", None)
        if qi is None:
            # nothing to test
            return
        ip = InstalledProduct("foo")
        ip.utilities = [("zope.intid.interfaces.IIntIds", "")]
        qi._setObject("foo", ip)

        fix_installed_products(self.layer["portal"])

        self.assertEqual([], ip.utilities)
