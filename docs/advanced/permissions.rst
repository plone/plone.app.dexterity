Permissions 
-------------

**Setting up add permissions, view permissions and field view/edit permissions**

Plone’s security system is based on the concept of 
*permissions* protecting *operations* 
(like accessing a view, 
viewing a field,
modifying a field,
or adding a type of content)
that are granted to *roles*,
which in turn are granted to *users* and/or *groups*.
In the context of developing content types,
permissions are typically used in three different ways:

- A content type or group of related content types often has a custom
  *add permission* which controls who can add this type of content.
- Views (including forms) are sometimes protected by custom
  permissions.
- Individual fields are sometimes protected by permissions,
  so that some users can view and edit fields that others can’t see.

It is easy to create new permissions.
However, be aware that it is considered good practice 
to use the standard permissions wherever possible and 
use *workflow* to control which roles are granted these permissions 
on a per-instance basis.
We’ll cover workflow later in this manual.

Standard permissions
~~~~~~~~~~~~~~~~~~~~~

The standard permissions can be found in ``Product.Five``\’s ``permissions.zcml`` 
(``parts/omelette/Products/Five/permissions.zcml``).
Here, you will find a short ``id`` 
(also known as the *Zope 3 permission id*)
and a longer ``title`` 
(also known as the *Zope 2 permission title*).
For historical reasons, some areas in Plone use the id,
whilst others use the title.
As a rule of thumb:

- Browser views defined in ZCML or protected via a ``grok.require()``
  directive use the Zope 3 permission id.
- Security checks using ``zope.security.checkPermission()`` use the Zope
  3 permission id
- Dexterity’s ``add_permission`` FTI variable uses the Zope 3 permission
  id.
- The ``rolemap.xml`` GenericSetup handler and workflows use the Zope 2
  permission title.
- Security checks using ``AccessControl``’s
  ``getSecurityManager().checkPermission()``, including the methods on
  the ``portal_membership`` tool, use the Zope 2 permission title.

The most commonly used permission are shown below.
The Zope 2 permission title is shown in parentheses.

``zope2.View`` (:guilabel:`View`)
    used to control access to the standard view of a content item;

``zope2.DeleteObjects`` (:guilabel:`Delete objects`)
    used to control the ability to delete child objects in a container;

``cmf.ModifyPortalContent`` (:guilabel:`Modify portal content`)
    used to control write access to content items;

``cmf.ManagePortal`` (:guilabel:`Manage portal`)
    used to control access to management screens;

``cmf.AddPortalContent`` (:guilabel:`Add portal content`)
    the standard add permission required to add content to a folder;

``cmf.SetOwnProperties`` (:guilabel:`Set own properties`) 
    used to allow users to set their own member properties'

``cmf.RequestReview`` (:guilabel:`Request Review`)
    typically used as a workflow transition guard 
    to allow users to submit content for review;

``cmf.ReviewPortalContent`` (:guilabel:`Review portal content`)
    usually granted to the ``Reviewer`` role,
    controlling the ability to publish or reject content.

Standard roles
~~~~~~~~~~~~~~~

As with permissions, it is easy to create custom roles (use the
``rolemap.xml`` GenericSetup import step – see ``CMFPlone``\’s version of
this file for an example), although you should use the standard roles
where possible.

The standard roles in Plone are:

:guilabel:`Anonymous`
    a pseudo-role that represents non-logged in users.

.. note::

    if a permission is granted to :guilabel:`Anonymous`,
    it is effectively granted to everyone.
    It is not possible to grant permissions to non-logged in users
    without also granting them to logged in ones.

:guilabel:`Authenticated`
     a pseudo-role that represents logged-in users.

:guilabel:`Owner`
     automatically granted to the creator of an object.

:guilabel:`Manager`
     which represents super-users/administrators.
     Almost all permissions that are not granted to ``Anonymous`` 
     are granted to ``Manager``.

