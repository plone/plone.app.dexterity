import re

# zope 2
import Acquisition

# zope 3
from zope.interface import implements
from zope.component import getMultiAdapter
from zope.traversing.interfaces import ITraversable
from zope.publisher.browser import BrowserPage

# dexterity
from plone.app.dexterity.interfaces import IFieldEditingContext

interface_name_re = re.compile(r'^([a-z0-9._]+)\.([a-z0-9._]+)$', re.IGNORECASE)

class FieldView(Acquisition.Implicit, BrowserPage):
    """ wrapper for published zope 3 schema fields
    """
    implements(IFieldEditingContext)
    
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, context, request):
        super(FieldView, self).__init__(context, request)
        self.field = self.context
        self.__name__ = self.field.__name__
        
class SchemaTraverser(object):
    """ traverser for ++schema++ namespace
    """
    
    implements(ITraversable)
    
    def __init__(self, context, request):
        self.context = context
        self.request = request
    
    def traverse(self, name, ignored):
        m = interface_name_re.match(name)
        try:
            # XXX security hole?  but this traversal isn't meant to last
            exec "from %s import %s as target_interface" % (m.group(1), m.group(2))
        except ImportError:
            return None
        return getMultiAdapter((target_interface, self.request), name=u'schema').__of__(self.context)
