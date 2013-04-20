from Products.CMFCore.utils import getToolByName


def remove_stylesheet(context):
    cssreg = getToolByName(context, 'portal_css')
    cssreg.unregisterResource('++resource++schemaeditor.css')
