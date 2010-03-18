import zope.i18nmessageid
MessageFactory = zope.i18nmessageid.MessageFactory('plone.app.dexterity')
PloneMessageFactory = zope.i18nmessageid.MessageFactory('plone')

try:
    from Products.CMFPlone.factory import _IMREALLYPLONE4
    PLONE40 = True
except ImportError:
    PLONE40 = False
