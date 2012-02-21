from Products.CMFCore.utils import getToolByName

def install_datepicker_profile(context):
    gs = getToolByName(context, 'portal_setup')
    profile = 'profile-collective.z3cform.datetimewidget:default'
    gs.runAllImportStepsFromProfile(profile, purge_old=False)
