import zope.deferredimport


zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.dexterity.utils import "
    "UTF8Property instead.",
    UTF8Property="plone.app.layout.dexterity.utils:UTF8Property",
)
