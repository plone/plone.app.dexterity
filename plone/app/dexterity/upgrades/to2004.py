from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFCore.utils import getToolByName


def remove_cr_and_lf_description(context):
    types = []

    behaviors = [
        "plone.app.dexterity.behaviors.metadata.IBasic",
        "plone.app.dexterity.behaviors.metadata.IDublinCore",
    ]

    context = context.aq_parent
    sm = context.getSiteManager()
    for (name, fti) in sm.getUtilitiesFor(IDexterityFTI):
        for behavior in behaviors:
            if behavior in fti.behaviors:
                types.append(name)

    catalog = getToolByName(context, "portal_catalog")

    for portal_type in types:
        brains = catalog.searchResults(portal_type=portal_type)

        for brain in brains:
            obj = brain.getObject()

            if "\n" in obj.description:
                obj.description = obj.description.replace("\n", "")

            if "\r" in obj.description:
                obj.description = obj.description.replace("\r", "")
