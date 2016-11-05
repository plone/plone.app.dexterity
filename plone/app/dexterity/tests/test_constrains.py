# -*- coding: utf-8 -*-
from plone.app.content.browser.constraintypes import IConstrainForm
from plone.app.dexterity.behaviors import constrains
from plone.app.dexterity.testing import DEXTERITY_FUNCTIONAL_TESTING
from plone.app.dexterity.testing import DEXTERITY_INTEGRATION_TESTING
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.dexterity.fti import DexterityFTI
from plone.testing.z2 import Browser
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from zope.interface.exceptions import Invalid

import unittest


def add_folder_type(portal):
    fti = DexterityFTI('folder')
    portal.portal_types._setObject('folder', fti)
    fti.klass = 'plone.dexterity.content.Container'
    fti.filter_content_types = False
    fti.behaviors = (
        'Products.CMFPlone.interfaces.constrains.'
        'ISelectableConstrainTypes',
        'plone.app.dexterity.behaviors.metadata.IBasic')
    return fti


def add_item_type(portal):
    fti = DexterityFTI('item')
    portal.portal_types._setObject('item', fti)
    fti.klass = 'plone.dexterity.content.Item'
    fti.filter_content_types = False
    fti.behaviors = (
        'plone.app.dexterity.behaviors.metadata.IBasic')
    return fti


