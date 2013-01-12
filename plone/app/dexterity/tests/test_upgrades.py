from Products.PloneTestCase import PloneTestCase as ptc


class UpgradesTestCase(ptc.PloneTestCase):

    def test_upgrade_7(self):
        qi = self.portal.portal_quickinstaller
        from Products.CMFQuickInstallerTool.InstalledProduct import InstalledProduct
        ip = InstalledProduct('foo')
        ip.utilities = [('zope.intid.interfaces.IIntIds', '')]
        qi._setObject('foo', ip)

        from plone.app.dexterity.upgrades.to7 import fix_installed_products
        fix_installed_products(self.portal)

        self.assertEqual([], ip.utilities)
