from AccessControl import getSecurityManager
from Acquisition import aq_base
from plone.app.dexterity import _
from plone.app.layout.nextprevious.interfaces import INextPreviousProvider
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.registry.interfaces import IRegistry
from plone.supermodel import model
from Products.CMFCore.interfaces import IContentish
from z3c.form import widget
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


class INextPreviousEnabled(Interface):
    """Behavior interface to enable next previous navigation for all items of
    a type.
    """


@provider(IFormFieldProvider)
class INextPreviousToggle(model.Schema):
    """Behavior interface to enable next previous navigation per item."""

    model.fieldset("settings", label=_("Settings"), fields=["nextPreviousEnabled"])

    nextPreviousEnabled = schema.Bool(
        title=_("label_nextprevious", default="Enable next previous navigation"),
        description=_(
            "help_nextprevious",
            default="This enables next/previous widget on content items "
            + "contained in this folder.",
        ),
        default=False,
        required=False,
    )

    directives.omitted("nextPreviousEnabled")
    directives.no_omit(IEditForm, "nextPreviousEnabled")
    directives.no_omit(IAddForm, "nextPreviousEnabled")


def getNextPreviousParentValue(adapter_):
    context = adapter_.context
    nextprevious = INextPreviousProvider(context, None)
    if nextprevious is None:
        return False
    return nextprevious.enabled


DefaultNextPreviousEnabled = widget.ComputedWidgetAttribute(
    getNextPreviousParentValue,
    field=INextPreviousToggle["nextPreviousEnabled"],
)


# This is taken from plone.app.folder
class NextPreviousBase:
    """adapter for acting as a next/previous provider"""

    def __init__(self, context):
        self.context = context
        registry = getUtility(IRegistry)
        self.vat = registry.get("plone.types_use_view_action_in_listings", [])
        self.security = getSecurityManager()
        order = context.getOrdering()
        if not isinstance(order, list):
            order = order.idsInOrder()
        if not isinstance(order, list):
            order = None
        self.order = order

    def getNextItem(self, obj):
        """return info about the next item in the container"""
        if not self.order:
            return None
        pos = self.context.getObjectPosition(obj.getId())
        if pos is None:
            return None
        for oid in self.order[pos + 1 :]:
            data = self.getData(self.context[oid])
            if data:
                return data

    def getPreviousItem(self, obj):
        """return info about the previous item in the container"""
        if not self.order:
            return None
        order_reversed = list(reversed(self.order))
        pos = order_reversed.index(obj.getId())
        for oid in order_reversed[pos + 1 :]:
            data = self.getData(self.context[oid])
            if data:
                return data

    def getData(self, obj):
        """return the expected mapping, see `INextPreviousProvider`"""
        if not self.security.checkPermission("View", obj):
            return None
        elif not IContentish.providedBy(obj):
            # do not return a not contentish object
            # such as a local workflow policy for example (#11234)
            return None

        ptype = obj.portal_type
        url = obj.absolute_url()
        if ptype in self.vat:  # "use view action in listings"
            url += "/view"
        return dict(
            id=obj.getId(),
            url=url,
            title=obj.Title(),
            description=obj.Description(),
            portal_type=ptype,
        )


@implementer(INextPreviousProvider)
@adapter(INextPreviousToggle)
class NextPreviousToggle(NextPreviousBase):
    """adapter for acting as a next/previous provider"""

    @property
    def enabled(self):
        return getattr(aq_base(self.context), "nextPreviousEnabled", False)


@implementer(INextPreviousProvider)
@adapter(INextPreviousEnabled)
class NextPreviousEnabled(NextPreviousBase):
    """adapter for acting as a next/previous provider"""

    enabled = True
