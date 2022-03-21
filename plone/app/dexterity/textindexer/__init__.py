# -*- coding: utf-8 -*-
"""Dynamic SearchableText index for dexterity content types
"""

from collective.dexteritytextindexer import utils
from plone.app.dexterity.behaviors.metadata import IBasic

utils.searchable(IBasic, 'title')
utils.searchable(IBasic, 'description')
