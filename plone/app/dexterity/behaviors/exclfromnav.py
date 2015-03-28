# -*- coding: utf-8 -*-
from plone.app.dexterity import MessageFactory as _
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IExcludeFromNavigation(model.Schema):
    """Behavior interface to exclude items from navigation.
    """

    model.fieldset(
        'settings',
        label=_(u"Settings"),
        fields=['exclude_from_nav']
    )

    exclude_from_nav = schema.Bool(
        title=_(
            u'label_exclude_from_nav',
            default=u'Exclude from navigation'
        ),
        description=_(
            u'help_exclude_from_nav',
            default=u'If selected, this item will not appear in the ' +
                    u'navigation tree'
        ),
        default=False
    )

    directives.omitted('exclude_from_nav')
    directives.no_omit(IEditForm, 'exclude_from_nav')
    directives.no_omit(IAddForm, 'exclude_from_nav')
