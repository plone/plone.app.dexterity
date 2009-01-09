from persistent import Persistent

from zope.interface import implements, alsoProvides
from zope.component import adapts

from zope import schema

from zope.annotation.interfaces import IAnnotatable
from zope.annotation import factory

from plone.formwidget.relations.field import Relationships
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget

from plone.directives import form

class IRelatedItems(form.Schema):
    """Behavior interface to make a type support related items.
    """
    
    relatedItems = Relationships(
        title=u"Related Items",
        value_type=schema.Choice(vocabulary="plone.formwidget.relations.cmfcontentsearch"),
        required=False,
        )
    form.widget(relatedItems = AutocompleteMultiFieldWidget)
    form.fieldset('categorization', label=u"Categorization", fields=['relatedItems'])

alsoProvides(IRelatedItems, form.IFormFieldProvider)

class RelatedItemsAnnotations(Persistent):
    """Persistent storage for related items in annotations."""
    
    implements(IRelatedItems)
    adapts(IAnnotatable)
    
    def __init__(self):
        self.relatedItems = []

# Use the factory from zope.annotation to support persistent storage of tag data.
RelatedItems = factory(RelatedItemsAnnotations)