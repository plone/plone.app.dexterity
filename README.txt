Introduction
============

This package integrates the Dexterity_ content type system into the Plone_
content management system.

.. _Dexterity: http://plone.org/products/dexterity
.. _Plone: http://plone.org

plone.app.dexterity contains code to handle four major areas of concern:

 * Dexterity Types control panel
 * Default behaviors
 * Installation of dependencies
 * Backports of several upstream changes


Dexterity Types control panel
-----------------------------

Installing this package adds a control panel called "Dexterity Content Types".
This control panel allows you to:

 * Add and remove Dexterity content types
 * Modify the schema of a Dexterity content type
 * Assign behaviors to a Dexterity content type


Default behaviors
-----------------

Several behaviors are included that can be enabled for a content type to make
it behave similarly to a standard ATContentTypes-based content type.  These
behaviors can be enabled via the Behaviors tab for a type in the Dexterity
Types control panel, or via the behaviors setting on the type's FTI in
portal_types in the ZMI.

Dublin Core metadata (plone.app.dexterity.behaviors.metadata.IDublinCore)
  This behavior includes the standard Dublin Core metadata fields.  Enabling
  it is equivalent to enabling the Basic Metadata, Categorization, Effective
  Range, and Ownership behaviors.

Basic Metadata (plone.app.dexterity.behaviors.metadata.IBasic)
  Includes title and description fields.

Categorization (plone.app.dexterity.behaviors.metadata.ICategorization)
  Includes subject and language fields.

Effective Range (plone.app.dexterity.behaviors.metadata.IPublication)
  Includes effective date and expiration date fields.

Ownership (plone.app.dexterity.behaviors.metadata.IOwnership)
  Includes creator, contributor, and copyright fields.

Related Items (plone.app.dexterity.behaviors.related.IRelatedItems)
  Includes a z3c.relationfield-based related items field.

Name From Title (plone.app.content.interfaces.INameFromTitle)
  Items with this behavior enabled will automatically get an id based on their
  title when the item is saved for the first time.


Installation of dependencies
----------------------------

Installing this package should also install everything else that you need to
use Dexterity within Plone.  In particular, it will pull in the following
packages as dependencies:

 * z3c.form
 * plone.z3cform
 * plone.app.z3cform
 * plone.supermodel
 * plone.dexterity
 * plone.directives.form
 * plone.directives.dexterity
 * plone.schemaeditor
 * plone.formwidget.autocomplete
 * plone.formwidget.contenttree
 * plone.app.relationfield


Backports of upstream changes
-----------------------------

Dexterity relies on several new features in CMF_ and plone.app.content that
are not included in existing Plone 3.x releases:

 * The ability to specify an expression for the add view on an FTI.
 * The ability to traverse to an add view in the ++add++ namespace.
 * Building the type factory menu based on actions.

.. _CMF: http://www.zope.org/Products/CMF

plone.app.dexterity applies these changes as monkey patches so that Dexterity
can be used in Plone 3.x.  See overrides.zcml and overrides.py for details.
