class UTF8Property(object):

    def __init__(self, name):
        self.name = name

    def __get__(self, inst, type=None):
        value = getattr(inst.context, self.name)
        if isinstance(value, str):
            value = value.decode('utf8')
        return value

    def __set__(self, inst, value):
        if isinstance(value, unicode):
            value = value.encode('utf8')
        setattr(inst.context, self.name, value)
