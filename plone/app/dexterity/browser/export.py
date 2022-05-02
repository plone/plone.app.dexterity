# @@types-export view for dexterity types configlet. View support for the
# "Export" button. This is done by repurposing the GS typeinfo export and
# removing unselected type information from its output.
from io import BytesIO
from lxml import etree
from plone.base.utils import safe_bytes
from plone.base.utils import safe_text
from plone.supermodel import serializeModel
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.GenericSetup.context import BaseContext
from Products.GenericSetup.context import TarballExportContext
from zipfile import ZipFile

import time


class SelectiveZipExportContext(TarballExportContext):
    def __init__(self, tool, typelist, encoding=None, base_name="setup_tool"):

        BaseContext.__init__(self, tool, encoding)

        self.typelist = typelist
        self.filenames = ["types.xml"]
        for tn in typelist:
            self.filenames.append(f"types/{tn}.xml")

        timestamp = time.gmtime()
        self._archive_filename = (
            base_name + "-%4d%02d%02d%02d%02d%02d.zip" % timestamp[:6]
        )

        self._archive_stream = BytesIO()
        self._archive = ZipFile(self._archive_stream, "w")

    def writeDataFile(self, filename, text, content_type, subdir=None):
        if filename not in self.filenames:
            return

        if filename == "types.xml":
            # Remove all the types except our targets.
            # Strategy: suck into ElementTree element, remove nodes,
            # convert back to text, prettify.
            root = etree.fromstring(text)
            todelete = []
            for element in root.getchildren():
                name = element.attrib["name"]
                if name != "title" and name not in self.typelist:
                    todelete.append(element)
            for element in todelete:
                root.remove(element)
            # Add a marker for ZopeSkel additions
            root.append(etree.Comment(" -*- extra stuff goes here -*- "))
            # minor prettifying
            root_str = safe_text(etree.tostring(root))
            text = f'<?xml version="1.0"?>\n{root_str}'
            text = text.replace("<!--", " <!--")
            text = text.replace("-->", "-->\n")

        self._archive.writestr(filename, safe_bytes(text))


class TypesExport(BrowserView):
    """Generate a types export archive for download"""

    def __call__(self):
        RESPONSE = self.request.RESPONSE
        ps = getToolByName(self.context, "portal_setup")

        items = self.request.selected.split(",")
        context = SelectiveZipExportContext(ps, items, base_name="dexterity_export")
        handler = ps.getExportStep("typeinfo")
        handler(context)

        filename = context.getArchiveFilename()

        RESPONSE.setHeader("Content-type", "application/zip")
        RESPONSE.setHeader("Content-disposition", f"attachment; filename={filename}")

        return context.getArchive()


class ModelsExport(BrowserView):
    """Generate an archive for download of model xml files for selected
    types.
    """

    def __call__(self):
        RESPONSE = self.request.RESPONSE
        pt = getToolByName(self.context, "portal_types")

        items = self.request.selected.split(",")

        if len(items) == 1:
            # return a single XML file

            item = items[0]
            filename = f"{item}.xml"
            text = serializeModel(pt[item].lookupModel())

            RESPONSE.setHeader("Content-type", "application/xml")
            RESPONSE.setHeader(
                "Content-disposition", f"attachment; filename={filename}"
            )

            return text

        elif len(items) > 1:
            # pack multiple items into a zip file

            timestamp = time.gmtime()
            archive_filename = (
                "dexterity_models-%4d%02d%02d%02d%02d%02d.zip" % timestamp[:6]
            )

            archive_stream = BytesIO()
            archive = ZipFile(archive_stream, "w")

            for item in items:
                filename = f"models/{item}.xml"
                text = serializeModel(pt[item].lookupModel())
                archive.writestr(filename, text)

            archive.close()

            RESPONSE.setHeader("Content-type", "application/zip")
            RESPONSE.setHeader(
                "Content-disposition",
                f"attachment; filename={archive_filename}",
            )

            return archive_stream.getvalue()

        else:
            return ""
