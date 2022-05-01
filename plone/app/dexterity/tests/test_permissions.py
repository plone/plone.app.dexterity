from plone.app.content.browser.vocabulary import VocabularyView
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.app.widgets.testing import PLONEAPPWIDGETS_DX_INTEGRATION_TESTING
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.autoform.interfaces import WIDGETS_KEY
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.fti import DexterityFTI
from z3c.form.interfaces import IFieldWidget
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from zope import schema
from zope.component import provideAdapter
from zope.component.globalregistry import base
from zope.globalrequest import setRequest
from zope.interface import Interface
from zope.publisher.browser import TestRequest

import json
import unittest


def add_mock_fti(portal):
    # Fake DX Type
    fti = DexterityFTI("dx_mock")
    portal.portal_types._setObject("dx_mock", fti)
    fti.klass = "plone.dexterity.content.Item"
    fti.schema = "plone.app.dexterity.tests.test_permissions.IMockSchema"
    fti.filter_content_types = False
    fti.behaviors = ("plone.app.dexterity.behaviors.metadata.IBasic",)


def _custom_field_widget(field, request):
    from plone.app.z3cform.widget import AjaxSelectWidget

    widget = FieldWidget(field, AjaxSelectWidget(request))
    widget.vocabulary = "plone.app.vocabularies.PortalTypes"
    return widget


class IMockSchema(Interface):
    allowed_field = schema.Choice(vocabulary="plone.app.vocabularies.PortalTypes")
    disallowed_field = schema.Choice(vocabulary="plone.app.vocabularies.PortalTypes")
    default_field = schema.Choice(vocabulary="plone.app.vocabularies.PortalTypes")
    custom_widget_field = schema.TextLine()
    adapted_widget_field = schema.TextLine()


IMockSchema.setTaggedValue(
    WRITE_PERMISSIONS_KEY,
    {
        "allowed_field": "zope2.View",
        "disallowed_field": "zope2.ViewManagementScreens",
        "custom_widget_field": "zope2.View",
        "adapted_widget_field": "zope2.View",
    },
)
IMockSchema.setTaggedValue(
    WIDGETS_KEY,
    {
        "custom_widget_field": _custom_field_widget,
    },
)


def _enable_custom_widget(field):
    provideAdapter(
        _custom_field_widget,
        adapts=(getSpecification(field), IPloneFormLayer),
        provides=IFieldWidget,
    )


def _disable_custom_widget(field):
    base.unregisterAdapter(
        required=(
            getSpecification(field),
            IPloneFormLayer,
        ),
        provided=IFieldWidget,
    )


