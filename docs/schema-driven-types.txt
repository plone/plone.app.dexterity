Schema-driven types
=====================

**Creating a minimal type based on a schema**

The schema
------------

**Writing a schema for the type**

A simple Dexterity type consists of a schema and an FTI (Factory Type
Information, the object configured in :guilabel:`portal_types` in the ZMI).
We’ll create the schemata here, and the FTI on the next page.

Each schema is typically in a separate module. Thus, we will add three
files to our product: ``presenter.py``, ``program.py``, and ``session.py``.
Each will start off with a schema interface.

First, we will define a message factory to aid future
internationalisation of the package. Every string that is presented to
the user should be wrapped in ``_()`` as shown with the titles and
descriptions below.

The message factory lives in the package root ``__init__.py`` file:

.. code-block:: python

    from zope.i18nmessageid import MessageFactory

    _ = MessageFactory("example.conference")

Notice how we use the package name as the translation domain.

We can now define the schemata for our three types.

For the Presenter type, ``presenter.py`` looks like this:

.. code-block:: python

    from five import grok
    from zope import schema

    from plone.directives import form, dexterity

    from plone.app.textfield import RichText
    from plone.namedfile.field import NamedImage

    from example.conference import _

    class IPresenter(form.Schema):
        """A conference presenter. Presenters can be added anywhere.
        """
        
        title = schema.TextLine(
                title=_(u"Name"),
            )
        
        description = schema.Text(
                title=_(u"A short summary"),
            )
        
        bio = RichText(
                title=_(u"Bio"),
                required=False
            )
        
        picture = NamedImage(
                title=_(u"Picture"),
                description=_(u"Please upload an image"),
                required=False,
            )

Notice how we use the field names title and description for the name and
summary. We do this to provide values for the default title and
description metadata used in Plone’s folder listings and searches, which
defaults to these fields. In general, every type should have a title
field, although it could be provided by behaviors (more on those later).

For the *Program* type, ``program.py`` looks like this:

.. code-block:: python

    from five import grok
    from zope import schema

    from plone.directives import form, dexterity
    from plone.app.textfield import RichText

    from example.conference import _

    class IProgram(form.Schema):
        """A conference program. Programs can contain Sessions.
        """
        
        title = schema.TextLine(
                title=_(u"Program name"),
            )
        
        description = schema.Text(
                title=_(u"Program summary"),
            )
        
        start = schema.Datetime(
                title=_(u"Start date"),
                required=False,
            )

        end = schema.Datetime(
                title=_(u"End date"),
                required=False,
            )
        
        details = RichText(
                title=_(u"Details"),
                description=_(u"Details about the program"),
                required=False,
            )

Finally, ``session.py`` for the Session type looks like this:

.. code-block:: python

    from five import grok
    from zope import schema

    from plone.directives import form, dexterity
    from plone.app.textfield import RichText

    class ISession(form.Schema):
        """A conference session. Sessions are managed inside Programs.
        """
        
        title = schema.TextLine(
                title=_(u"Title"),
                description=_(u"Session title"),
            )
        
        description = schema.Text(
                title=_(u"Session summary"),
            )
        
        details = RichText(
                title=_(u"Session details"),
                required=False
            )


Note that we haven’t added information about speakers or tracks yet.
We’ll do that when we cover vocabularies and references later.

Schema interfaces vs. other interfaces
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As you may have noticed, each schema is basically just an interface
(``zope.interface.Interface``) with fields.
The standard fields are found in the `zope.schema`_ package.
You should look at its interfaces
(``parts/omelette/zope/schema/interfaces.py``) to learn about the various
schema fields available, and review the `online documentation`_ for the
package. You may also want to look up `plone.namedfile`_, which you can
use if you require a file field, `z3c.relationfield`_, which can be used
for references, and `plone.app.textfield`_, which supports rich text
with a WYSIWYG editor. We will cover these field types later in this
manual. They can also be found in the reference at the end.

Unlike a standard interface, however, we are deriving from ``form.Schema``
(actually, ``plone.directives.form.Schema``). This is just a marker
interface that allows us to add some form hints to the interface, which
are then used by Dexterity (actually, the `plone.autoform`_ package) to
construct forms. Take a look at the `plone.directives.form`_
documentation to learn more about the various hints that are possible.
The most common ones are ``form.fieldset()``, to define groups of fields,
``form.widget()``, to set a widget for a particular field, and
``form.omit()`` to hide one or more fields from the form. 
We will see examples of these later in the manual.

.. _zope.schema: 
.. _online documentation: http://pypi.python.org/pypi/zope.schema
.. _plone.app.textfield: http://pypi.python.org/pypi/plone.app.textfield
.. _plone.autoform: http://pypi.python.org/pypi/plone.autoform
.. _plone.directives.form: http://pypi.python.org/pypi/plone.directives.form
.. _plone.namedfile: http://pypi.python.org/pypi/plone.namedfile
.. _z3c.relationfield: http://pypi.python.org/pypi/z3c.relationfield

The FTI
--------

**Adding a Factory Type Information object for the type**

With the schema in place, we just need to make our types installable. We
do this with GenericSetup.

