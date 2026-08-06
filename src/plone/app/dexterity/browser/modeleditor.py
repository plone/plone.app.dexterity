import zope.deferredimport


zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.dexterity.modeleditor import "
    "ModelEditorView instead.",
    NAMESPACE="plone.app.layout.dexterity.modeleditor:NAMESPACE",
    ModelEditorView="plone.app.layout.dexterity.modeleditor:ModelEditorView",
)
