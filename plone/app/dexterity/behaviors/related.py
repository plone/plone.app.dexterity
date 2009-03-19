from zope.component import adapts
from zope.interface import alsoProvides, implements

from z3c.relationfield.schema import RelationChoice, RelationList

from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.dexterity.interfaces import IDexterityContent
from plone.directives import form

class IRelatedItems(form.Schema):
    """Behavior interface to make a type support related items.
    """
    
    form.fieldset('categorization', label=u"Categorization", fields=['relatedItems'])
    
    relatedItems = RelationList(
        title=u"Related Items",
        default=[],
        value_type=RelationChoice(title=u"Related",
                      source=ObjPathSourceBinder()),
        required=False,
        )

alsoProvides(IRelatedItems, form.IFormFieldProvider)

class RelatedItemsFactory(object):
    """An adapter for storing related items directly on the object"""
    adapts(IDexterityContent)
    implements(IRelatedItems)
    field_name = 'relatedItems'

    def __init__(self, context):
        self.context = context

    # We can't use a FieldProperty because vocabulary validation won't work
    # the vocabulary has content and we store RelationValues
    def _get_related(self):
        return getattr(self.context, self.field_name)
    def _set_related(self, value):
        setattr(self.context, self.field_name, value)
    relatedItems = property(_get_related, _set_related)