class DocumentIntegrationTest(unittest.TestCase):

    layer = DEXTERITY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

        self.fti = add_folder_type(self.portal)

        self.portal.invokeFactory('folder', 'folder')
        self.folder = self.portal['folder']

        self.folder.invokeFactory('folder', 'inner_folder')
        self.inner_folder = self.folder['inner_folder']

        self.types_tool = getToolByName(self.portal, 'portal_types')
        folder_type = self.types_tool.getTypeInfo(self.folder)
        self.default_types = [
            t
            for t in self.types_tool.listTypeInfo()
            if t.isConstructionAllowed(self.folder) and
            folder_type.allowType(t.getId())
        ]
        assert len(self.default_types) > 1
        self.types_id_subset = [t.getId() for t in self.default_types][:1]

    def test_behavior_added(self):
        self.assertIn('Products.CMFPlone.interfaces.'
                      'constrains.ISelectableConstrainTypes',
                      self.types_tool.getTypeInfo(self.folder).behaviors)
        self.assertTrue(ISelectableConstrainTypes(self.folder))

    def test_constrainTypesModeDefault(self):
        behavior1 = ISelectableConstrainTypes(self.folder)
        behavior2 = ISelectableConstrainTypes(self.inner_folder)
        self.assertEqual(
            constrains.DISABLED, behavior1.getConstrainTypesMode())
        self.assertEqual(constrains.ACQUIRE, behavior2.getConstrainTypesMode())

    def test_constrainTypesModeValidSet(self):
        behavior = ISelectableConstrainTypes(self.folder)
        behavior.setConstrainTypesMode(constrains.ENABLED)
        self.assertEqual(constrains.ENABLED, behavior.getConstrainTypesMode())

    def test_constrainTypesModeInvalidSet(self):
        behavior = ISelectableConstrainTypes(self.folder)
        self.assertRaises(
            ValueError, behavior.setConstrainTypesMode, 'INVALID')

    def test_canSetConstrainTypesMode(self):
        behavior = ISelectableConstrainTypes(self.folder)
        self.assertEqual(1, behavior.canSetConstrainTypes())

    def test_locallyAllowedTypesDefaultWhenDisabled(self):
        """
        Constrain Mode Disabled.
        We get the default constrains, independent of what our parent folder
        or we ourselves defined
        """
        behavior = ISelectableConstrainTypes(self.inner_folder)
        behavior.setConstrainTypesMode(constrains.DISABLED)
        behavior.setLocallyAllowedTypes([])

        outer_behavior = ISelectableConstrainTypes(self.folder)
        outer_behavior.setConstrainTypesMode(constrains.ENABLED)
        outer_behavior.setLocallyAllowedTypes([])

        types = self.default_types
        type_ids = [t.getId() for t in types]

        self.assertEqual(types, behavior.allowedContentTypes())
        self.assertEqual(type_ids, behavior.getLocallyAllowedTypes())

    def test_locallyAllowedTypesDefaultWhenEnabled(self):
        """
        Constrain Mode enabled
        We get the set constrains, independent of what our parent folder
        defined
        """
        behavior = ISelectableConstrainTypes(self.inner_folder)
        behavior.setConstrainTypesMode(constrains.ENABLED)
        behavior.setLocallyAllowedTypes(self.types_id_subset)

        outer_behavior = ISelectableConstrainTypes(self.folder)
        outer_behavior.setConstrainTypesMode(constrains.ENABLED)
        outer_behavior.setLocallyAllowedTypes([])

        types = [t for t in self.default_types
                 if t.getId() in self.types_id_subset]
        type_ids = self.types_id_subset

        self.assertEqual(types, behavior.allowedContentTypes())
        self.assertEqual(type_ids, behavior.getLocallyAllowedTypes())

    def test_locallyAllowedTypesDefaultWhenAcquired(self):
        """
        Constrain Mode set to ACQUIRE
        Try to acquire the constrains, if that fails, use the defaults
        """
        behavior = ISelectableConstrainTypes(self.inner_folder)
        behavior.setConstrainTypesMode(constrains.ACQUIRE)
        behavior.setLocallyAllowedTypes([])

        outer_behavior = ISelectableConstrainTypes(self.folder)
        outer_behavior.setConstrainTypesMode(constrains.ENABLED)
        outer_behavior.setLocallyAllowedTypes(self.types_id_subset)

        types = self.types_id_subset

        self.assertEqual(types, behavior.getLocallyAllowedTypes())

        outer_behavior.setConstrainTypesMode(constrains.ACQUIRE)

        types = self.default_types
        type_ids = [t.getId() for t in types]

        self.assertEqual(types, behavior.allowedContentTypes())
        self.assertEqual(type_ids, behavior.getLocallyAllowedTypes())

    def test_locallyAllowedTypesDefaultWhenMultipleAcquired(self):
        """
        Prevent regression.
        Multiple (two or more) acquisition from parent must not fail if
        user doesn't have add permission on parent.
        """
        self.inner_folder.invokeFactory('folder', 'deeper_folder')
        deeper_folder = self.inner_folder.deeper_folder
        self.portal.acl_users._doAddUser(
            'user_contributor', 'secret', ['Member'],
            []
        )
        deeper_folder.manage_addLocalRoles('user_contributor', ['Contributor'])
        login(self.portal, 'user_contributor')
        behavior = ISelectableConstrainTypes(deeper_folder)
        types = behavior.getLocallyAllowedTypes()
        self.assertTrue(len(types) > 0)

    def test_locallyAllowedTypesInvalidSet(self):
        behavior = ISelectableConstrainTypes(self.folder)
        self.assertRaises(ValueError,
                          behavior.setLocallyAllowedTypes,
                          self.types_id_subset + ['invalid'])

    def test_locallyAllowedTypesInvalidValuesGetFiltered(self):
        behavior = ISelectableConstrainTypes(self.folder)
        behavior.setConstrainTypesMode(constrains.ENABLED)
        self.folder.locally_allowed_types = self.types_id_subset + \
            ['invalid']
        self.assertEqual(
            self.types_id_subset, behavior.getLocallyAllowedTypes())

    def test_immediatelyAllowedTypesDefaultWhenDisabled(self):
        """
        Constrain Mode Disabled.
        We get the default addables, independent of what our parent folder
        or we ourselves defined
        """
        behavior = ISelectableConstrainTypes(self.inner_folder)
        behavior.setConstrainTypesMode(constrains.DISABLED)
        behavior.setImmediatelyAddableTypes([])

        outer_behavior = ISelectableConstrainTypes(self.folder)
        outer_behavior.setConstrainTypesMode(constrains.ENABLED)
        outer_behavior.setImmediatelyAddableTypes([])

        types = [t.getId() for t in self.default_types]

        self.assertEqual(types, behavior.getImmediatelyAddableTypes())

    def test_immediatelyAllowedTypesDefaultWhenEnabled(self):
        """
        Constrain Mode enabled
        We get the set constrains, independent of what our parent folder
        defined
        """
        behavior = ISelectableConstrainTypes(self.inner_folder)
        behavior.setConstrainTypesMode(constrains.ENABLED)
        behavior.setImmediatelyAddableTypes(self.types_id_subset)

        outer_behavior = ISelectableConstrainTypes(self.folder)
        outer_behavior.setConstrainTypesMode(constrains.ENABLED)
        outer_behavior.setImmediatelyAddableTypes([])

        types = self.types_id_subset

        self.assertEqual(types, behavior.getImmediatelyAddableTypes())

    def test_immediatelyAllowedTypesDefaultWhenAcquired(self):
        """
        Constrain Mode set to ACQUIRE
        Try to acquire the constrains, if that fails, use the defaults
        """
        behavior = ISelectableConstrainTypes(self.inner_folder)
        behavior.setConstrainTypesMode(constrains.ACQUIRE)
        behavior.setImmediatelyAddableTypes([])

        outer_behavior = ISelectableConstrainTypes(self.folder)
        outer_behavior.setConstrainTypesMode(constrains.ENABLED)
        outer_behavior.setImmediatelyAddableTypes(self.types_id_subset)

        types = self.types_id_subset

        self.assertEqual(types, behavior.getImmediatelyAddableTypes())

        outer_behavior.setConstrainTypesMode(constrains.ACQUIRE)

        types = [t.getId() for t in self.default_types]

        self.assertEqual(types, outer_behavior.getImmediatelyAddableTypes())

    def test_immediatelyAllowedTypesInvalidSet(self):
        behavior = ISelectableConstrainTypes(self.folder)
        self.assertRaises(ValueError,
                          behavior.setImmediatelyAddableTypes,
                          self.types_id_subset + ['invalid'])

    def test_immediatelyAllowedTypesInvalidValuesGetFiltered(self):
        behavior = ISelectableConstrainTypes(self.folder)
        behavior.setConstrainTypesMode(constrains.ENABLED)
        self.folder.immediately_addable_types = self.types_id_subset + \
            ['invalid']
        self.assertEqual(
            self.types_id_subset, behavior.getImmediatelyAddableTypes())

    def test_defaultAddableTypesDefault(self):
        behavior = ISelectableConstrainTypes(self.folder)
        self.assertEqual(self.default_types, behavior.getDefaultAddableTypes())

    def test_allowedContentTypesExit1(self):
        """
        Constrains are disabled, use the portal ones
        """
        behavior = ISelectableConstrainTypes(self.folder)

        types = behavior._getAddableTypesFor(self.portal, self.folder)

        behavior.setConstrainTypesMode(constrains.DISABLED)
        self.assertEqual(types, behavior.allowedContentTypes())

    def test_allowedContentTypesExit2(self):
        """
        Constrains are acquired, parent folder is Plone Site
        """
        behavior = ISelectableConstrainTypes(self.folder)

        types = behavior._getAddableTypesFor(self.portal, self.folder)

        behavior.setConstrainTypesMode(constrains.ACQUIRE)
        self.assertEqual(types, behavior.allowedContentTypes())

    def test_allowedContentTypesExit3(self):
        """
        Constrains are acquired, parent folder is of same type
        """
        outer_behavior = ISelectableConstrainTypes(self.folder)

        assert len(outer_behavior.getLocallyAllowedTypes()) > 2
        outer_behavior.setLocallyAllowedTypes(self.types_id_subset)
        outer_behavior.setConstrainTypesMode(constrains.ENABLED)

        behavior = ISelectableConstrainTypes(self.inner_folder)
        behavior.setConstrainTypesMode(constrains.ACQUIRE)
        self.assertEqual(
            self.types_id_subset,
            [x.getId() for x in behavior.allowedContentTypes()]
        )

    def test_allowedContentTypesExit4(self):
        """
        Constrains are enabled
        """
        behavior = ISelectableConstrainTypes(self.folder)

        behavior.setLocallyAllowedTypes(self.types_id_subset)
        behavior.setConstrainTypesMode(constrains.ENABLED)

        self.assertEqual(
            self.types_id_subset,
            [x.getId() for x in behavior.allowedContentTypes()]
        )

    def test_formschemainvariants(self):
        class Data(object):
            allowed_types = []
            secondary_types = []
        bad = Data()
        bad.allowed_types = []
        bad.secondary_types = ['1']
        good = Data()
        good.allowed_types = ['1']
        good.secondary_types = []
        self.assertTrue(IConstrainForm.validateInvariants(good) is None)
        self.assertRaises(Invalid, IConstrainForm.validateInvariants, bad)


