Standard behaviors 
===================

**A list of common behaviors that ship with Dexterity**

Dexterity ships with several standard behaviors. The following table
shows the interfaces you can list in the FTI *behaviors* properties and
the resultant form fields and interfaces.

+----------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Interface                                                | Description                                                                                                                                                   |
+==========================================================+===============================================================================================================================================================+
| plone.app.dexterity.behaviors.metadata.IBasic            | Adds the standard title and description fields                                                                                                                |
+----------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.metadata.ICategorization   | Adds the *Categorization* fieldset and fields                                                                                                                 |
+----------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.metadata.IPublication      | Adds the *Dates* fieldset and fields                                                                                                                          |
+----------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.metadata.IOwnership        | Adds the *Ownership* fieldset and fields                                                                                                                      |
+----------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.metadata.IDublinCore       | A single behavior that includes all the Dublin Core fields of the behaviors above                                                                             |
+----------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.content.interfacess.INameFromTitle             | Causes the content item’s name to be calculated from the *title* attribute (which you must ensure is present and correctly set). Not a form field provider.   |
+----------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+
| plone.app.dexterity.behaviors.metadata.IRelatedItems     | Adds the *Related items* field to the *Categorization* fieldset.                                                                                              |
+----------------------------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------+


