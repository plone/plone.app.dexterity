from zope.component import queryUtility
from plone.supermodel.utils import syncSchema
from plone.supermodel import serializeModel
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import splitSchemaName


def serializeSchemaContext(schema_context, event=None):
    """ Serializes the schema associated with a schema context.
    
    The serialized schema is saved to the model_source property of the FTI
    associated with the schema context.
    """
    # find the FTI and model
    fti = schema_context.fti
    schemaName = schema_context.schemaName
    schema = schema_context.schema
    model = fti.lookupModel()

    # synchronize changes to the model
    syncSchema(schema, model.schemata[schemaName], overwrite=True)
    fti.model_source = serializeModel(model)


def serializeSchema(schema):
    """ Finds the FTI and model associated with a schema, and synchronizes
        the schema to the FTI model_source attribute.
        
        This method only works for schemas that were created from an FTI's
        model_source property
        
        BBB - deprecated
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
