from plone.app.dexterity.textindexer.directives import SEARCHABLE_KEY
from plone.app.dexterity.textindexer.interfaces import INDEXER_NAMESPACE
from plone.app.dexterity.textindexer.interfaces import INDEXER_PREFIX
from plone.schemaeditor.interfaces import IFieldEditorExtender
from plone.schemaeditor.interfaces import ISchemaContext
from zope import schema
from zope.component import adapter
from zope.i18nmessageid import MessageFactory
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.interfaces import IField


_ = MessageFactory("plone.app.dexterity.textindexer")


class ISearchableTextField(Interface):
    searchable = schema.Bool(title=_("Searchable"), required=False)


@adapter(IField)
@implementer(ISearchableTextField)
class SearchableTextField:

    namespace = INDEXER_NAMESPACE
    prefix = INDEXER_PREFIX

    def __init__(self, field):
        self.field = field
        self.schema = field.interface

    def _read_searchable(self):
        tagged_value = self.schema.queryTaggedValue(SEARCHABLE_KEY, [])

        name = self.field.__name__
        value = (Interface, name, "true")

        return value in tagged_value

    def _write_searchable(self, value):
        tagged_value = self.schema.queryTaggedValue(SEARCHABLE_KEY, [])

        name = self.field.__name__
        new_value = (Interface, name, bool(value) and "true" or "false")
        old_value = (Interface, name, bool(value) and "false" or "true")

        while old_value in tagged_value:
            tagged_value.remove(old_value)

        if bool(value) and new_value not in tagged_value:
            tagged_value.append(new_value)

        self.schema.setTaggedValue(SEARCHABLE_KEY, tagged_value)

    searchable = property(_read_searchable, _write_searchable)


# ISearchableTextField could be registered directly as a named adapter
# providing IFieldEditorExtender for ISchemaContext and IField, but instead,
# we register a separate callable which returns the schema only if additional
# conditions pass:
@adapter(ISchemaContext, IField)
@implementer(IFieldEditorExtender)
def get_searchabletext_schema(schema_context, field):
    behavior = "plone.textindexer"
    fti = getattr(schema_context, "fti", None)
    if fti and behavior in getattr(fti, "behaviors", []):
        return ISearchableTextField
