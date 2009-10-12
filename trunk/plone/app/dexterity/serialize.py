from zope.component import queryUtility
from plone.supermodel.utils import syncSchema
from plone.supermodel import serializeModel
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import splitSchemaName

def serializeSchema(schema):
    """ Finds the FTI and model associated with a schema, and synchronizes
        the schema to the FTI model_source attribute.
    """

    # determine portal_type
    try:
        prefix, portal_type, schemaName = splitSchemaName(schema.__name__)
    except ValueError:
        # not a dexterity schema
        return

    # find the FTI and model
    fti = queryUtility(IDexterityFTI, name=portal_type)
    if fti.model_source:
        model = fti.lookupModel()

        # synchronize changes to the model
        syncSchema(schema, model.schemata[schemaName], overwrite=True)
        fti.model_source = serializeModel(model)
    else:
        raise TypeError, "Changes to non-dynamic schemata not yet supported."

def serializeSchemaOnFieldEvent(field, event):
    oldParent = getattr(event, 'oldParent', None)
    newParent = getattr(event, 'newParent', None)
    if oldParent or newParent:
        # for container events
        if oldParent:
            serializeSchema(event.oldParent)
        if newParent and newParent is not oldParent:
            serializeSchema(event.newParent)
    else:
        # we just have a field
        serializeSchema(field.interface)
        
def serializeSchemaOnSchemaEvent(schema, event):
    serializeSchema(schema)

# XXX should batch so we don't do this multiple times if multiple
# fields were modified?
