import transaction
from thread import allocate_lock

from zope.component import adapts
from zope.container.interfaces import INameChooser
from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFPlone import utils as ploneutils


from plone.namedfile.file import NamedBlobImage
from plone.namedfile.file import NamedBlobFile
from plone.app.widgets.interfaces import IDXFileFactory

upload_lock = allocate_lock()

from plone.dexterity.utils import createContentInContainer


class DXFileFactory(object):
    implements(IDXFileFactory)
    adapts(IFolderish)

    def __init__(self, context):
        self.context = context

    def __call__(self, name, content_type, data):
        ctr = getToolByName(self.context, 'content_type_registry')
        type_ = ctr.findTypeName(name.lower(), '', '') or 'File'

        name = name.decode("utf8")

        chooser = INameChooser(self.context)

        # otherwise I get ZPublisher.Conflict ConflictErrors
        # when uploading multiple files
        upload_lock.acquire()

        newid = chooser.chooseName(name, self.context.aq_parent)
        try:
            transaction.begin()

            # Try to determine which kind of NamedBlob we need
            # This will suffice for standard p.a.contenttypes File/Image
            # and any other custom type that would have 'File' or 'Image' in
            # its type name
            filename = ploneutils.safe_unicode(name)
            if 'Image' in type_:
                image = NamedBlobImage(data=data,
                                       filename=filename,
                                       contentType=content_type)
                obj = createContentInContainer(
                    self.context, type_, id=newid, image=image)
            else:
                file = NamedBlobFile(data=data,
                                     filename=filename,
                                     contentType=content_type)
                obj = createContentInContainer(
                    self.context, type_, id=newid, file=file)

            obj.title = name
            obj.reindexObject()
            transaction.commit()

        finally:
            upload_lock.release()

        return obj
