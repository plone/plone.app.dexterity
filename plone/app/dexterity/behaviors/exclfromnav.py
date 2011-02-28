from zope.interface import alsoProvides

from zope import interface, schema

from plone.directives import form

from plone.app.dexterity import MessageFactory as _

class IExcludeFromNavigation(form.Schema):
    """Behavior interface to exclude items from navigation.
    """

    form.fieldset('categorization', label=u"Categorization",
                  fields=['exclude_from_nav'])

    exclude_from_nav = schema.Bool(
                title=_(u'label_exclude_from_nav', default=u'Exclude from navigation'),
                description=_(u'help_exclude_from_nav', default=u'If selected, this item will not appear in the navigation tree'),
                default=False
                )

alsoProvides(IExcludeFromNavigation, form.IFormFieldProvider)
