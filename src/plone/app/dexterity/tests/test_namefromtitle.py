from plone.app.dexterity.testing import DEXTERITY_FUNCTIONAL_TESTING
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from plone.dexterity.fti import DexterityFTI
from plone.testing.zope import Browser

import transaction
import unittest


def add_dinosaur_type(portal, behavior_name):
    fti = DexterityFTI("dinosaur")
    portal.portal_types._setObject("dinosaur", fti)
    fti.klass = "plone.dexterity.content.Container"
    fti.filter_content_types = False
    fti.behaviors = (
        behavior_name,
        "plone.basic",
    )
    return fti


class NameFromTitleFunctionalTest(unittest.TestCase):
    """Test name-from-title using named behavior."""

    layer = DEXTERITY_FUNCTIONAL_TESTING
    behavior_name = "plone.namefromtitle"

    def setUp(self):
        app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.portal_url = self.portal.absolute_url()

        # Say we have a 'Dinosaur' content type:
        self.fti = add_dinosaur_type(self.portal, self.behavior_name)

        transaction.commit()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        self.browser.addHeader(
            "Authorization",
            "Basic {}:{}".format(
                TEST_USER_NAME,
                TEST_USER_PASSWORD,
            ),
        )

    def test_create(self):
        self.browser.open(f"{self.portal_url}/++add++dinosaur")
        self.browser.getControl("Title").value = "Brachiosaurus"
        self.browser.getControl("Save").click()
        self.assertEqual(self.browser.url, f"{self.portal_url}/brachiosaurus/view")

        # Does it still work if we are adding content within a container?
        self.browser.open(f"{self.portal_url}/brachiosaurus/++add++dinosaur")
        self.browser.getControl("Title").value = "Baby Brachiosaurus"
        self.browser.getControl("Save").click()
        self.assertEqual(
            self.browser.url,
            f"{self.portal_url}/brachiosaurus/baby-brachiosaurus/view",
        )


class PloneAppContentNameFromTitleFunctionalTest(NameFromTitleFunctionalTest):
    """Test name-from-title using old plone.app.content behavior interface."""

    behavior_name = "plone.app.content.interfaces.INameFromTitle"


# We could test that you can use the new interface location as behavior name,
# but this fails, and this is fine: it was never supported.
# In all cases the named behavior is recommended.
#
# class PloneBaseNameFromTitleFunctionalTest(NameFromTitleFunctionalTest):
#     """Test name-from-title using new plone.base behavior interface."""
#     behavior_name = "plone.base.interfaces.INameFromTitle"


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)
