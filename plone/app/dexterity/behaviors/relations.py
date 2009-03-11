from zope.interface import alsoProvides

from zope import schema

from plone.formwidget.relations.field import Relationships
from plone.formwidget.contenttree import MultiContentTreeFieldWidget, ObjPathSourceBinder

from plone.directives import form

class IRelatedItems(form.Schema):
    """Behavior interface to make a type support related items.
    """
    
    relatedItems = Relationships(
        title=u"Related Items",
        value_type=schema.Choice(source=ObjPathSourceBinder()),
        required=False,
        )
    form.widget(relatedItems = MultiContentTreeFieldWidget)
    form.fieldset('categorization', label=u"Categorization", fields=['relatedItems'])

alsoProvides(IRelatedItems, form.IFormFieldProvider)
