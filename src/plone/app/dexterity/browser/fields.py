import zope.deferredimport


zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.dexterity.fields import "
    "EnhancedSchemaListing, TypeFieldsPage instead.",
    EnhancedSchemaListing="plone.app.layout.dexterity.fields:EnhancedSchemaListing",
    TypeFieldsPage="plone.app.layout.dexterity.fields:TypeFieldsPage",
)
