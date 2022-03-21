# -*- coding: utf-8 -*-
"""Contains different behaviors needed for testing.
"""
from collective import dexteritytextindexer
from plone.app.textfield import RichText
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class ISimpleBehavior(model.Schema):
    """Simple behavior containing simple text line fields.
    """

    dexteritytextindexer.searchable('foo')
    foo = schema.TextLine(title=u'Foo')

    bar = schema.TextLine(title=u'Bar')


@provider(IFormFieldProvider)
class IListBehavior(model.Schema):
    """More advanced behavior with a list of fields.
    """

    dexteritytextindexer.searchable('list_field')

    list_field = schema.List(
        title=u'List field',
        value_type=schema.TextLine()
    )


@provider(IFormFieldProvider)
class IIntBehavior(model.Schema):
    """Basic behavior with a integer field.
    """

    dexteritytextindexer.searchable('int_field')
    int_field = schema.Int(title=u'Int')


@provider(IFormFieldProvider)
class IRichTextBehavior(model.Schema):
    """Basic behavior with a rich-text field.
    """

    dexteritytextindexer.searchable('richtext_field')
    richtext_field = RichText(
        title=u'Body text',
        default_mime_type='text/html',
        output_mime_type='text/x-html',
        allowed_mime_types=('text/html', 'text/plain',),
        default=u'',
    )

@provider(IFormFieldProvider)
class IEmptyRichTextBehavior(model.Schema):
    """Behavior with a rich-text field without a default value.
    """

    dexteritytextindexer.searchable('foo')
    foo = schema.TextLine(title=u'Foo')

    dexteritytextindexer.searchable('empty_richtext_field')
    empty_richtext_field = RichText(
        title=u'Body text',
        default_mime_type='text/html',
        output_mime_type='text/x-html',
        allowed_mime_types=('text/html', 'text/plain',),
    )

@provider(IFormFieldProvider)
class ITupleBehavior(model.Schema):
    """Basic behavior with a tuple field.
    """

    dexteritytextindexer.searchable('tuple_field')
    tuple_field = schema.Tuple(
        title=u'Tuple',
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )


@provider(IFormFieldProvider)
class ITupleChoiceBehavior(model.Schema):
    """Basic behavior with a tuple choice field.
    """

    dexteritytextindexer.searchable('tuple_choice_field')
    tuple_choice_field = schema.Tuple(
        title=u'Tuple choice',
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.Keywords'
        ),
        required=False,
        missing_value=(),
    )


@provider(IFormFieldProvider)
class IInheritedBehavior(ISimpleBehavior):
    """Behavior extending from ISimpleBehavior for testing inheritance.
    """


@provider(IFormFieldProvider)
class IMissingFieldBehavior(model.Schema):
    """A behavior defining a field as searchable which does not exist.
    """

    dexteritytextindexer.searchable('foo')
    foo = schema.TextLine(title=u'Foo')

    dexteritytextindexer.searchable('bar')