First, we add a ``types.xml`` file to ``profiles/default``:

.. code-block:: xml

    <object name="portal_types">
     <object name="example.conference.presenter" meta_type="Dexterity FTI" />
     <object name="example.conference.program" meta_type="Dexterity FTI" />
     <object name="example.conference.session" meta_type="Dexterity FTI" />
    </object>

We use the package name as a prefix and the type name in lowercase to
create a unique name. It is important that the ``meta_type`` is
*Dexterity FTI*.

We then need to add an XML file for each of the types, where the file
name matches the type name. First, we add a directory
``profiles/default/types``, and then add the following:

For the *Presenter* type, we have ``example.conference.presenter.xml``:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="example.conference.presenter" meta_type="Dexterity FTI"
       i18n:domain="example.conference" xmlns:i18n="http://xml.zope.org/namespaces/i18n">
     
     <!-- Basic metadata -->
     <property name="title" i18n:translate="">Presenter</property>
     <property name="description" i18n:translate="">A person presenting sessions</property>
     <property name="content_icon">user.gif</property>
     <property name="allow_discussion">True</property>
     <property name="global_allow">True</property>
     <property name="filter_content_types">True</property>
     <property name="allowed_content_types" />
     
     <!-- schema interface -->
     <property name="schema">example.conference.presenter.IPresenter</property> 
     
     <!-- class used for content items -->
     <property name="klass">plone.dexterity.content.Item</property>
     
     <!-- add permission -->
     <property name="add_permission">cmf.AddPortalContent</property>
     
     <!-- enabled behaviors -->
     <property name="behaviors">
         <element value="plone.app.content.interfaces.INameFromTitle" />
     </property>
     
     <!-- View information -->
     <property name="default_view">view</property>
     <property name="default_view_fallback">False</property>
     <property name="view_methods">
      <element value="view"/>
     </property>
     
     <!-- Method aliases -->
     <alias from="(Default)" to="(dynamic view)"/>
     <alias from="edit" to="@@edit"/>
     <alias from="sharing" to="@@sharing"/>
     <alias from="view" to="(selected layout)"/>
     
     <!-- Actions -->
     <action title="View" action_id="view" category="object" condition_expr=""
        url_expr="string:${object_url}" visible="True">
      <permission value="View"/>
     </action>
     <action title="Edit" action_id="edit" category="object" condition_expr=""
        url_expr="string:${object_url}/edit" visible="True">
      <permission value="Modify portal content"/>
     </action>
    </object>

There is a fair amount of boilerplate here which could actually be
omitted, because the Dexterity FTI defaults will take care of most of
this. However, it is useful to see the options available so that you
know what you can change.

The important lines here are:

-  The ``name`` attribute on the root element must match the name in
   ``types.xml`` and the filename.
-  We use the package name as the translation domain again, via
   ``i18n:domain``.
-  We set a title and description for the type
-  We also specify an icon. Here, we use a standard icon from Plone’s
   ``plone_images`` skin layer. You’ll learn more about static resources
   later.
-  We set ``global_allow`` to ``True``. This means that the type will be
   addable in standard folders.
-  The schema interface is referenced by the ``schema`` property.
-  We set the ``klass`` property to the standard
   ``plone.dexterity.content.Item``. There is also
   ``plone.dexterity.content.Container``.
-  We specify the name of an add permission. The default
   ``cmf.AddPortalContent`` should be used unless you configure a custom
   permission. Custom permissions are convered later in this manual.
-  We add a *behavior*. Behaviors are re-usable aspects providing
   semantics and/or schema fields. Here, we add the ``INameFromTitle``
   behavior, which will give our content object a readable id based on
   the ``title`` property. We’ll cover other behaviors later.

The ``Session`` type, in ``example.conference.session.xml``, is very
similar:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="example.conference.session" meta_type="Dexterity FTI"
       i18n:domain="example.conference" xmlns:i18n="http://xml.zope.org/namespaces/i18n">
     
     <!-- Basic metadata -->
     <property name="title" i18n:translate="">Session</property>
     <property name="description" i18n:translate="">A session on the program</property>
     <property name="content_icon">document_icon.gif</property>
     <property name="allow_discussion">True</property>
     <property name="global_allow">False</property>
     <property name="filter_content_types">True</property>
     <property name="allowed_content_types" />
     
     <!-- schema interface -->
     <property name="schema">example.conference.session.ISession</property> 
     
     <!-- class used for content items -->
     <property name="klass">plone.dexterity.content.Item</property>
     
     <!-- add permission -->
     <property name="add_permission">cmf.AddPortalContent</property>
     
     <!-- enabled behaviors -->
     <property name="behaviors">
         <element value="plone.app.content.interfaces.INameFromTitle" />
     </property>
     
     <!-- View information -->
     <property name="default_view">view</property>
     <property name="default_view_fallback">False</property>
     <property name="view_methods">
      <element value="view"/>
     </property>
     
     <!-- Method aliases -->
     <alias from="(Default)" to="(dynamic view)"/>
     <alias from="edit" to="@@edit"/>
     <alias from="sharing" to="@@sharing"/>
     <alias from="view" to="(selected layout)"/>
     
     <!-- Actions -->
     <action title="View" action_id="view" category="object" condition_expr=""
        url_expr="string:${object_url}" visible="True">
      <permission value="View"/>
     </action>
     <action title="Edit" action_id="edit" category="object" condition_expr=""
        url_expr="string:${object_url}/edit" visible="True">
      <permission value="Modify portal content"/>
     </action>
    </object>

