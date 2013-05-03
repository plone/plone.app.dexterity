from z3c.form import button

from plone.schemaeditor.browser.schema.listing import SchemaListing
from plone.schemaeditor.browser.schema.listing import ReadOnlySchemaListing

from plone.app.dexterity.browser.layout import TypeFormLayout
from plone.app.dexterity import MessageFactory as _

try:
    import plone.resourceeditor
    plone.resourceeditor  # avoid PEP 8 warning
    HAVE_RESOURCE_EDITOR = True
except ImportError:
    HAVE_RESOURCE_EDITOR = False


# We want to add a Plone-specific feature to the SchemaListing
# form from plone.schemaeditor. We'll do this by subclassing, then
# adding the plone-specific button for the ace model editor.

class EnhancedSchemaListing(SchemaListing):

    def handleModelEdit(self, action):
        self.request.response.redirect('@@modeleditor')

if HAVE_RESOURCE_EDITOR:
    but = button.Button("modeleditor", title=u'Edit XML Field Model')
    EnhancedSchemaListing.buttons += button.Buttons(but)
    handler = button.Handler(but, EnhancedSchemaListing.handleModelEdit)
    EnhancedSchemaListing.handlers.addHandler(but, handler)


class TypeFieldsPage(TypeFormLayout):
    label = _(u'Fields')

    @property
    def form(self):
        if self.context.fti.hasDynamicSchema:
            return EnhancedSchemaListing
        else:
            return ReadOnlySchemaListing
