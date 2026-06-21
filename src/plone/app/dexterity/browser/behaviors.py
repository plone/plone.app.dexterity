import zope.deferredimport


zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Please use from plone.app.layout.dexterity.behaviors import "
    "BehaviorConfigurationAdapter, TypeBehaviorsForm, TypeBehaviorsPage, "
    "behaviorConfigurationModified instead.",
    TTW_BEHAVIOR_BLACKLIST="plone.app.layout.dexterity.behaviors:TTW_BEHAVIOR_BLACKLIST",
    behaviorConfigurationModified="plone.app.layout.dexterity.behaviors:behaviorConfigurationModified",
    BehaviorConfigurationAdapter="plone.app.layout.dexterity.behaviors:BehaviorConfigurationAdapter",
    TypeBehaviorsForm="plone.app.layout.dexterity.behaviors:TypeBehaviorsForm",
    TypeBehaviorsPage="plone.app.layout.dexterity.behaviors:TypeBehaviorsPage",
)
