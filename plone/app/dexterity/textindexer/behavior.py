"""IDexterityTextIndexer    dexterity behavior interface for enabling
the dexteritytextindexer
"""
from zope.interface import Interface


class IDexterityTextIndexer(Interface):
    """Dexterity behavior interface for enabling the dynamic SearchableText
    indexer on a content type.
    """