class DexterityVocabularyPermissionTests(unittest.TestCase):

    layer = PLONEAPPWIDGETS_DX_INTEGRATION_TESTING

    def setUp(self):
        self.request = TestRequest(environ={"HTTP_ACCEPT_LANGUAGE": "en"})
        setRequest(self.request)
        self.portal = self.layer["portal"]

        login(self.portal, TEST_USER_NAME)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        add_mock_fti(self.portal)
        self.portal.invokeFactory("dx_mock", "test_dx")

        self.portal.test_dx.manage_permission("View", ("Anonymous",), acquire=False)
        self.portal.test_dx.manage_permission(
            "View management screens", (), acquire=False
        )
        self.portal.test_dx.manage_permission(
            "Modify portal content",
            ("Editor", "Manager", "Site Adiminstrator"),
            acquire=False,
        )

    def test_vocabulary_field_allowed(self):
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update(
            {
                "name": "plone.app.vocabularies.PortalTypes",
                "field": "allowed_field",
            }
        )
        data = json.loads(view())
        self.assertEqual(
            len(data["results"]),
            len(self.portal.portal_types.objectIds()),
        )

    def test_vocabulary_field_wrong_vocabulary_disallowed(self):
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update(
            {
                "name": "plone.app.vocabularies.Fake",
                "field": "allowed_field",
            }
        )
        data = json.loads(view())
        self.assertEqual(data["error"], "Vocabulary lookup not allowed")

    def test_vocabulary_field_disallowed(self):
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update(
            {
                "name": "plone.app.vocabularies.PortalTypes",
                "field": "disallowed_field",
            }
        )
        data = json.loads(view())
        self.assertEqual(data["error"], "Vocabulary lookup not allowed")

    def test_vocabulary_field_default_permission(self):
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update(
            {
                "name": "plone.app.vocabularies.PortalTypes",
                "field": "default_field",
            }
        )
        # If the field is does not have a security declaration, the
        # default edit permission is tested (Modify portal content)
        setRoles(self.portal, TEST_USER_ID, ["Member"])
        data = json.loads(view())
        self.assertEqual(data["error"], "Vocabulary lookup not allowed")

        setRoles(self.portal, TEST_USER_ID, ["Editor"])
        # Now access should be allowed, but the vocabulary does not exist
        data = json.loads(view())
        self.assertEqual(
            len(data["results"]),
            len(self.portal.portal_types.objectIds()),
        )

    def test_vocabulary_field_default_permission_wrong_vocab(self):
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update(
            {
                "name": "plone.app.vocabularies.Fake",
                "field": "default_field",
            }
        )
        setRoles(self.portal, TEST_USER_ID, ["Editor"])
        # Now access should be allowed, but the vocabulary does not exist
        data = json.loads(view())
        self.assertEqual(data["error"], "Vocabulary lookup not allowed")

    def test_vocabulary_missing_field(self):
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update(
            {
                "name": "plone.app.vocabularies.PortalTypes",
                "field": "missing_field",
            }
        )
        setRoles(self.portal, TEST_USER_ID, ["Member"])
        with self.assertRaises(AttributeError):
            view()

    def test_vocabulary_on_widget(self):
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update(
            {
                "name": "plone.app.vocabularies.PortalTypes",
                "field": "custom_widget_field",
            }
        )
        data = json.loads(view())
        self.assertEqual(
            len(data["results"]),
            len(self.portal.portal_types.objectIds()),
        )
        self.request.form["name"] = "plone.app.vocabularies.Fake"
        data = json.loads(view())
        self.assertEqual(data["error"], "Vocabulary lookup not allowed")

    def test_vocabulary_on_adapted_widget(self):
        _enable_custom_widget(IMockSchema["adapted_widget_field"])
        view = VocabularyView(self.portal.test_dx, self.request)
        self.request.form.update(
            {
                "name": "plone.app.vocabularies.PortalTypes",
                "field": "adapted_widget_field",
            }
        )
        data = json.loads(view())
        self.assertEqual(
            len(data["results"]),
            len(self.portal.portal_types.objectIds()),
        )

        self.request.form["name"] = "plone.app.vocabularies.Fake"
        data = json.loads(view())
        self.assertEqual(data["error"], "Vocabulary lookup not allowed")
        _disable_custom_widget(IMockSchema["adapted_widget_field"])

    def test_vocabulary_field_allowed_from_add_view(self):
        add_view = DefaultAddView(
            self.portal, self.request, self.portal.portal_types["dx_mock"]
        )
        view = VocabularyView(add_view, self.request)
        self.request.form.update(
            {
                "name": "plone.app.vocabularies.PortalTypes",
                "field": "allowed_field",
            }
        )
        data = json.loads(view())
        self.assertEqual(
            len(data["results"]),
            len(self.portal.portal_types.objectIds()),
        )

    def test_vocabulary_field_allowed_from_add_form(self):
        add_form = DefaultAddForm(self.portal, self.request)
        add_form.portal_type = "dx_mock"
        view = VocabularyView(add_form, self.request)
        self.request.form.update(
            {
                "name": "plone.app.vocabularies.PortalTypes",
                "field": "allowed_field",
            }
        )
        data = json.loads(view())
        self.assertEqual(
            len(data["results"]),
            len(self.portal.portal_types.objectIds()),
        )
