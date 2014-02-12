import unittest2 as unittest
from plone.app.testing import setRoles, TEST_USER_ID
from plone.app.dexterity.behaviors.richtext import IRichText
from plone.app.dexterity.testing import DEXTERITY_INTEGRATION_TESTING

from plone.dexterity.fti import DexterityFTI
from Products.CMFCore.utils import getToolByName


class RichTextBase:
    # subclass here
    _behaviors = None
    _portal_type = None

    def _setupFTI(self):
        fti = DexterityFTI(self._portal_type)
        self.portal.portal_types._setObject(self._portal_type, fti)
        fti.klass = 'plone.dexterity.content.Item'
        fti.behaviors = self._behaviors


class RichTextToggleTests(RichTextBase, unittest.TestCase):
    """ basic use cases and tests for richtext behavior"""

    layer = DEXTERITY_INTEGRATION_TESTING

    _behaviors = (
        'plone.app.dexterity.behaviors.richtext.IRichText',)
    _portal_type = 'SomeDocument'

    def setUp(self):
        self.portal = self.layer['portal']
        self.wf = getToolByName(self.portal, "portal_workflow")
        self.portal.acl_users._doAddUser('user_std', 'secret', ['Member'], [])
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self._setupFTI()
        self.portal.invokeFactory(self._portal_type, 'doc1')
        setRoles(self.portal, TEST_USER_ID, ['Member'])

    def testIfDocImplementsRichText(self):
        self.assertTrue(IRichText(self.portal.doc1, None))


def test_suite():
    from unittest import defaultTestLoader
    return defaultTestLoader.loadTestsFromName(__name__)
