import zope.deferredimport


zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.dexterity.folder_listing import "
    "FolderView instead.",
    FolderView="plone.app.layout.dexterity.folder_listing:FolderView",
)
