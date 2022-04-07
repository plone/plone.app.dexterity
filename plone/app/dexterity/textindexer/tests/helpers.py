from plone.app.dexterity.textindexer.directives import SEARCHABLE_KEY
from plone.supermodel.utils import mergedTaggedValueList


def get_searchable_fields(iface):
    fieldnames = []

    for flag_iface, fieldname, value in mergedTaggedValueList(iface, SEARCHABLE_KEY):
        if flag_iface == iface and value:
            fieldnames.append(fieldname)

    return fieldnames
