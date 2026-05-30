import zope.deferredimport


zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.dexterity.layout import "
    "TypeFormLayout instead.",
    TypeFormLayout="plone.app.layout.dexterity.layout:TypeFormLayout",
)
