# -*- coding: utf-8 -*-
"""Dynamic SearchableText index for dexterity content types
"""

from plone.app.dexterity.textindexer import utils
from plone.app.dexterity.behaviors.metadata import IBasic

from plone.app.dexterity.textindexer.interfaces import IDynamicTextIndexExtender, IDexterityTextIndexFieldConverter

from plone.app.dexterity.textindexer.directives import searchable, SEARCHABLE_KEY

utils.searchable(IBasic, 'title')
utils.searchable(IBasic, 'description')
