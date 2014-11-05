Standard behaviors
===================

**A list of common behaviors that ship with Dexterity**

Dexterity ships with several standard behaviors. The following table
shows the interfaces you can list in the FTI *behaviors* properties and
the resultant form fields and interfaces.

+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| Interface                                                         | Description                                                                                                                                          |
+===================================================================+======================================================================================================================================================+
| plone.app.dexterity.behaviors.metadata.IBasic                     | Basic metadata: Adds title and description fields.                                                                                                   |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.metadata.ICategorization            | Categorization: Adds keywords and language fields.                                                                                                   |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.metadata.IPublication               | Date range: Adds effective date and expiration date fields.                                                                                          |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.metadata.IOwnership                 | Ownership: Adds creator, contributor, and rights fields.                                                                                             |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.metadata.IDublinCore                | Dublin Core metadata: Adds standard metadata fields (equals Basic metadata + Categorization + Effective range + Ownership)                           |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.content.interfaces.INameFromTitle                       | Name from title: Automatically generate short URL name for content based on its initial title. Not a form field provider.                            |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.filename.INameFromFileName          | Name from file name: Automatically generate short URL name for content based on its primary field file name                                          |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.layout.navigation.interfaces.INavigationRoot            | Navigation root: Make all items of this type a navigation root                                                                                       |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation  | Exclude From navigation: Allow items to be excluded from navigation                                                                                  |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.nextprevious.INextPreviousToggle    | Next previous navigation toggle: Allow items to have next previous navigation enabled                                                                |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.discussion.IAllowDiscussion         | Allow discussion: Allow discussion on this item                                                                                                      |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.id.IShortName                       | Short name: Gives the ability to rename an item from its edit form.                                                                                  |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.nextprevious.INextPreviousEnabled   | Next previous navigation: Enable next previous navigation for all items of this type                                                                 |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| Products.CMFPlone.interfaces.constrains.ISelectableConstrainTypes | Folder Addable Constrains: Restrict the content types that can be added to folderish content                                                         |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.relationfield.behavior.IRelatedItems                    | Adds the *Related items* field to the *Categorization* fieldset.                                                                                     |
+-------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------+
