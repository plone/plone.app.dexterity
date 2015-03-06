# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_hasattr
from plone.app.content.interfaces import INameFromTitle
from plone.rfc822.interfaces import IPrimaryFieldInfo
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer


class INameFromFileName(Interface):
    """Marker interface to enable name from filename behavior"""


@implementer(INameFromTitle)
@adapter(INameFromFileName)
class NameFromFileName(object):

    def __new__(cls, context):
        info = IPrimaryFieldInfo(context, None)
        if info is None:
            return None
        filename = getattr(info.value, 'filename', None)
        if not isinstance(filename, basestring) or not filename:
            return None
        instance = super(NameFromFileName, cls).__new__(cls)
        instance.title = filename
        if safe_hasattr(context, 'title') and not context.title:
            context.title = filename
        return instance

    def __init__(self, context):
        pass
