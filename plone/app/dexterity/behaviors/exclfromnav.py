# -*- coding: utf-8 -*-
from plone.app.dexterity import _
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


class IExcludeFromNavigationDefault(Interface):

    def __call__():
        """boolean if item is by default excluded from navigation or not.
        """


@implementer(IExcludeFromNavigationDefault)
def default_exclude_false(context):
    """provide a default adapter with the standard uses
    """
    return False


@implementer(IExcludeFromNavigationDefault)
def default_exclude_true(context):
    """provide a alternative adapter with opposite default as standard
    """
    return True


@provider(IContextAwareDefaultFactory)
def default_exclude(context):
    return IExcludeFromNavigationDefault(context)


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
            default=u'If selected, this item will not appear in the '
                    u'navigation tree'
        ),
        defaultFactory=default_exclude,
    )

    directives.omitted('exclude_from_nav')
    directives.no_omit(IEditForm, 'exclude_from_nav')
    directives.no_omit(IAddForm, 'exclude_from_nav')
