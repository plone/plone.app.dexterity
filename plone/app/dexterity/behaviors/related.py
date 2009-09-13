from zope.interface import alsoProvides

from z3c.relationfield.schema import RelationChoice, RelationList

from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.directives import form

from plone.app.dexterity import MessageFactory as _

class IRelatedItems(form.Schema):
    """Behavior interface to make a type support related items.
    """

    form.fieldset('categorization', label=u"Categorization",
                  fields=['relatedItems'])

    relatedItems = RelationList(
        title=_(u'label_related_items', default=u'Related Items'),
        default=[],
        value_type=RelationChoice(title=u"Related",
                      source=ObjPathSourceBinder()),
        required=False,
        )

alsoProvides(IRelatedItems, form.IFormFieldProvider)
