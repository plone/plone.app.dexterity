"""Dynamic SearchableText index for dexterity content types
"""

from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.dexterity.textindexer import utils
from plone.app.dexterity.textindexer.directives import searchable
from plone.app.dexterity.textindexer.directives import SEARCHABLE_KEY
from plone.app.dexterity.textindexer.interfaces import IDexterityTextIndexFieldConverter
from plone.app.dexterity.textindexer.interfaces import IDynamicTextIndexExtender


utils.searchable(IBasic, "title")
utils.searchable(IBasic, "description")
