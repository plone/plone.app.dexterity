from Products.CMFCore.utils import getToolByName

import logging


logger = logging.getLogger("plone.app.dexterity")


def cleanup_portal_actions(context):
    # Our actions.xml registers dexterity-types as controlpanel item.  But this
    # is what controlpanel.xml is for.  So remove it.
    # https://github.com/plone/plone.app.dexterity/issues/218
    actions_tool = getToolByName(context, "portal_actions")
    main_category = "controlpanel"
    sub_category = "controlpanel_addons"
    action_name = "dexterity-types"

    # Lookup for action in category.
    main = getattr(actions_tool, main_category, None)
    if main is None:
        logger.info("%s category was already removed.", main_category)
        return
    sub = getattr(main, sub_category, None)
    if sub is None:
        logger.info("%s category was already removed.", sub_category)
        return
    if action_name not in sub.objectIds():
        logger.info("%s action was already removed.", action_name)
        return
    sub._delObject(action_name)
    logger.info("Removed %s from portal_actions.", action_name)

    # Cleanup empty categories.
    if len(sub.objectIds()) > 0:
        return
    main._delObject(sub_category)
    logger.info("Removed empty %s action sub category.", sub_category)
    if len(main.objectIds()) > 0:
        return
    actions_tool._delObject(main_category)
    logger.info("Removed empty %s action main category.", main_category)
