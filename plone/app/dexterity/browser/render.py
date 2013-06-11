from Products.Five.browser.metaconfigure import ViewMixinForTemplates
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from Products.Five import BrowserView


# The widget rendering templates need to be Zope 3 templates
class RenderWidgets(ViewMixinForTemplates, BrowserView):
    index = ViewPageTemplateFile('render_widgets.pt')


# The widget rendering templates need to be Zope 3 templates
class RenderGroups(ViewMixinForTemplates, BrowserView):
    index = ViewPageTemplateFile('render_groups.pt')


# The widget rendering templates need to be Zope 3 templates
class RenderFolderListing(ViewMixinForTemplates, BrowserView):
    index = ViewPageTemplateFile('render_folder_listing.pt')
