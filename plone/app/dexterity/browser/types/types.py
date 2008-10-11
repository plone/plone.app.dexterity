from zope.component import getAllUtilitiesRegisteredFor
from plone.z3cform.crud import crud
from plone.dexterity.interfaces import IDexterityFTI

class TypesListing(crud.CrudForm):
    
    def get_items(self):
        return []