import zope.deferredimport


zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.dexterity.add_type import "
    "TypeAddForm, TypeAddFormPage instead.",
    TypeAddForm="plone.app.layout.dexterity.add_type:TypeAddForm",
    TypeAddFormPage="plone.app.layout.dexterity.add_type:TypeAddFormPage",
)
