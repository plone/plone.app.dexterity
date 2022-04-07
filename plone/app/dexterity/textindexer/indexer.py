"""Contains the indexer and some helper methods for indexing.
"""

from plone.app.dexterity.textindexer import interfaces
from plone.app.dexterity.textindexer.behavior import IDexterityTextIndexer
from plone.app.dexterity.textindexer.directives import SEARCHABLE_KEY
from plone.dexterity.utils import iterSchemata
from plone.indexer import indexer
from plone.supermodel.utils import mergedTaggedValueList
from plone.z3cform import z2
from z3c.form.field import Field
from z3c.form.interfaces import DISPLAY_MODE
from z3c.form.interfaces import IContextAware
from z3c.form.interfaces import IField
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from zope import schema
from zope.component import getAdapters
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest
from zope.interface import alsoProvides

import logging


LOGGER = logging.getLogger("plone.app.dexterity.textindexer")


class FakeView:
    """This fake view is used for enabled z3c forms z2 mode on."""

    def __init__(self, context, request):
        self.context = context
        self.request = request


@indexer(IDexterityTextIndexer)
def dynamic_searchable_text_indexer(obj):
    """Dynamic searchable text indexer."""
    # if the object does not provide a request, get one.
    # This happens when running scripts (bin/instance run script.py)
    try:
        request = obj.REQUEST
    except AttributeError:
        request = getRequest()

    # We need to make sure that we have z2 mode switched on for z3c form.
    # Since we do not really have any view to do this on, we just use
    # a fake view. For switching z2 mode on, it's only necessary that
    # there is a view.request.
    view = FakeView(obj, request)
    z2.switch_on(view, request_layer=IFormLayer)

    indexed = []

    for _storage, fields in get_searchable_contexts_and_fields(obj):
        for field in fields:

            # we need the form-field, not the schema-field we
            # already have..
            form_field = Field(field, interface=field.interface, prefix="")

            # get the widget
            try:
                widget = get_field_widget(obj, form_field, request)
            except TypeError:
                # Some times the field value is wrong, then the converter
                # failes. We should not fail, so we catch this error.
                continue

            # get the converter for this field / widget
            converter = getMultiAdapter(
                (obj, field, widget), interfaces.IDexterityTextIndexFieldConverter
            )

            # convert the field value
            value = converter.convert()

            # if no value was returned, we don't need to index
            # anything.
            if not value:
                continue

            # only accept strings
            assert isinstance(value, str), (
                "expected converted "
                + "value of IDexterityTextIndexFieldConverter to be a str"
            )

            indexed.append(value)

    # after converting all fields, run additional
    # IDynamicTextIndexExtender adapters.
    for _name, adapter in getAdapters((obj,), interfaces.IDynamicTextIndexExtender):
        extended_value = adapter()

        # if no value was returned, we don't need to index anything.
        if not extended_value:
            continue

        # only accept strings
        assert isinstance(extended_value, str), (
            "expected converted " + "value of IDynamicTextIndexExtender to be a str"
        )

        indexed.append(extended_value)

    return " ".join(indexed)


def get_field_widget(obj, field, request):
    """Returns the field widget of a field in display mode without
    touching any form.
    The `field` should be a z3c form field, not a zope schema field.
    """

    assert IField.providedBy(field), "field is not a form field"

    if field.widgetFactory.get(DISPLAY_MODE) is not None:
        factory = field.widgetFactory.get(DISPLAY_MODE)
        widget = factory(field.field, request)
    else:
        widget = getMultiAdapter((field.field, request), IFieldWidget)
    widget.name = "" + field.__name__  # prefix not needed
    widget.id = widget.name.replace(".", "-")
    widget.context = obj
    alsoProvides(widget, IContextAware)
    widget.mode = DISPLAY_MODE
    widget.ignoreRequest = True
    widget.update()
    return widget


def get_searchable_contexts_and_fields(obj):
    """Returns a generator of tuples, which contains a storage object for
    each schema (adapted `obj`) and a list of fields on this schema which
    are searchable.
    """

    for schemata in iterSchemata(obj):
        fields = []
        tagged_values = mergedTaggedValueList(schemata, SEARCHABLE_KEY)
        if not tagged_values:
            continue

        for _i, name, _v in tagged_values:
            field = schema.getFields(schemata).get(name)
            if not field:
                dottedname = ".".join((schemata.__module__, schemata.__name__))
                logging.error('%s has no field "%s"', dottedname, name)

            elif field not in fields:
                fields.append(field)

        if fields:
            storage = schemata(obj)
            yield storage, fields