class FolderConstrainViewFunctionalText(unittest.TestCase):

    layer = DEXTERITY_FUNCTIONAL_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal_url = self.portal.absolute_url()

        self.fti = add_folder_type(self.portal)

        self.portal.invokeFactory('folder', id='folder', title='My Folder')
        self.folder = self.portal.folder
        self.folder_url = self.folder.absolute_url()
        import transaction
        transaction.commit()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )

    def test_folder_view(self):
        self.browser.open(self.folder_url + '/view')
        self.assertTrue('My Folder' in self.browser.contents)
        self.assertTrue('Restrictions' in self.browser.contents)

    def test_folder_restrictions_view(self):
        self.browser.open(self.folder_url + '/folder_constraintypes_form')
        self.assertIn('Restrict what types', self.browser.contents)
        self.assertIn(
            '// Custom form constraints for constrain form',
            self.browser.contents,
        )
        self.assertIn('current_prefer_form', self.browser.contents)

    def test_form_save_restrictions(self):
        self.browser.open(self.folder_url)
        self.browser.getLink('Restrictions').click()

        def ctrl(name):
            return self.browser.getControl(name=name)

        self.browser.getControl('Type restrictions').value = ['1']
        ctrl('form.widgets.allowed_types:list').value = ['Document', 'Folder']
        ctrl('form.widgets.secondary_types:list').value = ['Document']
        self.browser.getControl('Save').click()
        aspect = ISelectableConstrainTypes(self.folder)
        self.assertEqual(1, aspect.getConstrainTypesMode())
        self.assertEqual(
            ['Document', 'Folder'],
            aspect.getLocallyAllowedTypes()
        )
        self.assertEqual(['Folder'], aspect.getImmediatelyAddableTypes())

    def test_form_bad_save(self):
        aspect = ISelectableConstrainTypes(self.folder)
        constraint_before = aspect.getConstrainTypesMode()
        assert constraint_before != 1, ('Default constraint should not be 1. '
                                        'Test is outdated.')

        self.browser.open(self.folder_url)
        self.browser.getLink('Restrictions').click()

        def ctrl(name):
            return self.browser.getControl(name=name)

        self.browser.getControl('Type restrictions').value = ['1']
        ctrl('form.widgets.allowed_types:list').value = ['Document']
        ctrl('form.widgets.secondary_types:list').value = [
            'Document',
            'Folder'
        ]
        self.browser.getControl('Save').click()
        self.assertEqual(constraint_before, aspect.getConstrainTypesMode())
        self.assertTrue('Error' in self.browser.contents)


