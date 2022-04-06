from plone.app.dexterity.textindexer.directives import SEARCHABLE_KEY
from plone.app.dexterity.textindexer.interfaces import INDEXER_NAMESPACE
from plone.app.dexterity.textindexer.interfaces import INDEXER_PREFIX
from plone.supermodel.parser import IFieldMetadataHandler
from plone.supermodel.utils import ns
from zope.interface import implementer
from zope.interface import Interface


@implementer(IFieldMetadataHandler)
class IndexerSchema:
    """Support the indexer: namespace in model definitions."""

    namespace = INDEXER_NAMESPACE
    prefix = INDEXER_PREFIX

    def _add_searchable(self, schema, value):
        tagged_value = schema.queryTaggedValue(SEARCHABLE_KEY, [])
        tagged_value.append(value)
        schema.setTaggedValue(SEARCHABLE_KEY, tagged_value)

    def read(self, fieldNode, schema, field):
        name = field.__name__
        searchable = fieldNode.get(ns("searchable", self.namespace))

        if searchable:
            value = (Interface, name, "true")
            self._add_searchable(schema, value)

    def write(self, fieldNode, schema, field):
        name = field.__name__
        searchable = schema.queryTaggedValue(SEARCHABLE_KEY, [])
        field_names = [fld[1] for fld in searchable]

        if name in field_names:
            fieldNode.set(ns("searchable", self.namespace), "true")
