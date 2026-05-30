import zope.deferredimport


zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.dexterity.clone_type import "
    "TypeCloneForm, TypeCloneFormPage instead.",
    TypeCloneForm="plone.app.layout.dexterity.clone_type:TypeCloneForm",
    TypeCloneFormPage="plone.app.layout.dexterity.clone_type:TypeCloneFormPage",
)
