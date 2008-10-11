import Acquisition
from OFS.interfaces import IItem
from zope.interface import Interface, implements
from zope.component import getAllUtilitiesRegisteredFor, getUtility, getMultiAdapter, ComponentLookupError
from zope.publisher.interfaces.browser import IBrowserPage
from zope.publisher.browser import BrowserPage
from zope import schema
from zope.schema.interfaces import IField
from z3c.form import field
from plone.z3cform import layout
from plone.z3cform.crud import crud
from plone.dexterity.interfaces import IDexterityFTI
from zope.publisher.browser import BrowserPage
from plone.app.dexterity.interfaces import ITypesEditingContext

class RemoveOnlyForm(crud.EditForm):
    
    def __init__(self, context, request):
        super(crud.EditForm, self).__init__(context, request)
        self.buttons = self.buttons.copy().omit('edit')

class TypesListing(crud.CrudForm):
    
    view_schema = field.Fields(IItem).select('title')
    addform_factory = crud.NullForm
    editform_factory = RemoveOnlyForm
    
    def get_items(self):
        ftis = getAllUtilitiesRegisteredFor(IDexterityFTI)
        return [(fti.__name__, fti) for fti in ftis]

    def add(self, data):
        return None

    def remove(self, (id, item)):
        return None

    def link(self, item, field):
        if item.has_dynamic_schema:
            return '%s/@@%s/%s' % (self.context.absolute_url(), self.__name__, item.__name__)
        else:
            return None
            
TypesListingPage = layout.wrap_form(TypesListing)
        
class TypesListingContext(Acquisition.Implicit, BrowserPage):
    implements(ITypesEditingContext)
        
    __allow_access_to_unprotected_subobjects__ = 1
        
    def publishTraverse(self, request, name):
        try:
            fti = getUtility(IDexterityFTI, name=name)
        except ComponentLookupError:
            return None
            
        if not fti.has_dynamic_schema:
            # XXX more verbose error?
            raise TypeError, u'This dexterity type cannot be edited through the web.'
        
        model = fti.lookup_model()
        schema = model.schema
        
        return getMultiAdapter((schema, self.request), name=u'schema').__of__(self)

    def browserDefault(self, request):
        return self, ('@@edit',)
