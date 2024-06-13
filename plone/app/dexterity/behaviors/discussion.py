from zope.deferredimport import deprecated


deprecated(
    "IAllowDiscussion import from here is deprecated. Import from plone.app.discussion.behaviors instead (will be removed in Plone 7)",
    IAllowDiscussion="plone.app.discussion.behaviors:IAllowDiscussion",
)
