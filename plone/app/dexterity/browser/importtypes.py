# -*- coding: utf-8 -*-
""" Support for importing Dexterity types from GS zip file.
"""

from DateTime.DateTime import DateTime
from lxml import etree
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.GenericSetup.context import BaseContext
from Products.GenericSetup.context import TarballImportContext
from Products.GenericSetup.interfaces import IImportContext
from StringIO import StringIO
from zipfile import ZipFile
from zope.interface import implements


class ZipFileImportContext(BaseContext):
    """ GS Import context for a ZipFile """

    implements(IImportContext)

    def __init__(self, tool, archive_bits, encoding=None, should_purge=False):
        BaseContext.__init__(self, tool, encoding)
        self._archive = ZipFile(archive_bits, 'r')
        self._should_purge = bool(should_purge)

    def readDataFile(self, filename, subdir=None):

        if subdir is not None:
            filename = '/'.join((subdir, filename))

        try:
            file = self._archive.open(filename, 'rU')
        except KeyError:
            return None

        return file.read()

    def getLastModified(self, path):
        try:
            zip_info = self._archive.getinfo(path)
        except KeyError:
            return None
        return DateTime(*zip_info.date_time)