:guilabel:`Reviewer`
     which represents content reviewers separately from site administrators.
     It is possible to grant the :guilabel:`Reviewer` role locally on the
     :guilabel:`Sharing`` tab, where it is shown as :guilabel:`Can review`.

:guilabel:`Member`
     representing “standard” Plone users.

In addition, there are three roles that are intended to be used as
*local roles* only. These are granted to specific users or groups via
the :guilabel:`Sharing` tab, where they appear under more user friendly
pseudonyms.

:guilabel:`Reader`, aka :guilabel:`Can view`,
    confers the right to view content.
    As a role of thumb,
    the :guilabel:`Reader` role should have the 
    :guilabel:`View` and :guilabel:`Access contents information` permissions 
    if the :guilabel:`Owner` roles does.

:guilabel:`Editor`, aka :guilabel:`Can edit`,
    confers the right to edit content.
    As a role of thumb, the :guilabel:`Editor` role should have the 
    :guilabel:`Modify portal content` permission 
    if the :guilabel:`Owner` roles does.

:guilabel:`Contributor`, aka :guilabel:`Can add`,
    confers the right to add new content.
    As a role of thumb,
    the:guilabel: `Contributor` role should have the 
    `Add:guilabel: portal content` permission 
    and any type-specific add permissions globally 
    (i.e. granted in ``rolemap.xml``),
    although these permissions are sometimes managed in workflow as well.

Performing permission checks in code
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is sometimes necessary to check permissions explicitly in code, for
example in a view. A permission check always checks a permission on a
context object, since permissions can change with workflow.

.. note::
    Never make security dependent on users’ roles directly. Always check for
    a permission, and assign the permission to the appropriate role or
    roles.

As an example,
let’s display a message on the view of a ``Session`` type
if the user has the ``cmf.RequestReview`` permission.
In ``session.py``, we update the ``View`` class with the following::

    from zope.security import checkPermission

    class View(dexterity.DisplayForm):
        grok.context(ISession)
        grok.require('zope2.View')
        
        def canRequestReview(self):
            return checkPermission('cmf.RequestReview', self.context)

And in the ``session_templates/view.pt`` template, we add:

.. code-block:: html

    <div class="discreet"
         tal:condition="view/canRequestReview"
         i18n:translate="suggest_review">
        Please submit this for review.
    </div>

Creating custom permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Although the standard permissions should be used to control basic operations
(view, modify, delete, review),
it is sometimes useful to create new permissions.
Combined with custom workflows,
custom permissions can be used 
to create highly tailored content review cycles
and data entry applications.
They are also an important way to control who can add what content.

The easiest way to create a custom permission is with the help of the
`collective.autopermission`_ package,
which allows permissions to be defined 
using the ``<permission />`` ZCML statement.

.. note::
    `collective.autopermission`_ is obsolete in Zope 2.12, where its
    functionality has been merged into Zope itself.

As an example,
let’s create some custom permissions 
for use with the ``Session`` type.
We’ll create a new add permission,
so that we can let any member submit a session to a program,
and a permission which we will later use 
to let reviewers edit some specific fields on the ``Session`` type.

First, we need to depend on `collective.autopermission`_. In ``setup.py``::

    install_requires=[
        ...
        'collective.autopermission',
    ],

.. note::
    Make sure `collective.autopermission`_\’s configuration is included 
    before any custom permissions are defined.
    In our case, 
    the ``<includeDependencies />`` line takes care of this.

Next, we’ll create a file called ``permissions.zcml`` to hold the
permissions (we could also place them directly into ``configure.zcml``).
We need to include this in ``configure.zcml``, just after the
``<includeDependencies />`` line:

.. code-block:: xml

    <include file="permissions.zcml" />

.. note::
    All permissions need to be defined before the 
    ``<grok:grok package=“.” />`` line in ``configure.zcml``.
    Otherwise, you may get errors trying to use the permission 
    with a ``grok.require()`` directive.

The ``permissions.zcml`` file looks like this:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        i18n_domain="example.conference">

        <permission
            id="example.conference.AddSession"
            title="example.conference: Add session"
            />

        <permission
            id="example.conference.ModifyTrack"
            title="example.conference: Modify track"
            />
            
    </configure>

New permissions are granted to the :guilabel:`Manager` role only by default.
To set a different default,
we can use the ``rolemap.xml`` GenericSetup import step,
which maps permissions to roles at the site root.

In ``profiles/default/rolemap.xml``, we have the following:

.. code-block:: xml

    <?xml version="1.0"?>
    <rolemap>
      <permissions>
        <permission name="example.conference: Add session" acquire="True">
          <role name="Owner"/>
          <role name="Manager"/>
          <role name="Member"/>
          <role name="Contributor"/>
        </permission>
        <permission name="example.conference: Modify track" acquire="True">
          <role name="Manager"/>
          <role name="Reviewer"/>
        </permission>
      </permissions>
    </rolemap>

.. note::
    This file uses the Zope 2 permission title instead of the shorter Zope 3
    permission id.

Content type add permissions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dexterity content types’ add permissions are set in the FTI,
using the ``add_permission`` property.
This can be changed through the web 
or in the GenericSetup import step for the content type.

To make the ``Session`` type use our new permission, we modify the
``add_permission`` line in
``profiles/default/example.conference.session.xml``:

.. code-block:: xml

     <property name="add_permission">example.conference.AddSession</property>

Protecting views and forms
~~~~~~~~~~~~~~~~~~~~~~~~~~

Access to views and other browser resources (like viewlets or portlets)
can be protected by permissions, either using the ``permission`` attribute
on ZCML statements like ``<browser:page />`` or using the ``grok.require()``
directive.

We have already seen this directive on our views::

    class View(grok.View):
        grok.context(IPresenter)
        grok.require('zope2.View')

We could use a custom permission name as the argument to
``grok.require()``. We could also use the special ``zope.Public`` permission
name to make the view accessible to anyone.

Protecting form fields
~~~~~~~~~~~~~~~~~~~~~~~

Individual fields in a schema may be associated with a *read* permission
and a *write* permission.
The read permission is used to control access to the field’s value 
via protected code (e.g. scripts or templates created through the web)
and URL traversal,
and can be used to control the appearance of fields 
when using display forms 
(if you use custom views that access the attribute directly,
you’ll need to perform your own checks).
Write permissions can be used to control 
whether or not a given field appears on a type’s add and edit forms.

In both cases,
read and write permissions are annotated onto the schema using directives
similar to those we’ve already seen for form widget hints.
The ``read_permission()`` and ``write_permission()`` directives are
found in the `plone.directives.dexterity`_ package.

As an example, let’s add a field for *Session* reviewers to record the
track for a session. We’ll store the vocabulary of available tracks on
the parent ``Program`` object in a text field, so that the creator of the
``Program`` can choose the available tracks.

First, we add this to the ``IProgram`` schema in ``program.py``::

    form.widget(tracks=TextLinesFieldWidget)
    tracks = schema.List(
            title=_(u"Tracks"),
            required=True,
            default=[],
            value_type=schema.TextLine(),
        )

The ``TextLinesFieldWidget`` is used to edit a list of text lines in a
text area. It is imported as::

    from plone.z3cform.textlines.textlines import TextLinesFieldWidget

Next, we’ll add a vocabulary for this to ``session.py``::

    from Acquisition import aq_inner, aq_parent
    from zope.schema.interfaces import IContextSourceBinder
    from zope.schema.vocabulary import SimpleVocabulary
    ...

    @grok.provider(IContextSourceBinder)
    def possibleTracks(context):
        
        # we put the import here to avoid a circular import
        from example.conference.program import IProgram
        while context is not None and not IProgram.providedBy(context):
            context = aq_parent(aq_inner(context))
        
        values = []
        if context is not None and context.tracks:
            values = context.tracks
        
        return SimpleVocabulary.fromValues(values)

This vocabulary finds the closest ``IProgram`` 
(in the add form, the ``context`` will be the ``Program``,
but on the edit form, it will be the ``Session``,
so we need to check the parent)
and uses its ``tracks`` variable as the vocabulary.

Next, we add a field to the ``ISession`` interface in the same file and
protect it with the relevant write permission::

    dexterity.write_permission(track='example.conference.ModifyTrack')
    track = schema.Choice(
            title=_(u"Track"),
            source=possibleTracks,
            required=False,
        )

The ``dexterity`` module is the root of the `plone.directives.dexterity`_
package, imported as::

    from plone.directives import dexterity

With this in place, users with the ``example.conference: Modify track``
permission should be able to edit tracks for a session. For everyone
else, the field will be hidden in the edit form.

.. _plone.directives.dexterity: http://pypi.python.org/pypi/plone.directives.dexterity
.. _collective.autopermission: http://pypi.python.org/pypi/collective.autopermission
.. _plone.directives.form: http://pypi.python.org/pypi/plone.directives.form

