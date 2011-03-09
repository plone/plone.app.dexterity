from z3c.form.interfaces import IEditForm, IAddForm
from zope.interface import alsoProvides
from zope import interface, schema
from plone.directives import form
from plone.app.dexterity import MessageFactory as _

class IExcludeFromNavigation(form.Schema):
    """Behavior interface to exclude items from navigation.
    """

    form.fieldset('settings', label=u"Settings",
                  fields=['exclude_from_nav'])

    exclude_from_nav = schema.Bool(
                title=_(u'label_exclude_from_nav', default=u'Exclude from navigation'),
                description=_(u'help_exclude_from_nav', default=u'If selected, this item will not appear in the navigation tree'),
                default=False
                )

    form.omitted('exclude_from_nav')
    form.no_omit(IEditForm, 'exclude_from_nav')
    form.no_omit(IAddForm, 'exclude_from_nav')

alsoProvides(IExcludeFromNavigation, form.IFormFieldProvider)
