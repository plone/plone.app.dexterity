Schema-driven types
=====================

**Creating a minimal type based on a schema**

The schema
------------

A simple Dexterity type consists of a schema and an FTI (Factory Type
Information, the object configured in :guilabel:`portal_types` in the ZMI).
We’ll create the schemata here, and the FTI on the next page.

Each schema is typically in a separate module. Thus, we will add three
files to our product: ``presenter.py``, ``program.py``, and ``session.py``.
Each will start off with a schema interface.

Creating base files
~~~~~~~~~~~~~~~~~~~

Since we created our example.conference command via ZopeSkel, we'll be able to use its ``addcontent`` command to add base files for our content types. ``addcontent`` must be used from inside your new package.

.. note::

    If you didn't use ZopeSkel, you'll need to add the files yourself. We'll supply the full source here, and you may refer to the example repository.

Typical `addcontent` use starting out at the buildout directory is:

.. code-block:: bash

    $ cd src/example.conference/
    $ ../../bin/paster addcontent -l
    Available templates:
        dexterity_behavior:  A behavior skeleton
        dexterity_content:   A content type skeleton

The "-l" lists available content templates.

.. note::

    At this point, you may receive an error message beginning with
    ``pkg_resources.DistributionNotFound``. Do *not* follow the error messages
    advice to run `python setup.py`. Instead, check to make sure that you have
    added your package to the eggs and develop sections of your buildout and
    have run buildout. This loads package dependencies that are required to run
    addcontent.

Now, let's add two of the three content types, for the conference sessions and programs.
We'll do presenters in the next section as a model-driven type.

.. code-block:: bash

    $ ../../bin/paster addcontent dexterity_content
    Enter contenttype_name (Content type name ) ['Example Type']: Session
    Enter contenttype_description (Content type description ) ['Description of the Example Type']: A session in a conference
    Enter folderish (True/False: Content type should act as a container ) [False]: False
    Enter global_allow (True/False: Globally addable ) [True]: False
    Enter allow_discussion (True/False: Allow discussion ) [False]:

    $ ../../bin/paster addcontent dexterity_content
    Enter contenttype_name (Content type name ) ['Example Type']: Program
    Enter contenttype_description (Content type description ) ['Description of the Example Type']: A conference program
    Enter folderish (True/False: Content type should act as a container ) [False]: True
    Enter global_allow (True/False: Globally addable ) [True]:
    Enter allow_discussion (True/False: Allow discussion ) [False]:

