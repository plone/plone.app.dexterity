# -*- coding: utf-8 -*-
""" Support for importing Dexterity types from GS zip file.
"""
# XXX: need to make exceptions more specific, shorten messages
from DateTime.DateTime import DateTime
from lxml import etree
from plone.app.dexterity import _
from plone.namedfile.field import NamedFile
from plone.z3cform.layout import wrap_form
from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.context import BaseContext
from Products.GenericSetup.interfaces import IImportContext
from six import BytesIO
from z3c.form import field
from z3c.form import form
from zipfile import BadZipfile
from zipfile import ZipFile
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import Invalid
from zope.interface import invariant

import os.path
import zope.schema


class ITypeProfileImport(Interface):
    """ Fields for a zip import form
    """

    profile_file = NamedFile(
        title=_(u'Type profiles archive file'),
        required=True,
    )

    @invariant
    def isGoodImportFile(data):
        nfile = getattr(data, 'profile_file', None)
        if nfile is None:
            # let required validator handle this
            return None
        try:
            archive = ZipFile(BytesIO(data.profile_file.data), 'r')
        except BadZipfile:
            raise Invalid(
                _(u"Error: The file submitted must be a zip archive."),
            )
        name_list = archive.namelist()
        for fname in name_list:
            if fname == 'types.xml':
                continue
            if os.path.dirname(fname) != 'types' \
               or os.path.splitext(fname)[1] != '.xml':
                raise Invalid(
                    _(u"Error: The file submitted must be a zip archive "
                      u"containing only type profile information.")
                )

        # check XML for basic integrity
        with archive.open('types.xml', 'r') as f:
            source = f.read()
            root = etree.fromstring(source)
            if root.tag != 'object':
                raise Invalid(_(u'types.xml in archive is invalid.'))

        # check against existing types; don't allow overwrites
        site = getSite()
        existing_types = getToolByName(site, 'portal_types').listContentTypes()
        for element in root.getchildren():
            if element.tag == 'object':
                attribs = element.attrib
                if not attribs['meta_type'] == 'Dexterity FTI':
                    raise Invalid(_(
                        'Types in archive must be only Dexterity types.'
                    ),)
                if attribs['name'] in existing_types:
                    msg = (
                        u'One or more types in the import archive is an '
                        u'existing type. Delete "%s" if you '
                        u'really wish to replace it.'
                    )
                    raise Invalid(_(msg, attribs['name']), )


@implementer(ITypeProfileImport)
class TypeProfileImport(object):
    form_fields = field.Fields(ITypeProfileImport)
    profile_file = zope.schema.fieldproperty.FieldProperty(
        ITypeProfileImport['profile_file']
    )

    def __init__(self, profile_file):
        self.profile_file = profile_file


class TypeProfileImportForm(form.AddForm):

    label = _(u'Import Content Types')
    description = _(
        u"You may import types by uploading a zip archive containing type "
        u"profiles. The import archive should contain a types.xml file and a "
        u"types directory containing one or more Dexterity type information "
        u"files. For a sample, create a content type and export it from the "
        u"Dexterity Content Types page."
    )
    fields = field.Fields(ITypeProfileImport)
    id = 'import-types-form'

    def create(self, data):
        return TypeProfileImport(**data)

    def add(self, profile_import):
        # initialize import context
        types_tool = getToolByName(self.context, 'portal_types')
        import_context = ZipFileImportContext(
            types_tool,
            BytesIO(profile_import.profile_file.data)
        )
        # run the profile
        setup_tool = getToolByName(self.context, 'portal_setup')
        handler = setup_tool.getImportStep(u'typeinfo')
        handler(import_context)
        self.status = _(u"Imported successfully.")

    def nextURL(self):
        url = self.context.absolute_url()
        return url


TypeProfileImportFormPage = wrap_form(TypeProfileImportForm)


@implementer(IImportContext)
class ZipFileImportContext(BaseContext):
    """ GS Import context for a ZipFile """

    def __init__(self, tool, archive_bits, encoding=None, should_purge=False):
        super(ZipFileImportContext, self).__init__(tool, encoding)
        self._archive = ZipFile(archive_bits, 'r')
        self._should_purge = bool(should_purge)
        self.name_list = self._archive.namelist()

    def readDataFile(self, filename, subdir=None):

        if subdir is not None:
            filename = '/'.join((subdir, filename))

        try:
            file = self._archive.open(filename, 'r')
        except KeyError:
            return None

        return file.read()

    def getLastModified(self, path):
        try:
            zip_info = self._archive.getinfo(path)
        except KeyError:
            return None
        return DateTime(*zip_info.date_time)

    def isDirectory(self, path):
        """ See IImportContext """

        # namelist only includes full filenames, not directories
        return path not in self.name_list

    def listDirectory(self, path, skip=[]):
        """ See IImportContext """

        # namelist contains only full path/filenames, not
        # directories. But we need to include directories.

        if path is None:
            path = ''
        path_parts = path.split('/')
        res = set()
        for pn in self.name_list:
            dn, bn = os.path.split(pn)
            dn_parts = dn.split('/')
            if dn == path:
                if bn not in skip:
                    res.add(bn)
                continue
            if dn.startswith(path) \
               and (path == '' or len(dn_parts) == len(path_parts) + 1):
                res.add(dn_parts[-1])
        return list(res)
