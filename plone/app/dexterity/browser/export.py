# -*- coding: utf-8 -*-
# @@types-export view for dexterity types configlet. View support for the
# "Export" button. This is done by repurposing the GS typeinfo export and
# removing unselected type information from its output.
from lxml import etree
from plone.supermodel import serializeModel
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_encode
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.GenericSetup.context import BaseContext
from Products.GenericSetup.context import TarballExportContext
from six import BytesIO
from zipfile import ZipFile

import time


class SelectiveZipExportContext(TarballExportContext):

    def __init__(self, tool, typelist, encoding=None, base_name='setup_tool'):

        BaseContext.__init__(self, tool, encoding)

        self.typelist = typelist
        self.filenames = ['types.xml']
        for tn in typelist:
            self.filenames.append('types/{0}.xml'.format(tn))

        timestamp = time.gmtime()
        self._archive_filename = (base_name + '-%4d%02d%02d%02d%02d%02d.zip'
                                  % timestamp[:6])

        self._archive_stream = BytesIO()
        self._archive = ZipFile(self._archive_stream, 'w')

    def writeDataFile(self, filename, text, content_type, subdir=None):
        if filename not in self.filenames:
            return

        if filename == 'types.xml':
            # Remove all the types except our targets.
            # Strategy: suck into ElementTree element, remove nodes,
            # convert back to text, prettify.
            root = etree.fromstring(text)
            todelete = []
            for element in root.getchildren():
                name = element.attrib['name']
                if name != 'title' and name not in self.typelist:
                    todelete.append(element)
            for element in todelete:
                root.remove(element)
            # Add a marker for ZopeSkel additions
            root.append(etree.Comment(' -*- extra stuff goes here -*- '))
            # minor prettifying
            root_str = safe_unicode(etree.tostring(root))
            text = '<?xml version="1.0"?>\n{0}'.format(root_str)
            text = text.replace('<!--', ' <!--')
            text = text.replace('-->', '-->\n')

        self._archive.writestr(filename, safe_encode(text))


class TypesExport(BrowserView):
    """Generate a types export archive for download
    """

    def __call__(self):
        RESPONSE = self.request.RESPONSE
        ps = getToolByName(self.context, 'portal_setup')

        items = self.request.selected.split(',')
        context = SelectiveZipExportContext(ps, items,
                                            base_name='dexterity_export')
        handler = ps.getExportStep(u'typeinfo')
        handler(context)

        filename = context.getArchiveFilename()

        RESPONSE.setHeader('Content-type', 'application/zip')
        RESPONSE.setHeader(
            'Content-disposition',
            'attachment; filename={0}'.format(filename)
        )

        return context.getArchive()


class ModelsExport(BrowserView):
    """Generate an archive for download of model xml files for selected
       types.
    """

    def __call__(self):
        RESPONSE = self.request.RESPONSE
        pt = getToolByName(self.context, 'portal_types')

        items = self.request.selected.split(',')

        if len(items) == 1:
            # return a single XML file

            item = items[0]
            filename = '{0}.xml'.format(item)
            text = serializeModel(pt[item].lookupModel())

            RESPONSE.setHeader('Content-type', 'application/xml')
            RESPONSE.setHeader(
                'Content-disposition',
                'attachment; filename={0}'.format(filename)
            )

            return text

        elif len(items) > 1:
            # pack multiple items into a zip file

            timestamp = time.gmtime()
            archive_filename = ('dexterity_models-%4d%02d%02d%02d%02d%02d.zip'
                                % timestamp[:6])

            archive_stream = BytesIO()
            archive = ZipFile(archive_stream, 'w')

            for item in items:
                filename = 'models/{0}.xml'.format(item)
                text = serializeModel(pt[item].lookupModel())
                archive.writestr(filename, text)

            archive.close()

            RESPONSE.setHeader('Content-type', 'application/zip')
            RESPONSE.setHeader(
                'Content-disposition',
                'attachment; filename={0}'.format(archive_filename)
            )

            return archive_stream.getvalue()

        else:
            return ''
