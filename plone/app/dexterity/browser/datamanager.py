import zope.interface
import zope.component
import zope.schema
from z3c import form
from plone.app.dexterity import interfaces

class SchemaFieldFormDataManager(form.datamanager.DataManager):
    """Form data adapter that modifies Field definitions on the schema."""
    zope.component.adapts(interfaces.IFieldView, zope.schema.interfaces.IField)

    def __init__(self, wrapper, field):
        self.context = wrapper
        self.schema = wrapper.schema
        self.field = wrapper.field
        
        self.metafield = field

    def get(self):
        # """See z3c.form.interfaces.IDataManager"""
        return getattr(self.field, self.metafield.__name__)

    # def query(self, default=form.interfaces.NOVALUE):
    #     # """See z3c.form.interfaces.IDataManager"""
    #     try:
    #         return self.get()
    #     except AttributeError:
    #         return default
    #     return None

    def set(self, value):
        # """See z3c.form.interfaces.IDataManager"""
        if self.metafield.readonly:
            raise TypeError("Can't set values on read-only fields "
                            "(name=%s, class=%s.%s)"
                            % (self.metafield.__name__,
                               self.field.__class__.__module__,
                               self.field.__class__.__name__))
        setattr(self.field, self.metafield.__name__, value)
        return

    # def canAccess(self):
    #     """See z3c.form.interfaces.IDataManager"""
    #     context = self.context
    #     if self.field.interface is not None:
    #         context = self.field.interface(context)
    #     if isinstance(context, Proxy):
    #         return canAccess(context, self.field.__name__)
    #     return True
    # 
    # def canWrite(self):
    #     """See z3c.form.interfaces.IDataManager"""
    #     context = self.context
    #     if self.field.interface is not None:
    #         context = self.field.interface(context)
    #     if isinstance(context, Proxy):
    #         return canWrite(context, self.field.__name__)
    #     return True
