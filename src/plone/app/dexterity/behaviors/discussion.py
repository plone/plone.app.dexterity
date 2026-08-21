from zope.deferredimport import deprecated

deprecated(
    "IAllowDiscussion import from here is deprecated. Import from plone.app.discussion.behavior instead (will be removed in Plone 7)",
    IAllowDiscussion="plone.app.discussion.behavior:IAllowDiscussion",
)
