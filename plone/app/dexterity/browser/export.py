import time
from StringIO import StringIO
from tarfile import DIRTYPE
from tarfile import TarInfo

from Products.CMFCore.utils import getToolByName

from Products.Five.browser import BrowserView

from Products.GenericSetup.context import TarballExportContext


class SelectiveTarballExportContext(TarballExportContext):

    def __init__( self, tool, typelist, encoding=None ):
        super(SelectiveTarballExportContext, self).__init__( tool, encoding )
        self.filenames = ['types.xml']
        for tn in typelist:
            self.filenames.append('types/%s.xml' % tn)

    def writeDataFile( self, filename, text, content_type, subdir=None ):
        if subdir is not None:
            filename = '/'.join( ( subdir, filename ) )

        if filename not in self.filenames:
            return

        if filename == 'types.xml':
            pass
            # TODO - trim this

        parents = filename.split('/')[:-1]
        while parents:
            path = '/'.join(parents) + '/'
            if path not in self._archive.getnames():
                info = TarInfo(path)
                info.type = DIRTYPE
                info.mode = 0755
                info.mtime = time.time()
                self._archive.addfile(info)
            parents.pop()

        stream = StringIO( text )
        info = TarInfo( filename )
        info.size = len( text )
        info.mtime = time.time()
        self._archive.addfile( info, stream )


class TypesExport(BrowserView):
    """Generate a types export archive for download
    """

    def __call__(self):
        RESPONSE = self.request.RESPONSE
        ps = getToolByName(self.context, 'portal_setup')

        items = self.request.selected.split(',')
        context = SelectiveTarballExportContext(ps, items)
        handler = ps.getExportStep(u'typeinfo')
        message = handler(context)

        filename = context.getArchiveFilename()
        filename = filename.replace('setup_tool', 'dexterity_export')

        RESPONSE.setHeader('Content-type', 'application/x-gzip')
        RESPONSE.setHeader('Content-disposition',
          'attachment; filename=%s' % filename)

        return context.getArchive()
