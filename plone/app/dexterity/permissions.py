from AccessControl import getSecurityManager
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.autoform.interfaces import WIDGETS_KEY
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from plone.autoform.utils import resolveDottedName
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.utils import iterSchemata
from plone.supermodel.utils import mergedTaggedValueDict
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IForm
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.deprecation import deprecated
from zope.interface import implementer
from zope.publisher.browser import TestRequest
from zope.security.interfaces import IPermission


try:
    from plone.app.z3cform.interfaces import IFieldPermissionChecker
except ImportError:
    # bbb for < plone 5.2rc2
    from plone.app.widgets.interfaces import IFieldPermissionChecker


@implementer(IPloneFormLayer)
class MockRequest(TestRequest):
    pass


@adapter(IDexterityContent)
@implementer(IFieldPermissionChecker)
class DXFieldPermissionChecker:
    """ """

    DEFAULT_PERMISSION = "Modify portal content"

    def __init__(self, context):
        self.context = context
        self._request = MockRequest()

    def _get_schemata(self):
        return iterSchemata(self.context)

    def _validate_vocabulary_name(self, schema, field, vocabulary_name):
        if not vocabulary_name:
            return True
        if vocabulary_name != getattr(
            field, "vocabulary", None
        ) and vocabulary_name != getattr(field, "vocabularyName", None):
            # Determine the widget to check for vocabulary there
            widgets = mergedTaggedValueDict(schema, WIDGETS_KEY)
            widget = widgets.get(field.getName())
            if widget:
                if isinstance(widget, str):
                    widget = resolveDottedName(widget)
                if widget:
                    widget = widget(field, self._request)
            else:
                # default widget
                widget = queryMultiAdapter((field, self._request), IFieldWidget)
            if widget:
                widget.update()
            if getattr(widget, "vocabulary", None) != vocabulary_name:
                return False
        return True

    def validate(self, field_name, vocabulary_name=None):
        context = self.context
        checker = getSecurityManager().checkPermission
        schemata = self._get_schemata()
        for schema in schemata:
            if field_name not in schema:
                continue
            # If a vocabulary name was specified and it does not
            # match the vocabulary name for the field or widget,
            # fail.
            field = schema[field_name]
            if not self._validate_vocabulary_name(schema, field, vocabulary_name):
                return False
            # Create mapping of all schema permissions
            permissions = mergedTaggedValueDict(schema, WRITE_PERMISSIONS_KEY)
            permission_name = permissions.get(field_name, None)
            if permission_name is not None:
                # if we have explicit permissions, check them
                permission = queryUtility(IPermission, name=permission_name)
                if permission:
                    return checker(permission.title, context)

            # If the field is in the schema, but no permission is
            # specified, fall back to the default edit permission
            return checker(self.DEFAULT_PERMISSION, context)
        else:
            raise AttributeError(f"No such field: {field_name}")


@adapter(IForm)
class GenericFormFieldPermissionChecker(DXFieldPermissionChecker):
    """Permission checker for when we just have an add view"""

    DEFAULT_PERMISSION = "Add portal content"

    def __init__(self, view):
        if getattr(view, "form_instance", None) is not None:
            view = view.form_instance
        if getattr(view, "create", None):
            content = view.create({})
            self.context = content.__of__(view.context)
        else:
            self.context = view.context

        self._request = MockRequest()
        self.view = view

    def _get_schemata(self):
        if getattr(self.view, "create", None):
            return iterSchemata(self.context)
        return [self.view.schema]


# BBB: Old name to match prior more limited function
DXAddViewFieldPermissionChecker = GenericFormFieldPermissionChecker
deprecated(
    "DXAddViewFieldPermissionChecker",
    "plone.app.dexterity.permissions.DXAddViewFieldPermissionChecker has been "
    "replaced with GenericFormFieldPermissionChecker, please update any "
    "imports.",
)
