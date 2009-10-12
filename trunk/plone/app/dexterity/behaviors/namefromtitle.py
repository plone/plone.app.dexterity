from zope.interface import implements
from plone.app.content.interfaces import INameFromTitle

class NameFromTitle(object):
    implements(INameFromTitle)
    
    def __init__(self, context):
        self.context = context
    
    @property
    def title(self):
        return self.context.title
