"""
Miscellaneous things to help integrate the Dexterity libraries into Plone.
"""

from zope.interface import implements
from Products.CMFPlone.interfaces import INonInstallable as IPloneFactoryNonInstallable

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
