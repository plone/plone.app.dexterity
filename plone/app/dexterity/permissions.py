# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from plone.app.widgets.interfaces import IFieldPermissionChecker
from plone.app.widgets.interfaces import IWidgetsLayer
from plone.autoform.interfaces import WIDGETS_KEY
from plone.autoform.interfaces import WRITE_PERMISSIONS_KEY
from plone.autoform.utils import resolveDottedName
from plone.dexterity.interfaces import IDexterityContent
from plone.dexterity.utils import iterSchemata, getAdditionalSchemata
from plone.supermodel.utils import mergedTaggedValueDict
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IFieldWidget
from zope.component import adapts
from zope.component import queryMultiAdapter
from zope.component import queryUtility
from zope.interface import implements
from zope.publisher.browser import TestRequest
from zope.security.interfaces import IPermission


class MockRequest(TestRequest):
    implements(IWidgetsLayer)


class DXFieldPermissionChecker(object):
    """
    """

    implements(IFieldPermissionChecker)
    adapts(IDexterityContent)

    DEFAULT_PERMISSION = 'Modify portal content'

    def __init__(self, context):
        self.context = context
        self._request = MockRequest()

    def _get_schemata(self):
        return iterSchemata(self.context)

    def validate(self, field_name, vocabulary_name=None):
        context = self.context
        checker = getSecurityManager().checkPermission
        schemata = self._get_schemata()
        for schema in schemata:
            if field_name in schema:
                # If a vocabulary name was specified and it does not
                # match the vocabulary name for the field or widget,
                # fail.
                field = schema[field_name]
                if vocabulary_name and (
                   vocabulary_name != getattr(field, 'vocabulary', None) and
                   vocabulary_name != getattr(field, 'vocabularyName', None)):
                    # Determine the widget to check for vocabulary there
                    widgets = mergedTaggedValueDict(schema, WIDGETS_KEY)
                    widget = widgets.get(field_name)
                    if widget:
                        widget = (isinstance(widget, basestring) and
                                  resolveDottedName(widget) or widget)
                        widget = widget and widget(field, self._request)
                    else:
                        widget = queryMultiAdapter((field, self._request),
                                                   IFieldWidget)
                    if getattr(widget, 'vocabulary', None) != vocabulary_name:
                        return False
                # Create mapping of all schema permissions
                permissions = mergedTaggedValueDict(schema,
                                                    WRITE_PERMISSIONS_KEY)
                permission_name = permissions.get(field_name, None)
                if permission_name is not None:
                    permission = queryUtility(IPermission,
                                              name=permission_name)
                    if permission:
                        return checker(permission.title, context)

                # If the field is in the schema, but no permission is
                # specified, fall back to the default edit permission
                return checker(self.DEFAULT_PERMISSION, context)
        else:
            raise AttributeError('No such field: {0}'.format(field_name))


class DXAddViewFieldPermissionChecker(DXFieldPermissionChecker):
    """Permission checker for when we just have an add view"""

    adapts(IAddForm)

    def __init__(self, view):
        self.context = view.context
        # This may fail for views that aren't DefaultAddForm or
        # DefaultAddView sub-classes, but they can register their own
        # more specific adapters, if needed.
        self.fti = getattr(view, 'fti', None)
        if self.fti is None:
            self.fti = view.ti
        self._request = view.request

    def _get_schemata(self):
        fti = self.fti
        yield fti.lookupSchema()
        for schema in getAdditionalSchemata(portal_type=fti.getId()):
            yield schema
