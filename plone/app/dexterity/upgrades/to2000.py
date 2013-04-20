from Products.CMFCore.utils import getToolByName


def remove_overlays_css(context):
    portal_css = getToolByName(context, 'portal_css')
    portal_css.unregisterResource(
        '++resource++plone.app.dexterity.overlays.css')
