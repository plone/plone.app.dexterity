import urllib

from zExceptions import NotFound
from OFS.SimpleItem import SimpleItem

from zope.interface import implements
from zope.cachedescriptors.property import Lazy as lazy_property
from zope.component import adapts, getAllUtilitiesRegisteredFor, getUtility, ComponentLookupError
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

from z3c.form import field, button
from plone.z3cform import layout
from plone.z3cform.crud import crud

from Products.CMFCore.utils import getToolByName

from plone.dexterity.interfaces import IDexterityFTI
from plone.app.dexterity.interfaces import ITypesContext, ITypeSchemaContext, ITypeSettings
from plone.app.dexterity.interfaces import ITypeStats

from plone.schemaeditor.browser.schema.traversal import SchemaContext

from plone.app.dexterity import MessageFactory as _


class TypeEditSubForm(crud.EditSubForm):
    """ Content type edit subform. Just here to use a custom template.
    """
    template = ViewPageTemplateFile('types_listing_row.pt')

class TypeEditForm(crud.EditForm):
    """ Content type edit form.  Just a normal CRUD form without the form title or edit button.
    """

    label = None
    editsubform_factory = TypeEditSubForm
    
    buttons = crud.EditForm.buttons.copy().omit('edit')
    handlers = crud.EditForm.handlers.copy()
    
    @button.buttonAndHandler(_(u'Clone'))
    def handleClone(self, action):
        selected = self.selected_items()
        
        if len(selected) > 1:
            self.status = _(u'Please select a single type to clone.')
        elif len(selected) == 1:
            id = selected[0][0]
            url = '%s/%s/@@clone' % (self.context.context.absolute_url(), id)
            self.request.response.redirect(url)
        else:
            self.status = _(u'Please select a type to clone.')

    @button.buttonAndHandler(_(u'Export Type Profiles'))
    def handleExport(self, action):
        selected = ",".join([items[0] for items in self.selected_items()])

        if len(selected) == 0:
            self.status = _(u'Please select types to export.')
        elif len(selected) > 0:
            url = '%s/@@types-export?selected=%s' % \
                (self.context.context.absolute_url(),
                 urllib.quote(selected))
            self.request.response.redirect(url)

    @button.buttonAndHandler(_(u'Export Schema Models'))
    def handleExportModels(self, action):
        selected = ",".join([items[0] for items in self.selected_items()])

        if len(selected) == 0:
            self.status = _(u'Please select types to export.')
        elif len(selected) > 0:
            url = '%s/@@models-export?selected=%s' % \
                (self.context.context.absolute_url(),
                 urllib.quote(selected))
            self.request.response.redirect(url)


class TypeSettingsAdapter(object):
    implements(ITypeSettings)
    adapts(IDexterityFTI)
    
    def __init__(self, context):
        self.context = context
    
    @property
    def id(self):
        return self.context.getId()
    
    @property
    def title(self):
        return self.context.title

    @property
    def description(self):
        description = self.context.description
        if not isinstance(description, unicode):
            description = description.decode('utf8')
        return description
    
    @property
    def container(self):
        return self.context.container


class TypeStatsAdapter(object):
    implements(ITypeStats)
    adapts(IDexterityFTI)
    
    def __init__(self, context):
        self.context = context
    
    @property
    def item_count(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        lengths = dict(catalog.Indexes['portal_type'].uniqueValues(withLengths=True))
        return lengths.get(self.context.getId(), 0)


class TypesListing(crud.CrudForm):
    """ The combined content type edit + add forms.
    """
    
    @lazy_property
    def description(self):
        if self.get_items():
            return _(u'The following custom content types are available for '
                     u'your site.')
        else:
            return _(u'Click the "Add Content Type" button to begin creating '
                     u' a new custom content type.')
    
    template = ViewPageTemplateFile('types_listing.pt')
    view_schema = field.Fields(ITypeSettings).select('title', 'description') + field.Fields(ITypeStats)
    addform_factory = crud.NullForm
    editform_factory = TypeEditForm
    
    def get_items(self):
        """ Look up all Dexterity FTIs via the component registry.
            (These utilities are created via an IObjectCreated handler for the DexterityFTI class,
            configured in plone.dexterity.)
        """
        ftis = getAllUtilitiesRegisteredFor(IDexterityFTI)
        return [(fti.__name__, fti) for fti in ftis]

    def remove(self, (id, item)):
        """ Remove a content type.
        """
        ttool = getToolByName(self.context, 'portal_types')
        ttool.manage_delObjects([id])

    def link(self, item, field):
        """ Generate links to the edit page for each type.
            (But only for types with schemata that can be edited through the web.)
        """
        if field == 'title':
            return '%s/%s' % (self.context.absolute_url(), item.__name__)

# Create a form wrapper so the form gets layout.
TypesListingPage = layout.wrap_form(TypesListing, label=_(u'Dexterity content types'))


class TypeSchemaContext(SchemaContext):
    implements(ITypeSchemaContext)
    
    fti = None
    schemaName = u''


class TypesContext(SimpleItem):
    """ This class represents the types configlet, and allows us to traverse
        through it to (a wrapper of) the schema of a particular type.
    """
    # IBrowserPublisher tells the Zope 2 traverser to pay attention to the
    # publishTraverse and browserDefault methods.
    implements(ITypesContext, IBrowserPublisher)
    
    def __init__(self, context, request):
        super(TypesContext, self).__init__(context, request)
        
        # make sure that breadcrumbs will be correct
        self.id = None
        self.Title = lambda: _(u'Dexterity Content Types')
        
        # turn off green edit border for anything in the type control panel
        request.set('disable_border', 1)
    
    def publishTraverse(self, request, name):
        """ 1. Try to find a content type whose name matches the next URL path element.
            2. Look up its schema.
            3. Return a schema context (an acquisition-aware wrapper of the schema).
        """
        try:
            fti = getUtility(IDexterityFTI, name=name)
        except ComponentLookupError:
            raise NotFound

        schema = fti.lookupSchema()
        schema_context = TypeSchemaContext(schema, request, name=name, title=fti.title).__of__(self)
        schema_context.fti = fti
        schema_context.schemaName = u''
        return schema_context

    def browserDefault(self, request):
        """ If we aren't traversing to a schema beneath the types configlet, we actually want to
            see the TypesListingPage.
        """
        return self, ('@@edit',)
