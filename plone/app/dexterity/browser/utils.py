class UTF8Property:
    def __init__(self, name):
        self.name = name

    def __get__(self, inst, type=None):
        return getattr(inst.context, self.name)

    def __set__(self, inst, value):
        setattr(inst.context, self.name, value)
