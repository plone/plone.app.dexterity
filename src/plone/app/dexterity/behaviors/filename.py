from plone.app.content.interfaces import INameFromTitle
from plone.base.utils import safe_hasattr
from plone.rfc822.interfaces import IPrimaryFieldInfo
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class INameFromFileName(Interface):
    """Marker interface to enable name from filename behavior"""


@implementer(INameFromTitle)
@adapter(INameFromFileName)
class NameFromFileName:
    def __new__(cls, context):
        info = IPrimaryFieldInfo(context, None)
        if info is None:
            return None
        filename = getattr(info.value, "filename", None)
        if not isinstance(filename, str) or not filename:
            return None
        instance = super().__new__(cls)
        instance.title = filename
        if safe_hasattr(context, "title") and not context.title:
            context.title = filename
        return instance

    def __init__(self, context):
        pass