Notice that we chose to make the `Conference` type a container, because we will
want it to be able to contain sessions. Likewise, we set `Globally addable`` for
the `Session` type to False, as we'll only want to allow them to be added inside
programs.

If you check ``example.conference/example/conference``, you'll discover that
Python source files program.py, session.py and presenter.py have been added. If
you explore ``example.conference/example/conference/profiles/default/types``,
you'll also find XML files setting the Factory Type Information for each new
type. We'll customize all of these.

Setting the schema
~~~~~~~~~~~~~~~~~~

Start with program.py. Notice the boilerplate:

.. code-block:: python

    # If you want a schema-defined interface, delete the model.load
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/program.xml to define the content type
    # and add directives here as necessary.

    model.load("models/program.xml")

Since we're going to be defining our fields via Zope schema rather than an XML model, delete all of that.

Next, add schema declarations for our fields. The top part of the file should look like:

.. code-block:: python

    from example.conference import MessageFactory as _
    from plone.app.textfield import RichText
    from plone.supermodel import model
    from zope import schema


    class IProgram(model.Schema):

        """A conference program. Programs can contain Sessions."""

        title = schema.TextLine(
            title=_(u'Program name'),
        )

        description = schema.Text(
            title=_(u'Program summary'),
        )

        start = schema.Datetime(
            title=_(u'Start date'),
            required=False,
        )

        end = schema.Datetime(
            title=_(u'End date'),
            required=False,
        )

        details = RichText(
                title=_(u'Details'),
                description=_(u'Details about the program.'),
                required=False,
            )


We've also removed unnecessary ``import`` declarations.

If you haven't developed for Plone before, take special note of the ``from example.conference import MessageFactory as _`` code. This is to aid future
internationalisation of the package. Every string that is presented to
the user should be wrapped in ``_()`` as shown with the titles and
descriptions below.

The message factory lives in the package root ``__init__.py`` file:

.. code-block:: python

    from zope.i18nmessageid import MessageFactory

    MessageFactory = MessageFactory("example.conference")

Notice how we use the package name as the translation domain.

Notice how we use the field names title and description for the name and
summary. We do this to provide values for the default title and
description metadata used in Plone’s folder listings and searches, which
defaults to these fields. In general, every type should have a title
field, although it could be provided by behaviors (more on those later).

Save program.py.

``session.py`` for the Session type should look like this:

.. code-block:: python

    from example.conference import MessageFactory as _
    from plone.app.textfield import RichText
    from plone.supermodel import model
    from zope import schema


    class ISession(model.Schema):

        """A conference session. Sessions are managed inside Programs."""

        title = schema.TextLine(
            title=_(u'Title'),
            description=_(u'Session title'),
        )

        description = schema.Text(
            title=_(u'Session summary'),
        )

        details = RichText(
            title=_(u'Session details'),
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
use if you require a file field, `plone.app.relationfield`_, which can be used
for references, and `plone.app.textfield`_, which supports rich text
with a WYSIWYG editor. We will cover these field types later in this
manual. They can also be found in the reference at the end.

Unlike a standard interface, however, we are deriving from ``model.Schema``
(actually, ``plone.supermodel.model.Schema``). This is just a marker
interface that allows us to add some form hints to the interface, which
are then used by Dexterity (actually, the `plone.autoform`_ package) to
construct forms. Take a look at the `plone.autoform`_
documentation to learn more about the various hints that are possible.
The most common ones are from ``plone.autoform.directives``.
Use ``fieldset()`` to define groups of fields,
``widget()`` to set widgets for particular fields and
``omitted()`` to hide one or more fields from the form.
We will see examples of these later in the manual.

.. _zope.schema:
.. _online documentation: http://pypi.python.org/pypi/zope.schema
.. _plone.app.relationfield: http://pypi.python.org/pypi/plone.app.relationfield
.. _plone.app.textfield: http://pypi.python.org/pypi/plone.app.textfield
.. _plone.autoform: http://pypi.python.org/pypi/plone.autoform
.. _plone.namedfile: http://pypi.python.org/pypi/plone.namedfile

The FTI
--------

**Adding a Factory Type Information object for the type**

With the schema in place, we just need to make our types installable. We
do this with GenericSetup. Most of this was set up when we used ``addcontent`` to add the content type boilerplate.

Look in the ``types.xml`` file in your packages ``example/conference/profiles/default`` directory:

.. code-block:: xml

    <object name="portal_types">
      <object name="example.conference.program" meta_type="Dexterity FTI" />
      <object name="example.conference.session" meta_type="Dexterity FTI" />
    </object>

We use the package name as a prefix and the type name in lowercase to
create a unique name. It is important that the ``meta_type`` is
*Dexterity FTI*.

We then need to add/edit an XML file for each of the types, where the file
name matches the type name.

The ``Session`` type, in ``example.conference.session.xml``, should look like this:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="example.conference.session" meta_type="Dexterity FTI"
        xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        i18n:domain="example.conference">

      <!-- Basic metadata -->
      <property name="title" i18n:translate="">Session</property>
      <property name="description" i18n:translate="">A session in a program</property>
      <property name="icon_expr">string:${portal_url}/document_icon.png</property>
      <property name="factory">example.conference.session</property>
      <property name="global_allow">False</property>
      <property name="filter_content_types">True</property>
      <property name="allowed_content_types" />
      <property name="allow_discussion">False</property>

      <!-- schema and class used for content items -->
      <property name="schema">example.conference.session.ISession</property>
      <property name="klass">example.conference.session.Session</property>

      <property name="behaviors">
        <element value="plone.app.content.interfaces.INameFromTitle" />
       </property>

      <!-- View information -->
      <property name="link_target"></property>
      <property name="immediate_view">view</property>
      <property name="default_view">view</property>
      <property name="view_methods">
        <element value="view"/>
      </property>
      <property name="default_view_fallback">False</property>
      <property name="add_permission">cmf.AddPortalContent</property>

      <!-- Method aliases -->
      <alias from="(Default)" to="(dynamic view)" />
      <alias from="view" to="(selected layout)" />
      <alias from="edit" to="@@edit" />
      <alias from="sharing" to="@@sharing" />

      <!-- Actions -->
      <action title="View" action_id="view" category="object" condition_expr=""
          url_expr="string:${object_url}/" visible="True">
        <permission value="View" />
      </action>
      <action title="Edit" action_id="edit" category="object" condition_expr=""
          url_expr="string:${object_url}/edit" visible="True">
        <permission value="Modify portal content" />
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
-  We have set ``global_allow`` to ``False``,
   since these objects should only be addable inside a *Program*..
-  The schema interface is referenced by the ``schema`` property.
-  We set the ``klass`` property to the class defined in the boilerplate file.
   If you were creating this yourself, you could have instead just used
   ``plone.dexterity.content.Item`` or
   ``plone.dexterity.content.Container``.
-  We specify the name of an add permission. The default
   ``cmf.AddPortalContent`` should be used unless you configure a custom
   permission. Custom permissions are convered later in this manual.
-  We add a *behavior*. Behaviors are re-usable aspects providing
   semantics and/or schema fields. Here, we add the ``INameFromTitle``
   behavior, which will give our content object a readable id based on
   the ``title`` property. We’ll cover other behaviors later.
   We removed the IBasic behavior (which would supply title and description fields)
   as we have alternative fields.


The ``Program``, in ``example.conference.program.xml``, looks like this:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="example.conference.program" meta_type="Dexterity FTI"
        xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        i18n:domain="example.conference">

      <!-- Basic metadata -->
      <property name="title" i18n:translate="">Program</property>
      <property name="description" i18n:translate="">Conference Program</property>
      <property name="icon_expr">string:${portal_url}/folder_icon.png</property>
      <property name="factory">example.conference.program</property>
      <property name="global_allow">True</property>
      <property name="filter_content_types">True</property>
      <property name="allowed_content_types">
        <element value="example.conference.session" />
      </property>
      <property name="allow_discussion">False</property>

      <!-- schema and class used for content items -->
      <property name="schema">example.conference.program.IProgram</property>
      <property name="klass">example.conference.program.Program</property>

      <property name="behaviors">
        <element value="plone.app.content.interfaces.INameFromTitle" />
       </property>

      <!-- View information -->
      <property name="link_target"></property>
      <property name="immediate_view">view</property>
      <property name="default_view">view</property>
      <property name="view_methods">
        <element value="view"/>
      </property>
      <property name="default_view_fallback">False</property>
      <property name="add_permission">cmf.AddPortalContent</property>


      <!-- Method aliases -->
      <alias from="(Default)" to="(dynamic view)" />
      <alias from="view" to="(selected layout)" />
      <alias from="edit" to="@@edit" />
      <alias from="sharing" to="@@sharing" />

      <!-- Actions -->
      <action title="View" action_id="view" category="object" condition_expr=""
          url_expr="string:${object_url}/" visible="True">
        <permission value="View" />
      </action>
      <action title="Edit" action_id="edit" category="object" condition_expr=""
          url_expr="string:${object_url}/edit" visible="True">
        <permission value="Modify portal content" />
      </action>
    </object>

We've edited this one a little from the boilplate: the difference here is that
we filter the containable types (``filter_content_types`` and
``allowed_content_types``) to allow only ``Sessions`` to be added inside this
folder.

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

- Make sure your schema derives from ``model.Schema``.
- Remember that the directives require you to specify the correct field
  name, even if they are placed before or after the relevant field.
