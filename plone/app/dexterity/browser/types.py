from OFS.SimpleItem import SimpleItem

from zope.interface import Interface, implements
from zope.component import getAllUtilitiesRegisteredFor, getUtility, ComponentLookupError
from zope.publisher.interfaces.browser import IBrowserPublisher
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope import schema

from z3c.form import field
from plone.z3cform import layout
from plone.z3cform.crud import crud

from Products.CMFCore.utils import getToolByName
from plone.i18n.normalizer.interfaces import IIDNormalizer

from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.fti import DexterityFTI
from plone.app.dexterity.interfaces import ITypesContext, ITypeSchemaContext
from plone.schemaeditor.browser.schema.schema import SchemaContext
import plone.schemaeditor.browser

try:
    from Products.CMFPlone.factory import _IMREALLYPLONE4
    PLONE40 = True
except ImportError:
    PLONE40 = False

class ITypeSettings(Interface):
    """ Define the fields for the content type add form
    """
    
    title = schema.TextLine(
        title = u'Type Name'
        )

    description = schema.Text(
        title = u'Description',
        required = False
        )

    container = schema.Bool(
        title = u'Container?',
        description = u'If yes, items of this type will be able to contain other items.',
        required = True,
        default = False,
        )

class TypeAddForm(crud.AddForm):
    """ Content type add form.  Just a normal CRUD add form with a custom template to show a form title.
    """
    
    label = u'Add Content Type'
    template = ViewPageTemplateFile('titledform.pt', _prefix=plone.schemaeditor.browser.__dict__)


class TypeEditSubForm(crud.EditSubForm):
    """ Content type edit subform. Just here to use a custom template.
    """
    template = ViewPageTemplateFile('types_listing_row.pt')

class TypeEditForm(crud.EditForm):
    """ Content type edit form.  Just a normal CRUD form without the form title or edit button.
    """

    label = None
    
    def __init__(self, context, request):
        super(crud.EditForm, self).__init__(context, request)
        self.buttons = self.buttons.copy().omit('edit')


class TypesListing(crud.CrudForm):
    """ The combined content type edit + add forms.
    """
    
    view_schema = field.Fields(ITypeSettings).omit('container')
    add_schema = ITypeSettings
    
    addform_factory = TypeAddForm
    editform_factory = TypeEditForm
    
    def get_items(self):
        """ Look up all Dexterity FTIs via the component registry.
            (These utilities are created via an IObjectCreated handler for the DexterityFTI class,
            configured in plone.dexterity.)
        """
        ftis = getAllUtilitiesRegisteredFor(IDexterityFTI)
        return [(fti.__name__, fti) for fti in ftis]

    def add(self, data):
        """ Add a new DexterityFTI.
            
            A URL normalizer, normally from plone.i18n, is used to sanitize the type's title.
        """
        
        id = getUtility(IIDNormalizer).normalize(data['title'])
        # XXX validation

        fti = DexterityFTI(id)
        fti.id = id
        data['behaviors'] = 'plone.app.dexterity.behaviors.metadata.IDublinCore'
        data['model_source'] = """
<model xmlns="http://namespaces.plone.org/supermodel/schema">
    <schema>
    </schema>
</model>
"""
        if data['container']:
            data['klass'] = 'plone.dexterity.content.Container'
            del data['container']
            icon = 'folder_icon'
        else:
            icon = 'document_icon'
        # XXX should probably copy icons into p.a.d and use them from here
        if PLONE40:
            data['icon_expr'] = 'string:${portal_url}/' + icon + '.png'
        else:
            data['content_icon'] = icon + '.gif'
        fti.manage_changeProperties(**data)

        ttool = getToolByName(self.context, 'portal_types')
        ttool._setObject(id, fti)

    def remove(self, (id, item)):
        """ Remove a content type.
        """
        ttool = getToolByName(self.context, 'portal_types')
        ttool.manage_delObjects([id])
        
        # XXX What to do with existing content items?

    def link(self, item, field):
        """ Generate links to the edit page for each type.
            (But only for types with schemata that can be edited through the web.)
        """
        if field == 'title':
            return '%s/%s' % (self.context.absolute_url(), item.__name__)

# Create a form wrapper so the form gets layout.
TypesListingPage = layout.wrap_form(TypesListing, label=u'Dexterity content types')

class TypeSchemaContext(SchemaContext):
    implements(ITypeSchemaContext)
    
    fti = None
    
    def setFTI(self, fti):
        self.fti = fti


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
        self.Title = lambda: u'Dexterity Content Types'
        
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
            return None

        schema = fti.lookupSchema()
        schema_context = TypeSchemaContext(schema, request, name=name, title=fti.title).__of__(self)
        schema_context.setFTI(fti)
        return schema_context

    def browserDefault(self, request):
        """ If we aren't traversing to a schema beneath the types configlet, we actually want to
            see the TypesListingPage.
        """
        return self, ('@@edit',)
