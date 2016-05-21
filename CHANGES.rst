Changelog
=========

2.3.0 (2016-05-21)
------------------

New features:

- The defaults of exclude from navigation is now obtained from a contextaware default factory, which value is obtained from an adapter.
  The default adapter returns False.
  An alternative adapter which defaults to True is provided but not registered.
  This change makes it possible to provide a custom context specific implementation.
  [jensens]

- Documentation: Shortnames added and some missing behaviors added.
  [jensens]

Bug fixes:

- Linebreaks in description are replaced with a space instead of vanishing it.
  Thus an editor can use them w/o having word glued together afterwards.
  [jensens]


2.2.0 (2016-04-28)
------------------

New:

- Assign short names for all behaviors as supported by plone.behavior.
  [jensens]

Fixes:

- Remove dups from TTW behavior FTI editor.
  [jensens]

- Fix problem in ConstrainTypesBehavior:
  when mode was ENABLED but only setLocallyAllowedTypes were set,
  then getImmediatelyAddableTypes returned None,
  but all consuming code expect it to return a list
  [jensens]

- Lookup of Content Type from MIME-Type for using right Plone Content Type to store Images (especially Tiff) correct as Images not Files.
  [loechel]


2.1.20 (2016-03-31)
-------------------

Fixes:

- Docs: Overhaul of chapter form-schema-hints.rst
  [jensens]

- Use the type ID in HTML classes in the type listing rather than titles.
  [davidjb]


2.1.19 (2016-02-26)
-------------------

Fixes:

- Rerelease due to possible brown bag release.  [maurits]


2.1.18 (2016-02-26)
-------------------

Fixes:

- Make the form permission validator a bit more generic so it can be used
  with non-AddForms.
  [alecm]


2.1.17 (2016-01-08)
-------------------

Fixes:

- Update event handler documentation.
  [jensens]

- Remove unused locales folder, translations are now in plone.app.locales.
  [vincentfretin]


2.1.16 (2015-12-03)
-------------------

Fixes:

- Fix wrong usage of MessageFactory
  [jensens]

- Use plone i18n domain
  [gforcada]

- Fix non existing self._request with schema.Choice value_type.
  [pcdummy]


2.1.15 (2015-10-28)
-------------------

New:

- Updated Traditional Chinese translation.
  [l34marr]

- Updated Brazil translations.
  [claytonc]

Fixes:

- Updated doc links in modeleditor.
  Issue `CMFPlone#1027`_.
  [pabo3000]

- Fixed icons in dexterity types list.
  Issues `CMFPlone#1013`_ and `CMFPlone#1151`_.
  [fgrcon]

- No longer rely on deprecated ``bobobase_modification_time`` from
  ``Persistence.Persistent``.
  [thet]

- Fixed typos in german translation. Thx bierik for reporting in
  Issue `dexterity#183`_.
  [jensens]

- Avoid re-adding the UUID on an upgrade step.
  [gforcada]


2.1.14 (2015-09-21)
-------------------

- Updated French translations.
  [enclope]


2.1.13 (2015-09-20)
-------------------

- Fixed issue with permission checker add form context.
  Issue `CMFPlone#1027`_.
  [alecm]

- Fixed ace editor javascript reference.
  Issue `CMFPlone#895`_.
  [rodfersou]

- Rerun i18ndude and updated German translation.
  [pabo3000]


2.1.12 (2015-09-15)
-------------------

- Remove unittest2 dependency.
  [gforcada]


2.1.11 (2015-09-11)
-------------------

- Updated basque translation
  [erral]


2.1.10 (2015-09-08)
-------------------

- Fix modeleditor for Plone 5
  [vangheem]


2.1.9 (2015-09-07)
------------------

- Restrict allowed field types to regular types (so plone.app.users do not show
  up)
  [ebrehault]


2.1.8 (2015-08-20)
------------------

- Avoid ``DeprecationWarning`` for ``getIcon`` and ``splitSchemaName``.
  [maurits]


2.1.7 (2015-07-18)
------------------

- Remove duplicate plone.app.z3cform pin in setup.py. This fixes https://github.com/plone/plone.app.dexterity/issues/167.
  [timo]

