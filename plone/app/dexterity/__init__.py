# -*- coding: utf-8 -*-
from zope.i18nmessageid import MessageFactory as ZMessageFactory
import warnings

_ = ZMessageFactory('plone')


def MessageFactory(*args, **kwargs):
    # BBB Remove in Plone 5.2
    warnings.warn(
        "Name clash, now use '_' as usal. Will be removed in Plone 5.2",
        DeprecationWarning)
    return _(*args, **kwargs)