Again, this is an Item. Here, we have set ``global_allow`` to ``False``,
since these objects should only be addable inside a *Program*.

The ``Program``, in ``example.conference.program.xml``, looks like this:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="example.conference.program" meta_type="Dexterity FTI"
       i18n:domain="example.conference" xmlns:i18n="http://xml.zope.org/namespaces/i18n">
     
     <!-- Basic metadata -->
     <property name="title" i18n:translate="">Program</property>
     <property name="description" i18n:translate="">A conference program</property>
     <property name="content_icon">folder_icon.gif</property>
     <property name="allow_discussion">True</property>
     <property name="global_allow">True</property>
     <property name="filter_content_types">True</property>
     <property name="allowed_content_types">
         <element value="example.conference.session" />
     </property>
     
     <!-- schema interface -->
     <property name="schema">example.conference.program.IProgram</property> 
     
     <!-- class used for content items -->
     <property name="klass">plone.dexterity.content.Container</property>
     
     <!-- add permission -->
     <property name="add_permission">cmf.AddPortalContent</property>
     
     <!-- enabled behaviors -->
     <property name="behaviors">
         <element value="plone.app.content.interfaces.INameFromTitle" />
     </property>
     
     <!-- View information -->
     <property name="default_view">view</property>
     <property name="default_view_fallback">False</property>
     <property name="view_methods">
      <element value="view"/>
     </property>
     
     <!-- Method aliases -->
     <alias from="(Default)" to="(dynamic view)"/>
     <alias from="edit" to="@@edit"/>
     <alias from="sharing" to="@@sharing"/>
     <alias from="view" to="(selected layout)"/>
     
     <!-- Actions -->
     <action title="View" action_id="view" category="object" condition_expr=""
        url_expr="string:${object_url}" visible="True">
      <permission value="View"/>
     </action>
     <action title="Edit" action_id="edit" category="object" condition_expr=""
        url_expr="string:${object_url}/edit" visible="True">
      <permission value="Modify portal content"/>
     </action>
    </object>

The difference here is that we use the ``Container`` class, and we filter
the containable types (``filter_content_types`` and
``allowed_content_types``) to allow only ``Sessions`` to be added inside
this folder.

Testing the type 
------------------

**How to start up Plone and test the type, and some trouble-shooting tips.**

With a schema and FTI for each type, and our GenericSetup profile
registered in ``configure.zcml``, we should be able to test our type. Make
sure that you have run a buildout, and then start ``./bin/instance fg`` as
normal. Add a Plone site, and go to the :guilabel:`portal_quickinstaller` in the
ZMI. You should see your package there and be able to install it.

Once installed, you should be able to add objects of the new content
types.

If Zope doesn’t start up:

-  Look for error messages on the console, and make sure you start in
   the foreground with ``./bin/instance fg``. You could have a syntax
   error or a ZCML error.

If you don’t see your package in :guilabel:`portal_quickinstaller`:

-  Ensure that the package is either checked out by ``mr.developer`` or
   that you have a ``develop`` line in ``buildout.cfg`` to load it as a
   develop egg. ``develop = src/*`` should suffice, but you can also add
   the package explicitly, e.g. with 
   ``develop = src/example.conference.``
-  Ensure that the package is actually loaded as an egg. It should be
   referenced in the ``eggs`` section under ``[instance]`` .
-  You can check that the package is correctly configured in the
   buildout by looking at the generated ``bin/instance`` script
   (``bin\instance-script.py`` on Windows). There should be a line for
   your package in the list of eggs at the top of the file.
-  Make sure that the package’s ZCML is loaded. You can do this by
   installing a ZCML slug (via the ``zcml`` option in the ``[instance]``
   section of ``buildout.cfg``) or by adding an ``<include />`` line in
   another package’s ``configure.zcml``. However, the easiest way with
   Plone 3.3 and later is to add the ``z3c.autoinclude.plugin`` entry
   point to ``setup.py``.
-  Ensure that you have added a ``<genericsetup:registerProfile />``
   stanza to ``configure.zcml``.

If the package fails to install in ``portal_quickinstaller``:

-  Look for errors in the :guilabel:`error_log` at the root of the Plone site, in
   your console, or in your log files.
-  Check the syntax and placement of the profile files. Remember that
   you need a ``types.xml`` listing your types, and corresponding files in
   ``types/*.xml``.

If your forms do not look right (e.g. you are missing custom widgets):

- Make sure your schema derives from ``form.Schema``.
- Remember that the directives require you to specify the correct field
  name, even if they are placed before or after the relevant field.
- Check that you have a ``<grok:grok package="." />`` line in
  ``configure.zcml``.