class ConstrainControlFunctionalText(unittest.TestCase):

    layer = DEXTERITY_FUNCTIONAL_TESTING

    def setUp(self):
        app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal_url = self.portal.absolute_url()

        self.folder_fti = add_folder_type(self.portal)
        self.item_fti = add_item_type(self.portal)

        import transaction
        transaction.commit()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic {0}:{1}'.format(SITE_OWNER_NAME, SITE_OWNER_PASSWORD, ),
        )

    def test_overview_folder_view(self):
        url = '/dexterity-types/folder/@@overview'
        self.browser.open(self.portal_url + url)
        self.assertTrue('Filter Contained Types' in self.browser.contents)
        self.assertTrue('No content types' in self.browser.contents)

    def test_overview_item_view(self):
        url = '/dexterity-types/item/@@overview'
        self.browser.open(self.portal_url + url)
        self.assertFalse('Filter Contained Types' in self.browser.contents)
        self.assertFalse('No content types' in self.browser.contents)

    def test_overview_folder_item_view(self):
        # First we access folder content types and check
        # that is possible to fiter content types (as it is a container)
        url = '/dexterity-types/folder/@@overview'
        self.browser.open(self.portal_url + url)
        self.assertTrue('Filter Contained Types' in self.browser.contents)
        self.assertTrue('No content types' in self.browser.contents)

        # Then we access item content types and check
        # that is NOT possible to fiter content types
        url = '/dexterity-types/item/@@overview'
        self.browser.open(self.portal_url + url)
        self.assertFalse('Filter Contained Types' in self.browser.contents)
        self.assertFalse('No content types' in self.browser.contents)

        # Acessing folder content types again
        # and it should be possible to filter content types
        url = '/dexterity-types/folder/@@overview'
        self.browser.open(self.portal_url + url)
        self.assertTrue('Filter Contained Types' in self.browser.contents)
        self.assertTrue('No content types' in self.browser.contents)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