- Fixed an adapter path at custom add forms documentation.
  [brunobbbs]

- Change the category of the configlet to 'plone-content'.
  [sneridagh]

- Unlock before changing id (fixes
  https://github.com/plone/Products.CMFPlone/issues/623).
  [pbauer]

- Remove superfluous 'for'. Fixes plone/Products.CMFPlone#669.
  [fulv]

- Schemaeditor does not redirect anymore.
  [barichu]


2.1.6 (2015-06-05)
------------------

- change control panel title to be upper cased
  [vangheem]

- ignore protected fields when testing addability.
  [ebrehault]

- Update Japanese translation.
  [terapyon]


2.1.5 (2015-05-04)
------------------

- pat-modal pattern has been renamed to pat-plone-modal
  [jcbrand]


2.1.4 (2015-03-26)
------------------

- Add i18n:domain for Default Page Warning template.
  [l34marr]

- Update Traditional Chinese translation.
  [l34marr]


2.1.3 (2015-03-13)
------------------

- Code and docs housekeeping: pep8 et al, zca decorators, doc style.
  [jensens]

- Ensure the default creator value is a unicode string.
  [lentinj]

- Add facility to import type profiles in zip archives. Added button to
  types edit page. Import format is identical to export.
  [smcmahon]

- Update markup and javascript for Plone 5.
  [davisagli]

- Fix the IDexterityContainer view to make use of plone.app.contenttype's new
  listing view. Accessing it's macro needs the macro-caller's view variable set
  to the new listing view.
  [thet]


2.1.2 (2014-10-23)
------------------

- Added transifex-client configuration for manage the translations
  from Plone transifex organization [macagua].

- Updated Spanish translation [flamelcanto, macagua].

- Add validator to ensure expires date is after effective date.
  [benniboy]

- Remove line feeds and carrige returns from meta description and
  added upgrade step to do it for existing content
  [bosim]

- Fixed issue.
  Multiple (two or more) acquisition from parent was failing when
  user didn't have add permission on parent.
  [keul, cekk]


2.1.1 (2014-04-13)
------------------

- Add behavior to let an item's id be edited from its edit form
  (plone.app.dexterity.behaviors.id.ShortName).
  [davisagli]

- Cloning of types containing white space did not work, this commit
  fixes that bug.
  [bosim]


2.1.0 (2014-03-01)
------------------

- Don't throw an error if allowed_content_types is none or missing.
  Fix https://github.com/plone/plone.app.contenttypes/issues/91
  [pbauer]

- PLIP #13705: Remove <base> tag.
  [frapell]


2.0.11 (2013-12-07)
-------------------

- Fix bug where the type editor's inline javascript was mangled by diazo.
  [davisagli]

- Fixed Add view URL of cloned content type.
  Refs http://dev.plone.org/ticket/13776.
  [thomasdesvenain]

- Add robot testing environment and first robot test.
  [cedricmessiant]

- Better string normalization when setting type id from type title
  (change accented or special characters with corresponding letters).
  [cedricmessiant]

- Show a warning when editing the default page of a folder.
  [davisagli]



2.0.10 (2013-09-16)
-------------------

- Fix determination of allowed types so it checks permission in
  the context of the original folder when inheriting allowed
  types.
  [davisagli]


2.0.9 (2013-08-13)
------------------

- Add documentation for defaultFactory tag in XML ref.
  [smcmahon]

- Removed line breaks within documentation URLs in modeleditor.py.
  [smcmahon]

- Fixed XML export so that GenericSetup's parser can successfully parse it
  later on at install time.
  [zupo]

- Use @@ploneform-render-widget to render widgets in display mode.
  [cedricmessiant]

- Call the IBasic description field 'Summary' and give it
  help text that is actually helpful.
  [davisagli]

- Don't show the 'Allow Discussion' field on an item's default view.
  [davisagli]


2.0.8 (2013-05-23)
------------------

- Add XML Model Editor based on plone.resourceditor. If plone.resourceditor
  is available, this is exposed by an "Edit XML Field Model" button on
  the fields tab of a content type -- if the content type is editable TTW.
  [smcmahon]

- Added catalan translations [sneridagh]


2.0.7 (2013-04-09)
------------------

- Fix bug in determining whether to show the allowed contained type
  fields.
  [ericof]

- Let the behavior INameFromFileName also set the title from the filename
  if the type has such a field and it is left empty.
  [pbauer]

- Updated french translations.
  [thomasdesvenain]


2.0.6 (2013-04-06)
------------------

- Add missing translation strings.
  [vincentfretin]


2.0.5 (2013-04-06)
------------------

- Updated pt_BR translation [ericof]


2.0.4 (2013-03-05)
------------------

- Add zh_TW translation [TsungWei Hu]

- Add support for constraining container allowed content types using
  the "Restrictions" form in the add menu.  Merged from Patrick
  Gerken's (@do3cc) work in plone.app.contenttypes.
  [rpatterson]

- When a new type is added, redirect to the fields tab as the next view.
  [davisagli]

- Don't show the short name as a field on the type overview page.
  [davisagli]

- Remove the 'Container' checkbox when adding a new type, and default
  to creating a container.
  [davisagli]

- Tweaks to type control panel based on user testing.
  [davisagli]

- Set default language for a new content item based on the language of
  its container.
  [frapell]

- Fixed i18n of "Contents" in folder default view.
  [vincentfretin]

- Added Ukrainian translations
  [kroman0]


2.0.3 (2013-01-17)
------------------

- Nothing changed yet.


2.0.2 (2013-01-01)
------------------

- Added French translations
  [cedricmessiant]

- The behavior controlpanel now correctly invalidates any modified FTIs.
  [malthe]

- I18n improved by adding many missing strings
  [giacomos]

- better graphical integration in the control panel
  [giacomos]

- Allow discussion behavior added.
  [timo]


2.0.1 (2012-08-31)
------------------

- Update MANIFEST.in to correct packaging error.
  [esteele]


2.0 (2012-08-30)
----------------

- DC metadata fields are now correctly encoded and decoded (from byte
  strings to unicode and vice versa). Currently, UTF-8 is assumed.
  [malthe]

- Use lxml instead of elementtree.
  [davisagli]

- Use ViewPageTemplateFile from zope.browserpage.
  [hannosch]

- Add upgrade step to make sure that only uninstalling plone.app.intid will
  remove the intids utility.
  [davisagli]

- Fix traversal over the types context so that skin items used by widgets
  can be acquired.
  [davisagli]

- Provide an ``additionalSchemata`` property on the schema context so the
  schema editor can include a preview of fields from behaviors.
  [davisagli]

- Give a more explicit warning before deleting content types that have existing
  instances.
  [davisagli]

- Add validation to prevent giving a type the same name as an existing type.
  [davisagli]

- Make sure the title and description of new FTIs are stored encoded,
  and with a default i18n domain of 'plone'.
  [davisagli]

- Add overview tab for each type in the control panel.
  [davisagli]

- Added Sphinx source for the Dexterity Developer manual.
  [giacomos]

- Added Italian translation.
  [giacomos]

- Internationalized content type settings pages,
  I18N fixes,
  messages extraction,
  French translations.
  [thomasdesvenain]

- Added Spanish translation.
  [hvelarde]

- Install the profile from collective.z3cform.datetimewidget to enable the
  Jquery Tools date picker for date/time fields.
  [davisagli]

- Bugfix: Make sure type short names are validated.
  [davisagli]

- Bugfix: Fix display of type descriptions in the types control panel.
  [davisagli]

- Bugfix: Make sure subject can still be retrieved as unicode for the
  categorization behavior now that the Subject accessor returns a bytestring.
  [davisagli]

- Add intro message to Dexterity control panel.
  [jonstahl, davisagli]

- Grok support is now an optional "grok" extra. Use this if you want
  ``five.grok``, ``plone.directives.form``, and ``plone.directives.dexterity``.
  See the release notes for more information. The behaviors in this package
  were updated to work without using grok.
  [davisagli]

- plone.formwidget.autocomplete and plone.formwidget.contenttree are no longer
  included by default. See the release notes for more information.
  [davisagli]

- Moved the 'Related Items' behavior to plone.app.relationfield.
  plone.app.relationfield is no longer installed as a dependency. See the
  release notes for more information including how to update your package if it
  depends on relation support or the 'Related Items' behavior.
  IMPORTANT: You must install plone.app.relationfield on sites that are being
  upgraded from Dexterity 1.0 to Dexterity 2.0, or the site will break.
  [davisagli]

- Converted tests to plone.app.testing-based setup. The old PloneTestCase-based
  test case classes and layer are now deprecated.
  [davisagli]

- Remove ++resource++plone.app.dexterity.overlays.css from the CSS registry.
  [davisagli]

- Removed support for Plone 3 / CMF 2.1 / Zope 2.10.
  [davisagli]

- Update dependencies and imports as appropriate for Zope 2.12 & Zope 2.13
  [davisagli]

- Remove CDATA section from "browser\types_listing.pt" (in HTML5: allowed only in SVG/MathML namespaces).
  [kleist]

1.0 - 2011-05-20
----------------

- Fix publishing dates DateTime/datetime conversions so as not to drift by the
  timezone delta every save.
  [elro]

- Make sure cloned types get a new factory.
  [davisagli]

- Don't override overlay CSS in Plone 4.
  [davisagli]

- Fixed cloning of types with a period (.) in their short name.
  [davisagli]

- Allow specifying a type's short name when adding a type.
  [davisagli]

- Make sure the Basic metadata adapter accesses the content's title attribute
  directly so it doesn't get encoded. Also make sure encoded data can't be set
  via this adapter.
  [davisagli]

1.0rc1 - 2011-04-30
-------------------

- Added upgrade step to install new javascript from
  plone.formwidget.autocomplete
  [davisagli]

- Added basic support for making TTW changes to schemas defined in filesystem
  models and code. (Note: This feature will not actually work until some further
  changes are completed in plone.dexterity.)

  In order to support this change, the event handling to serialize schema changes
  was revised. We now register a single event handler for the SchemaModifiedEvent
  raised for the schema context. This allows us to keep track of the FTI
  that changes need to be serialized to on the schema context. The
  serializeSchemaOnFieldEvent and serializeSchemaOnSchemaEvent handlers were
  removed from the serialize module and replaced by serializeSchemaContext. The
  serializeSchema helper remains but is deprecated.
  [davisagli]

- Add MANIFEST.in.
  [WouterVH]

- Add "export" button to types editor. Exports GS-style zip archive of type
  info for selected types.
  [stevem]

- Fix old jquery alias in types_listing.pt. This closes
  http://code.google.com/p/dexterity/issues/detail?id=159
  [davisagli]

- Make display templates fill content-core on Plone 4.
  [elro]

- Add ids to the group fieldsets on display forms.
  [elro]

- Exclude from navigation behavior should be restricted to IDexterityContent.
  [elro]


1.0b4 - 2011-03-15
------------------

- Add a "Name from file name" behavior.
  [elro]

- Remove the NameFromTitle behavior factory, it is not necessary.
  [elro]

- Add "Next previous navigation" and "Next previous navigation toggle"
  behaviors.
  [elro]

- Add an "Exclude from navigation" behavior.
  [lentinj]

- Put the folder listing within a fieldset.
  [lentinj]


1.0b3 - 2011-02-11
------------------

- Add a navigation root behavior.
  [elro]

- Fix decoding error when an encoded description is stored in the FTI.
  [davisagli]

- Avoid empty <div class="field"> tag for title and description in
  item.pt and container.pt.
  [gaudenzius]

- Add locales structure for translations with cs , de, es, eu, fr, ja, nl, pt_BR
  [toutpt]

- Update french translation
  [toutpt]


1.0b2 - 2010-08-05
------------------

- Fix several XML errors in templates. Needed for Chameleon compatibility.
  [wichert]

- cloning a type through the dexterity UI in the control panel did not work
  if the type had a hyphen in it's name. This fixes
  http://code.google.com/p/dexterity/issues/detail?id=126
  [vangheem]


1.0b1 - 2010-04-20
------------------

- Require plone.app.jquerytools for the schema editor UI, and make sure it is
  installed when upgrading.
  [davisagli]

- Remove unused schemaeditor.css.
  [davisagli]

- Omit the metadata fields except on edit and add forms.
  [davisagli]

- Enable the "Name from title" behavior for new types, by default.
  [davisagli]

- Include plone.formwidget.namedfile so that File upload and Image fields are
  available out of the box.  You must explicitly include z3c.blobfile in your
  environment if you want blob-based files.
  [davisagli]

- Added a DexterityLayer that can be used in tests.
  [davisagli]

- Fix issue with the BehaviorsForm accidentally polluting the title of the
  z3c.form EditForm 'Apply' button.
  [davisagli]

- Add upgrades folder and make sure plone.app.z3cform profile gets installed
  on upgrades from previous versions of Dexterity.
  [davisagli]

- Depend on the plone.app.z3cform profile, to make sure the Plone browser layer
  for z3c.form gets installed.
  [davisagli]

- Avoid relying on acquisition to get the portal_url for links in the type
  listing table.
  [davisagli]


1.0a7 - 2010-01-08
------------------

- Make sure the Dublin Core fieldsets appear in the same order as they
  do in AT content.
  [davisagli]

- Make sure the current user is loaded as the default creator for the
  IOwnership schema in an add form.
  [davisagli]

- Include behavior descriptions on the behavior edit tab.
  [davisagli]

- IBasic behavior: set missing_value of description-field to u'' . The
  description should never be None (live_search would not work any more).
  [jbaumann]

- Fix issue where traversing to a nonexistent type name in the types control
  panel did not raise NotFound.
  [davisagli]

- Make it possible to view the fields of non-editable schemata.
  [davisagli]

- Tweaks to the tabbed_forms template used for the types control panel.
  [davisagli]


1.0a6 - 2009-10-12
------------------

- Add plone.app.textfield as a dependency. We don't use it directly in this
  package, but users of Dexterity should have it installed and available.
  [optilude]

- Use some default icons for new types.
  [davisagli]

- Show type icons in type listing if available.
  [davisagli]

- Removed 'container' field from the types listing in the control panel
  (it wasn't working).
  [davisagli]

- Add message factories to titles and descriptions of metadata schema fields.
  Fixes http://code.google.com/p/dexterity/issues/detail?id=75.
  [optilude]

- Patch listActionInfos() instead of listActions() in order to get the
  folder/add category into the actions list. This avoids a problem with
  the 'actions.xml' export handler exporting the folder/add category
  incorrectly. Fixes http://code.google.com/p/dexterity/issues/detail?id=78
  [optilude]


1.0a5 - 2009-07-26
------------------

- Explicitly include overrides.zcml from plone.app.z3cform.
  [optilude]


1.0a4 - 2009-07-12
------------------

- Changed API methods and arguments to mixedCase to be more consistent with
  the rest of Zope. This is a non-backwards-compatible change. Our profuse
  apologies, but it's now or never. :-/

  If you find that you get import errors or unknown keyword arguments in your
  code, please change names from foo_bar too fooBar, e.g. serialize_schema()
  becomes serializeSchema().
  [optilude]


1.0a3 - 2009-06-07
------------------

- Updated use of <plone:behavior /> directive to match plone.behavior 1.0b4.
  [optilude]


1.0a2 - 2009-06-01
------------------

- Remove superfluous <includeOverrides /> in configure.zcml which would cause
  a problem when the package is loaded via z3c.autoinclude.plugin
  [optilude]


1.0a1 - 2009-05-27
--------------------

- Initial release

.. _`dexterity#183`: https://github.com/plone/plone.app.dexterity/issues/183

.. _`CMFPlone#895`: https://github.com/plone/Products.CMFPlone/issues/895
.. _`CMFPlone#1013`: https://github.com/plone/Products.CMFPlone/issues/1013
.. _`CMFPlone#1027`: https://github.com/plone/Products.CMFPlone/issues/1027
.. _`CMFPlone#1151`: https://github.com/plone/Products.CMFPlone/issues/1151
.. _`CMFPlone#1207`: https://github.com/plone/Products.CMFPlone/issues/1207
