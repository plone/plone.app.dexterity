import zope.deferredimport


zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.dexterity.import_types import "
    "ITypeProfileImport, TypeProfileImport, TypeProfileImportForm, "
    "TypeProfileImportFormPage, ZipFileImportContext instead.",
    ITypeProfileImport="plone.app.layout.dexterity.import_types:ITypeProfileImport",
    TypeProfileImport="plone.app.layout.dexterity.import_types:TypeProfileImport",
    TypeProfileImportForm="plone.app.layout.dexterity.import_types:TypeProfileImportForm",
    TypeProfileImportFormPage="plone.app.layout.dexterity.import_types:TypeProfileImportFormPage",
    ZipFileImportContext="plone.app.layout.dexterity.import_types:ZipFileImportContext",
)
