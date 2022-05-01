from _thread import allocate_lock
from plone.app.dexterity.interfaces import IDXFileFactory
from plone.base.utils import safe_text
from plone.dexterity.utils import createContentInContainer
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFCore.utils import getToolByName
from zope.component import adapter
from zope.container.interfaces import INameChooser
from zope.interface import implementer


upload_lock = allocate_lock()


@adapter(IFolderish)
@implementer(IDXFileFactory)
class DXFileFactory:
    def __init__(self, context):
        self.context = context

    def __call__(self, name, content_type, data):
        ctr = getToolByName(self.context, "content_type_registry")
        type_ = ctr.findTypeName(name.lower(), content_type, data) or "File"

        name = safe_text(name)

        chooser = INameChooser(self.context)

        # otherwise I get ZPublisher.Conflict ConflictErrors
        # when uploading multiple files
        upload_lock.acquire()
        try:
            newid = chooser.chooseName(name, self.context.aq_parent)
            # Try to determine which kind of NamedBlob we need
            # This will suffice for standard p.a.contenttypes File/Image
            # and any other custom type that would have 'File' or 'Image' in
            # its type name
            # XXX heuristics are harmful behavior, here a better implemenation
            #     is needed
            filename = name
            if "Image" in type_:
                image = NamedBlobImage(
                    data=data, filename=filename, contentType=content_type
                )
                obj = createContentInContainer(
                    self.context, type_, id=newid, image=image
                )
            else:
                file = NamedBlobFile(
                    data=data, filename=filename, contentType=content_type
                )
                obj = createContentInContainer(self.context, type_, id=newid, file=file)

            obj.title = name
            obj.reindexObject()

        finally:
            upload_lock.release()

        return obj
