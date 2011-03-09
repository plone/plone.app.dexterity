from AccessControl import getSecurityManager
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IContentish
from plone.app.dexterity import MessageFactory as _
from plone.app.layout.nextprevious.interfaces import INextPreviousProvider
from plone.directives import form
from z3c.form import widget
from z3c.form.interfaces import IEditForm
from z3c.form.interfaces import IAddForm
from zope import schema
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.interface import implements
from zope.component import adapts

class INextPreviousEnabled(Interface):
    """Behavior interface to enable next previous navigation for all items of a type.
    """    

class INextPreviousToggle(form.Schema):
    """Behavior interface to enable next previous navigation per item.
    """

    form.fieldset('settings', label=u"Settings",
                  fields=['nextPreviousEnabled'])

    nextPreviousEnabled = schema.Bool(
                title=_(u'label_nextprevious', default=u'Enable next previous navigation'),
                description=_(u'help_nextprevious', default=u'This enables next/previous widget on content items contained in this folder.'),
                default=False
                )

    form.omitted('nextPreviousEnabled')
    form.no_omit(IEditForm, 'nextPreviousEnabled')
    form.no_omit(IAddForm, 'nextPreviousEnabled')

alsoProvides(INextPreviousToggle, form.IFormFieldProvider)


def getNextPreviousParentValue(adapter):
    context = adapter.context
    nextprevious = INextPreviousProvider(context, None)
    if nextprevious is None:
        return False
    return nextprevious.enabled

DefaultNextPreviousEnabled = widget.ComputedWidgetAttribute(
    getNextPreviousParentValue,
    field=INextPreviousToggle['nextPreviousEnabled'],
    )

# This is taken from plone.app.folder
class NextPreviousBase(object):
    """ adapter for acting as a next/previous provider """

    def __init__(self, context):
        self.context = context
        props = getToolByName(context, 'portal_properties').site_properties
        self.vat = props.getProperty('typesUseViewActionInListings', ())
        self.security = getSecurityManager()
        order = context.getOrdering()
        if not isinstance(order, list):
            order = order.idsInOrder()
        if not isinstance(order, list):
            order = None
        self.order = order

    def getNextItem(self, obj):
        """ return info about the next item in the container """
        if not self.order:
            return None
        pos = self.context.getObjectPosition(obj.getId())
        for oid in self.order[pos+1:]:
            data = self.getData(self.context[oid])
            if data:
                return data

    def getPreviousItem(self, obj):
        """ return info about the previous item in the container """
        if not self.order:
            return None
        order_reversed = list(reversed(self.order))
        pos = order_reversed.index(obj.getId())
        for oid in order_reversed[pos+1:]:
            data = self.getData(self.context[oid])
            if data:
                return data

    def getData(self, obj):
        """ return the expected mapping, see `INextPreviousProvider` """
        if not self.security.checkPermission('View', obj):
            return None
        elif not IContentish.providedBy(obj):
            # do not return a not contentish object
            # such as a local workflow policy for example (#11234)
            return None

        ptype = obj.portal_type
        url = obj.absolute_url()
        if ptype in self.vat:       # "use view action in listings"
            url += '/view'
        return dict(id=obj.getId(), url=url, title=obj.Title(),
            description=obj.Description(), portal_type=ptype)


class NextPreviousToggle(NextPreviousBase):
    """ adapter for acting as a next/previous provider """
    implements(INextPreviousProvider)
    adapts(INextPreviousToggle)

    @property
    def enabled(self):
        return getattr(aq_base(self.context), 'nextPreviousEnabled', False)


class NextPreviousEnabled(NextPreviousBase):
    """ adapter for acting as a next/previous provider """
    implements(INextPreviousProvider)
    adapts(INextPreviousEnabled)

    enabled = True
