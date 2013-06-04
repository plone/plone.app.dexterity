Release Notes
=============

Dexterity 2.0 is a major release of Dexterity. It has focused on getting
Dexterity included in Plone core, by cleaning things up and making
dependencies that are not ready for primetime optional.

Grok-style configuration no longer included by default
------------------------------------------------------

Dexterity 1.0 included ``five.grok`` to allow configuring components via
Python directives rather than in separate XML-based ZCML files.  It also
included two packages, ``plone.directives.form`` and
``plone.directives.dexterity``, to provide some grok-style directives for
Dexterity-specific features.

The Dexterity authors still like grok and believe it makes it easier to learn
how to customize Plone.  However, it has been turned into an optional feature
so that Dexterity has a chance to enter Plone core even if the Plone framework
team doesn't want to add grok to the already complex stack.

To include these three grok-related packages when you install Dexterity,
enable the "grok" extra::

  [instance]
  eggs =
      plone.app.dexterity [grok]

By the way, a number of schema directives from ``plone.directives.form`` that
used to require grok to work have been reimplemented so that they work without
grok. In particular, the ``Schema`` class and the ``model``, ``fieldset``,
and ``primary`` directives were moved to ``plone.supermodel.model``. The
``omitted``, ``no_omit``, ``mode``, ``widget``, ``order_before``,
``order_after``, ``read_permission``, and ``write_permission`` directives were
moved to ``plone.autoform.directives``.  There are aliases in the old locations
so you don't need to update existing code, but you can switch to the new
locations if you're trying to avoid depending on grok.

Relation support no longer included by default
----------------------------------------------

Dexterity 1.0 included support for object relations based on the zc.relation
catalog and plone.app.relationfield, as well as a behavior
(``plone.app.dexterity.behaviors.related.IRelatedItems``) providing a
generic list of related items based on that implementation.

Since this feature was added to Dexterity, we discovered that it will be hard
to support this type of relation well in Zope 2 until Zope 2 is setting
__parent__ pointers everywhere. In addition, we encountered some problems with
using interfaces as keys in the zc.relation catalog. And Dexterity gained
support for the Archetypes reference engine in
``plone.app.referenceablebehavior``. As a result of these factors, the
zc.relation approach to object relationships will not be included in Dexterity or Plone core for the time being.

VERY IMPORTANT: If you are upgrading a site with Dexterity 1.0 to Dexterity
2.0, it will break unless you install plone.app.relationfield, since your
database contains persistent intid and relations utilities. The easiest way
to include plone.app.relationfield is to install plone.app.dexterity with
the "relations" extra::

  [instance]
  eggs =
      plone.app.dexterity [relations]

Using relations via plone.app.relationfield
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you were relying on the support for relations, you can re-enable support
by installing the ``plone.app.relationfield`` package. You need to add it to
your package's install_requires in setup.py::

  install_requires=[
      'plone.app.relationfield',
      ]

Make sure your package is including its ZCML in configure.zcml::

  <include package="plone.app.relationfield" />

And install its GenericSetup profile as a dependency in your package's metadata.xml::

  <dependencies>
    <dependency>profile-plone.app.relationfield:default</dependency>
  </dependencies>

If you have any content types using the IRelatedItems behavior, you should
update them to import the behavior from the new location::

  <property name="behaviors">
      <element value="plone.app.relationfield.behavior.IRelatedItems" />
  </property>

Content tree and Autocomplete widgets no longer included by default
-------------------------------------------------------------------

In Dexterity 1.0, the widgets in ``plone.formwidget.autocomplete`` and
``plone.formwidget.contenttree`` were installed as dependencies of
``plone.app.dexterity``. In Dexterity 2.0 they are no longer installed
by default, because they are not used by any of the included behaviors
or made available via the through-the-web content type editor at this
time.

If you use these widgets, make sure your package lists them as
dependencies in setup.py, loads their ZCML in configure.zcml, and
activates their GenericSetup profiles as dependencies in metadata.xml.
