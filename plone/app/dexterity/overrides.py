# Forward compatibility with CMF 2.2.
# XXX: Should be removed when Plone moves to CMF 2.2

#   1. Monkey patch TypesTool to include FTI actions for add views in the
#       return value from listActions()

from Products.CMFCore.interfaces import IAction
def TypesTool_listActions(self, info=None, object=None):
    """ List all the actions defined by a provider.
    """
    actions = list( self._actions )

    if object is None and info is not None:
        object = info.object
    if object is not None:
        type_info = self.getTypeInfo(object)
        if type_info is not None:
            actions.extend( type_info.listActions(info, object) )

    # XXX: Prior to CMF 2.2, FTI's are not expected to be actions and so the
    # next two lines are missing.
    add_actions = [ ti for ti in self.objectValues()
                    if IAction.providedBy(ti) and ti.add_view_expr ]
    actions.extend(add_actions)

    return actions

#   2. Register the ++add++ traversal adapter from CMF 2.2

from zope.component import adapts
from zope.component import queryMultiAdapter
from zope.interface import implements
from zope.interface import Interface
from zope.traversing.interfaces import ITraversable
from zope.traversing.interfaces import TraversalError

from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName

class AddViewTraverser(object):

    """Add view traverser.
    """

    adapts(IFolderish, Interface)
    implements(ITraversable)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def traverse(self, name, ignored):       
        ttool = getToolByName(self.context, 'portal_types')
        ti = ttool.getTypeInfo(name)
        if ti is not None:
            add_view = queryMultiAdapter((self.context, self.request, ti),
                                         name=ti.factory)
            if add_view is None:
                add_view = queryMultiAdapter((self.context, self.request, ti))
            if add_view is not None:
                add_view.__name__ = ti.factory
                return add_view.__of__(self.context)

        raise TraversalError(self.context, name)

#   3. Monkey patch ActionInfo constructor to work around a bug in CMF 2.1

from UserDict import UserDict
def ActionInfo___init__(self, action, ec):
    if isinstance(action, dict):
        lazy_keys = []
        UserDict.__init__(self, action)
        if 'name' in self.data:
            self.data.setdefault( 'id', self.data['name'].lower() )
            self.data.setdefault( 'title', self.data['name'] )
            del self.data['name']
        self.data.setdefault( 'url', '' )
        self.data.setdefault( 'category', 'object' )
        self.data.setdefault( 'visible', True )
        self.data['available'] = True
    else:
        # if action isn't a dict, it has to implement IAction
        (lazy_map, lazy_keys) = action.getInfoData()
        UserDict.__init__(self, lazy_map)

    # XXX: In CMF 2.1, this incorrectly says self.data['allowed'] = True,
    # overriding the value from the lazy map
    self.data.setdefault('allowed', True)
    permissions = self.data.pop( 'permissions', () )
    if permissions:
        self.data['allowed'] = self._checkPermissions
        lazy_keys.append('allowed')

    self._ec = ec
    self._lazy_keys = lazy_keys
    self._permissions = permissions

#   4. Register override view for @@folder_factories to use actions instead
#       of constructing URLs manually

# BBB support for plone.app.content < 2.0
try:
    from plone.app.layout.content.folderfactories import FolderFactoriesView
except ImportError:
    from plone.app.content.browser.folderfactories import FolderFactoriesView

from zope.component import getMultiAdapter, queryUtility
from zope.i18n import translate
from plone.i18n.normalizer.interfaces import IIDNormalizer
from urllib import quote_plus
from Acquisition import aq_inner

