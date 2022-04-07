"""Contains different behaviors needed for testing.
"""
from plone.app.dexterity import textindexer
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class ISimpleBehavior(model.Schema):
    """Simple behavior containing simple text line fields."""

    textindexer.searchable("foo")
    foo = schema.TextLine(title="Foo")

    bar = schema.TextLine(title="Bar")


@provider(IFormFieldProvider)
class IListBehavior(model.Schema):
    """More advanced behavior with a list of fields."""

    textindexer.searchable("list_field")

    list_field = schema.List(title="List field", value_type=schema.TextLine())


@provider(IFormFieldProvider)
class IIntBehavior(model.Schema):
    """Basic behavior with a integer field."""

    textindexer.searchable("int_field")
    int_field = schema.Int(title="Int")


@provider(IFormFieldProvider)
class IRichTextBehavior(model.Schema):
    """Basic behavior with a rich-text field."""

    textindexer.searchable("richtext_field")
    richtext_field = RichText(
        title="Body text",
        default_mime_type="text/html",
        output_mime_type="text/x-html",
        allowed_mime_types=(
            "text/html",
            "text/plain",
        ),
        default="",
    )


@provider(IFormFieldProvider)
class IEmptyRichTextBehavior(model.Schema):
    """Behavior with a rich-text field without a default value."""

    textindexer.searchable("foo")
    foo = schema.TextLine(title="Foo")

    textindexer.searchable("empty_richtext_field")
    empty_richtext_field = RichText(
        title="Body text",
        default_mime_type="text/html",
        output_mime_type="text/x-html",
        allowed_mime_types=(
            "text/html",
            "text/plain",
        ),
    )


@provider(IFormFieldProvider)
class ITupleBehavior(model.Schema):
    """Basic behavior with a tuple field."""

    textindexer.searchable("tuple_field")
    tuple_field = schema.Tuple(
        title="Tuple",
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )


@provider(IFormFieldProvider)
class ITupleChoiceBehavior(model.Schema):
    """Basic behavior with a tuple choice field."""

    textindexer.searchable("tuple_choice_field")
    tuple_choice_field = schema.Tuple(
        title="Tuple choice",
        value_type=schema.Choice(vocabulary="plone.app.vocabularies.Keywords"),
        required=False,
        missing_value=(),
    )


@provider(IFormFieldProvider)
class IInheritedBehavior(ISimpleBehavior):
    """Behavior extending from ISimpleBehavior for testing inheritance."""


@provider(IFormFieldProvider)
class IMissingFieldBehavior(model.Schema):
    """A behavior defining a field as searchable which does not exist."""

    textindexer.searchable("foo")
    foo = schema.TextLine(title="Foo")

    textindexer.searchable("bar")
