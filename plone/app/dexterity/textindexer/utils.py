from plone.app.dexterity.textindexer.directives import SEARCHABLE_KEY
from zope import schema


def searchable(iface, field_name):
    """
    mark a field in existing iface as searchable
    """

    if schema.getFields(iface).get(field_name) is None:
        dottedname = ".".join((iface.__module__, iface.__name__))
        raise AttributeError(f'{dottedname} has no field "{field_name}"')

    store = iface.queryTaggedValue(SEARCHABLE_KEY)
    if store is None:
        store = []
    store.append((iface, field_name, "true"))
    iface.setTaggedValue(SEARCHABLE_KEY, store)


def no_longer_searchable(iface, field_name):
    """Removes a "searchable" mark from a previously marked
    field.
    """

    if schema.getFields(iface).get(field_name) is None:
        dottedname = ".".join((iface.__module__, iface.__name__))
        raise AttributeError(f'{dottedname} has no field "{field_name}"')

    store = iface.queryTaggedValue(SEARCHABLE_KEY)
    if store is None:
        return False

    key = (iface, field_name, "true")
    if key not in store:
        return False

    store.remove(key)
    iface.setTaggedValue(SEARCHABLE_KEY, store)
    return True
