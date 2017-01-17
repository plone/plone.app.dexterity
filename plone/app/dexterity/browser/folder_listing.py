# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone.app.dexterity import _
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import ISecuritySchema
from Products.CMFPlone.PloneBatch import Batch
from Products.Five import BrowserView
from zope.component import getMultiAdapter
from zope.component import getUtility


class FolderView(BrowserView):

    def __init__(self, context, request):
        super(FolderView, self).__init__(context, request)

        self.plone_view = getMultiAdapter(
            (context, request), name=u'plone')
        self.portal_state = getMultiAdapter(
            (context, request), name=u'plone_portal_state')
        self.pas_member = getMultiAdapter(
            (context, request), name=u'pas_member')

        limit_display = getattr(self.request, 'limit_display', None)
        limit_display = int(limit_display) if limit_display is not None else 20
        b_size = getattr(self.request, 'b_size', None)
        self.b_size = int(b_size) if b_size is not None else limit_display
        b_start = getattr(self.request, 'b_start', None)
        self.b_start = int(b_start) if b_start is not None else 0

    def results(self, **kwargs):
        """Return a content listing based result set with contents of the
        folder.

        :param **kwargs: Any keyword argument, which can be used for catalog
                         queries.
        :type  **kwargs: keyword argument

        :returns: plone.app.contentlisting based result set.
        :rtype: ``plone.app.contentlisting.interfaces.IContentListing`` based
                sequence.
        """
        # Extra filter
        kwargs.update(self.request.get('contentFilter', {}))
        if 'object_provides' not in kwargs:  # object_provides is more specific
            kwargs.setdefault('portal_type', self.friendly_types)
        kwargs.setdefault('batch', True)
        kwargs.setdefault('b_size', self.b_size)
        kwargs.setdefault('b_start', self.b_start)

        listing = aq_inner(self.context).restrictedTraverse(
            '@@folderListing', None)
        if listing is None:
            return []
        results = listing(**kwargs)
        return results

    def batch(self):
        batch = Batch(
            self.results(),
            size=self.b_size,
            start=self.b_start,
            orphan=1
        )
        return batch

    def normalizeString(self, text):
        return self.plone_view.normalizeString(text)

    def toLocalizedTime(self, time, long_format=None, time_only=None):
        return self.plone_view.toLocalizedTime(time, long_format, time_only)

    @property
    def friendly_types(self):
        return self.portal_state.friendly_types()

    @property
    def isAnon(self):
        return self.portal_state.anonymous()

    @property
    def navigation_root_url(self):
        return self.portal_state.navigation_root_url()

    @property
    def use_view_action(self):
        registry = getUtility(IRegistry)
        return registry.get('plone.types_use_view_action_in_listings', [])

    @property
    def show_about(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISecuritySchema, prefix='plone')
        show_about = getattr(settings, 'allow_anon_views_about', False)
        return show_about or not self.isAnon

    @property
    def no_items_message(self):
        return _(
            'description_no_items_in_folder',
            default=u'There are currently no items in this folder.'
        )
