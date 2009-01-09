def initialize(context):
    from plone.app.dexterity.overrides import apply_patches
    apply_patches()