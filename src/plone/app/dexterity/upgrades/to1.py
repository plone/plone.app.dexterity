from Products.CMFCore.utils import getToolByName


def install_z3cform_profile(context):
    gs = getToolByName(context, "portal_setup")
    profile = "profile-plone.app.z3cform:default"
    gs.runAllImportStepsFromProfile(profile, purge_old=False)
