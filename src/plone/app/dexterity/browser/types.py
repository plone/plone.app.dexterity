import zope.deferredimport


zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.dexterity.types import "
    "TypeEditForm, TypeEditSubForm, TypeSchemaContext, TypeSettingsAdapter, "
    "TypeStatsAdapter, TypesContext, TypesEditFormWrapper, TypesListing, "
    "TypesListingPage instead.",
    ALLOWED_FIELDS="plone.app.layout.dexterity.types:ALLOWED_FIELDS",
    TypeEditSubForm="plone.app.layout.dexterity.types:TypeEditSubForm",
    TypeEditForm="plone.app.layout.dexterity.types:TypeEditForm",
    TypesEditFormWrapper="plone.app.layout.dexterity.types:TypesEditFormWrapper",
    TypeSettingsAdapter="plone.app.layout.dexterity.types:TypeSettingsAdapter",
    TypeStatsAdapter="plone.app.layout.dexterity.types:TypeStatsAdapter",
    TypesListing="plone.app.layout.dexterity.types:TypesListing",
    TypesListingPage="plone.app.layout.dexterity.types:TypesListingPage",
    TypeSchemaContext="plone.app.layout.dexterity.types:TypeSchemaContext",
    TypesContext="plone.app.layout.dexterity.types:TypesContext",
)
