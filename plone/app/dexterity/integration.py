"""
Miscellaneous things to help integrate the Dexterity libraries into Plone.
"""

from zope.interface import implements, classImplements
from Products.CMFPlone.interfaces import INonInstallable as IPloneFactoryNonInstallable
try:
    from Products.CMFQuickInstallerTool.interfaces import INonInstallable as IQuickInstallerNonInstallable
except ImportError:
    # Plone trunk
    HAS_QI = False
else:
    HAS_QI = True

class HiddenProfiles(object):
    implements(IPloneFactoryNonInstallable)

    def getNonInstallableProfiles(self):
        """
        Prevents profiles for our widget/field dependencies from showing up in
        the profile list when creating a Plone site.
        """
        return [u'plone.formwidget.autocomplete:default',
                u'plone.formwidget.contenttree:default',
                u'plone.app.relationfield:default',
                ]

    def getNonInstallableProducts(self):
        """
        Prevents our widget/field depencies from showing up in the quick
        installer's list of installable products.
        """
        return [
            'plone.formwidget.autocomplete',
            'plone.formwidget.contenttree',
            'plone.app.relationfield',
            ]

if HAS_QI:
    classImplements(HiddenProfiles, IQuickInstallerNonInstallable)
