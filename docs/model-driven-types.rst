Model-driven types
==================

In the previous section, we defined two types by using Zope schema. In this
section, we're going to define a type's fields using an XML model file.

The great advantage of using a model file is that we can prototype the content
type in Dexterity's through-the-web field editor, then export the XML model file
for incorporation into our package.

XML may be used to do pretty much anything you could do via Zope schema. Many
users not already schooled in Zope schema will find this by far the easiest and
fastest way to create Dexterity content types.

Adding the type
---------------

As in the previous section, we'll use ``addcontent`` to add our content type to
the project. This type will be for conference presenters.

.. code-block:: bash

    $ ../../bin/paster addcontent dexterity_content
    Enter contenttype_name (Content type name ) ['Example Type']: Presenter
    Enter contenttype_description (Content type description ) ['Description of the Example Type']: A person presenting a conference session
    Enter folderish (True/False: Content type should act as a container ) [False]: False
    Enter global_allow (True/False: Globally addable ) [True]:
    Enter allow_discussion (True/False: Allow discussion ) [False]:

Setting the field model
-----------------------

Look in ``example.conference/example/conference/models/presenter.xml`` for a bare model file created by addcontent. Let's elaborate it:

.. code-block:: xml

    <model xmlns:form="http://namespaces.plone.org/supermodel/form"
           xmlns:security="http://namespaces.plone.org/supermodel/security"
           xmlns:marshal="http://namespaces.plone.org/supermodel/marshal"
           xmlns="http://namespaces.plone.org/supermodel/schema">
      <schema>
        <field name="name" type="zope.schema.TextLine">
          <description/>
          <title>Name</title>
        </field>
        <field name="description" type="zope.schema.Text">
          <description/>
          <title>A short summary</title>
        </field>
        <field name="bio" type="plone.app.textfield.RichText">
          <description/>
          <required>False</required>
          <title>Bio</title>
        </field>
        <field name="photo" type="plone.namedfile.field.NamedBlobImage">
          <description>Please upload an image.</description>
          <required>False</required>
          <title>Photo</title>
        </field>I
      </schema>
    </model>

The XML name spaces we use are described in the `Dexterity XML` reference
section.

That's all we need! To see why, look in the generated file ``presenter.py``:

.. code-block:: python

    from example.conference import MessageFactory as _
    from plone.supermodel import model
    from zope import schema


    class IPresenter(model.Schema):

        """Schema for Conference Presenter content type."""

        model.load('models/presenter.xml')


Note the ``model.load`` directive. We'd deleted that when we created schema-driven field sets. Now, we leave it in to automatically load our model file.

Setting Factory Type Information
--------------------------------

This part of the process is identical to what we explained for schema-driven
type.

Look in the ``types.xml`` file in your packages
``example/conference/profiles/default`` directory. It should now contain:

.. code-block:: xml

    <object name="portal_types">
      <object name="example.conference.program" meta_type="Dexterity FTI" />
      <object name="example.conference.session" meta_type="Dexterity FTI" />
      <object name="example.conference.presenter" meta_type="Dexterity FTI" />
    </object>


For the *Presenter* type, we have ``example.conference.presenter.xml``:

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="example.conference.presenter" meta_type="Dexterity FTI"
         xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        i18n:domain="example.conference">

      <!-- Basic metadata -->
      <property name="title" i18n:translate="">Presenter</property>
      <property name="description" i18n:translate="">Conference Presenter</property>
      <property name="icon_expr">string:${portal_url}/document_icon.png</property>
      <property name="factory">example.conference.presenter</property>
      <property name="global_allow">True</property>
      <property name="filter_content_types">True</property>
      <property name="allowed_content_types" />
      <property name="allow_discussion">False</property>

      <!-- schema and class used for content items -->
      <property name="schema">example.conference.presenter.IPresenter</property>
      <property name="klass">example.conference.presenter.Presenter</property>

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

Note that this is addable anywhere.