class ActionAwareFolderFactoriesView(FolderFactoriesView):
    
    def addable_types(self, include=None):
        """Return menu item entries in a TAL-friendly form.
        
        Pass a list of type ids to 'include' to explicitly allow a list of
        types.
        """
        
        # XXX: When Plone moves to CMF 2.1, all addable types should provide
        #  IAction and give us an action in the 'folder/add' category. This
        #  means that the code below could be simplified quite a lot. When no
        #  add_view_expr is set, the url will be '', which should then
        #  delegate to createObject.
        
        context = aq_inner(self.context)
        request = self.request
        
        results = []
        
        portal_state = getMultiAdapter((context, request), name='plone_portal_state')
        portal_url = portal_state.portal_url()
        
        addContext = self.add_context()
        baseUrl = addContext.absolute_url()
        
        allowedTypes = addContext.allowedContentTypes()
        
        # XXX: This is calling a pyscript (which we encourage people to customise TTW)
        exclude = addContext.getNotAddableTypes()

        # XXX: Added to support CMF 2.2 style add view actions
        context_state = getMultiAdapter((context, request), name='plone_context_state')
        addActionsById = dict([(a['id'], a['url'],) 
                                for a in context_state.actions().get('folder/add', []) 
                                if a['available'] and a['allowed']])

        # If there is an add view available, use that instead of createObject
        # Note: that this depends on the convention that the add view and the
        # factory have the same name, and it still only applies where there
        # is an FTI in portal_types to begin with. Alas, FTI-less content
        # is pretty much a no-go in CMF.
        addingview = queryMultiAdapter((addContext, request), name='+')
        idnormalizer = queryUtility(IIDNormalizer)
        for t in allowedTypes:
            typeId = t.getId()
            if typeId not in exclude and (include is None or typeId in include):
                cssId = idnormalizer.normalize(typeId)
                cssClass = 'contenttype-%s' % cssId
                factory = t.factory
                
                # XXX: Added to support CMF 2.2 style add view actions
                if addActionsById.get(typeId, ''): # we have a non-empty URL
                    url = addActionsById[typeId]
                elif addingview is not None and \
                   queryMultiAdapter((addingview, self.request), name=factory) is not None:
                    url = '%s/+/%s' % (baseUrl, factory,)
                else:
                    url = '%s/createObject?type_name=%s' % (baseUrl, quote_plus(typeId),)
                icon = t.getIcon()
                if icon:
                    icon = '%s/%s' % (portal_url, icon)

                results.append({ 'id'           : typeId,
                                 'title'        : t.Title(),
                                 'description'  : t.Description(),
                                 'action'       : url,
                                 'selected'     : False,
                                 'icon'         : icon,
                                 'extra'        : {'id' : cssId, 'separator' : None, 'class' : cssClass},
                                 'submenu'      : None,
                                })

        # Sort the addable content types based on their translated title
        results = [(translate(ctype['title'], context=request), ctype) for ctype in results]
        results.sort()
        results = [ctype[-1] for ctype in results]

        return results

#   5. Register an override adapter for the add menu item used when only one
#      thing is addable to type folder

from plone.app.contentmenu.menu import FactoriesSubMenuItem

class ActionAwareFactoriesSubMenuItem(FactoriesSubMenuItem):
    
    @property
    def action(self):
        addContext = self._addContext()
        if self._hideChildren():
            (addContext, fti) = self._itemsToAdd()[0]
            
            # XXX: Added check for folder/add action
            ftiId = fti.getId()
            for a in self.context_state.actions().get('folder/add', []):
                if a['id'] == ftiId:
                    actionUrl = a['url']
                    if actionUrl:
                        return actionUrl
            
            baseUrl = addContext.absolute_url()
            addingview = queryMultiAdapter((addContext, self.request), name='+')
            if addingview is not None:
                addview = queryMultiAdapter((addingview, self.request), name=fti.factory)
                if addview is not None:
                    return '%s/+/%s' % (baseUrl, fti.factory,)
            return '%s/createObject?type_name=%s' % (baseUrl, quote_plus(fti.getId()),)
        else:
            return '%s/folder_factories' % self.context_state.folder().absolute_url()



def apply_patches():
    from Products.CMFCore.TypesTool import TypesTool
    TypesTool.listActions = TypesTool_listActions
    
    from Products.CMFCore.ActionInformation import ActionInfo
    ActionInfo.__init__ = ActionInfo___init__