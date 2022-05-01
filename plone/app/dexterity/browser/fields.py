from plone.app.dexterity import _
from plone.app.dexterity.browser.layout import TypeFormLayout
from plone.schemaeditor.browser.schema.listing import ReadOnlySchemaListing
from plone.schemaeditor.browser.schema.listing import SchemaListing
from z3c.form import button

import pkg_resources


# We want to add a Plone-specific feature to the SchemaListing
# form from plone.schemaeditor. We'll do this by subclassing, then
# adding the plone-specific button for the ace model editor.


class EnhancedSchemaListing(SchemaListing):
    def handleModelEdit(self, action):
        self.request.response.redirect("@@modeleditor")


if pkg_resources.get_distribution("plone.resourceeditor"):
    but = button.Button("modeleditor", title="Edit XML Field Model")
    EnhancedSchemaListing.buttons += button.Buttons(but)
    handler = button.Handler(but, EnhancedSchemaListing.handleModelEdit)
    EnhancedSchemaListing.handlers.addHandler(but, handler)


class TypeFieldsPage(TypeFormLayout):
    label = _("Fields")

    @property
    def form(self):
        if self.context.fti.hasDynamicSchema:
            return EnhancedSchemaListing
        else:
            return ReadOnlySchemaListing
