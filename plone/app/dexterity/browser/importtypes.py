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

import os.path


class ZipFileImportContext(BaseContext):
    """ GS Import context for a ZipFile """

    implements(IImportContext)

    def __init__(self, tool, archive_bits, encoding=None, should_purge=False):
        BaseContext.__init__(self, tool, encoding)
        self._archive = ZipFile(archive_bits, 'r')
        self._should_purge = bool(should_purge)
        self.name_list = self._archive.namelist()

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
        res = set()
        for pn in self.name_list:
            dn, bn = os.path.split(pn)
            if dn == path:
                if bn not in skip:
                    res.add(bn)
            elif dn.startswith(path) and \
              (path == '' or len(dn.split('/')) == len(path.split('/')) + 1):
                res.add(dn.split('/')[-1])
        return list(res)
