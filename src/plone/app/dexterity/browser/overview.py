import zope.deferredimport


zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.dexterity.overview import "
    "TypeOverviewForm, TypeOverviewPage instead.",
    TypeOverviewForm="plone.app.layout.dexterity.overview:TypeOverviewForm",
    TypeOverviewPage="plone.app.layout.dexterity.overview:TypeOverviewPage",
)
