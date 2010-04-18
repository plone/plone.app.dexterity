from Products.CMFCore.utils import getToolByName

def install_jquerytools_profile(context):
    gs = getToolByName(context, 'portal_setup')
    profile = 'profile-plone.app.jquerytools:default'
    gs.runAllImportStepsFromProfile(profile, purge_old=False)
