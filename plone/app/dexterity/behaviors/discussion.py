from zope.deferredimport import deprecated

deprecated(
    "IAllowDiscussion is here deprecated. Import from plone.app.z3cform.widgets.select instead (will be removed in Plone 7)"
    IAllowDiscussion="plone.app.discussion.behaviors:IAllowDiscussion",
)
