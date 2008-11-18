from zope.component import queryUtility
from plone.supermodel.utils import sync_schema
from plone.supermodel import serialize_model
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import split_schema_name

def serialize_schema(schema):
    """ Finds the FTI and model associated with a schema, and synchronizes
        the schema to the FTI model_source attribute.
    """

    # determine portal_type
    try:
        prefix, portal_type, schema_name = split_schema_name(schema.__name__)
    except ValueError:
        # not a dexterity schema
        return

    # find the FTI and model
    fti = queryUtility(IDexterityFTI, name=portal_type)
    if fti.model_source:
        model = fti.lookup_model()

        # synchronize changes to the model
        sync_schema(schema, model.schemata[schema_name], overwrite=True)
        fti.model_source = serialize_model(model)
    else:
        raise TypeError, "Changes to non-dynamic schemata not yet supported."

def serialize_schema_on_field_event(field, event):
    oldParent = getattr(event, 'oldParent', None)
    newParent = getattr(event, 'newParent', None)
    if oldParent or newParent:
        # for container events
        if oldParent:
            serialize_schema(event.oldParent)
        if newParent and newParent is not oldParent:
            serialize_schema(event.newParent)
    else:
        # we just have a field
        serialize_schema(field.interface)
        
def serialize_schema_on_schema_event(schema, event):
    serialize_schema(schema)

# XXX should batch so we don't do this multiple times if multiple
# fields were modified?
