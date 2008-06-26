from AccessControl import getSecurityManager

from zope.component import adapts, queryUtility
from zope.schema.interfaces import IField
from z3c import form
from plone.supermodel.utils import sync_schema
from plone.supermodel import serialize_model
from plone.dexterity.interfaces import IDexteritySchema, IDexterityFTI
from plone.dexterity.utils import split_schema_name
from plone.app.dexterity.interfaces import IFieldEditingContext

class SchemaFieldFormDataManager(form.datamanager.DataManager):
    """Form data adapter that modifies Field definitions on the schema."""
    adapts(IFieldEditingContext, IField)

    def __init__(self, wrapper, field):
        self.context = wrapper
        self.schema = wrapper.schema
        self.field = wrapper.field
        
        self.metafield = field

    def get(self):
        # """See z3c.form.interfaces.IDataManager"""
        return getattr(self.field, self.metafield.__name__)

    def query(self, default=form.interfaces.NOVALUE):
        # """See z3c.form.interfaces.IDataManager"""
        try:
            return self.get()
        except AttributeError:
            return default
        return None

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

    def canAccess(self):
        """See z3c.form.interfaces.IDataManager"""
        return getSecurityManager().checkPermission('Manage schemata', self.context)
    
    def canWrite(self):
        """See z3c.form.interfaces.IDataManager"""
        return getSecurityManager().checkPermission('Manage schemata', self.context)

def serialize_schema(field_editing_context, event):
    # XXX should batch so we don't do this multiple times if multiple
    # fields were modified.  but for that, we need to annotate the request or something?

    schema = field_editing_context.schema

    # determine portal_type
    try:
        prefix, portal_type, schema_name = split_schema_name(schema.__name__)
    except ValueError:
        # not a dexterity schema
        return

    # find the FTI and model
    # (XXX Proof of concept.  Need to think through full use cases involving things
    # like customizing through the web following filesystem customization, need for
    # merging, etc.)
    fti = queryUtility(IDexterityFTI, name=portal_type)

    if fti.has_dynamic_schema:
        try:
            model = fti.lookup_model()
        except Exception, e:
            raise

        # synchronize changes to the model
        sync_schema(schema, model.lookup_schema(schema_name), overwrite=True)
        fti.model_source = serialize_model(model)
    else:
        raise "Changes to non-dynamic schemata not yet supported."
