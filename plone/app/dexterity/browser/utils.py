# -*- coding: utf-8 -*-
import six


class UTF8Property(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, inst, type=None):
        value = getattr(inst.context, self.name)
        if six.PY2 and isinstance(value, six.binary_type):
            value = value.decode('utf8')
        return value

    def __set__(self, inst, value):
        if six.PY2 and isinstance(value, six.text_type):
            value = value.encode('utf8')
        setattr(inst.context, self.name, value)
