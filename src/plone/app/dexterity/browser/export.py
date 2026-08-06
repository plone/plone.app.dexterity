import zope.deferredimport


zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.dexterity.export import "
    "ModelsExport, SelectiveZipExportContext, TypesExport instead.",
    SelectiveZipExportContext="plone.app.layout.dexterity.export:SelectiveZipExportContext",
    TypesExport="plone.app.layout.dexterity.export:TypesExport",
    ModelsExport="plone.app.layout.dexterity.export:ModelsExport",
)
