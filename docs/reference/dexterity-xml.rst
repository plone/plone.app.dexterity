Dexterity XML
=============

**A reference for Dexterity's XML name spaces**

Introduction
------------

The schema (structure) of a Dexterity content type may be detailed in two very
different ways:

    * In Python as a Zope schema; or,

    * In XML

When you are using Dexterity's through-the-web schema editor, all your work is
being saved in the content type's Factory Type Information (FTI) as XML.
``plone.supermodel`` dynamically translates that XML into Python objects which
are used to display and edit your content objects.

The XML model of your content object may be exported from Dexterity and
incorporated into a Python package. That's typically done with code like::

    class IExampleType(form.Schema):

        form.model("models/example_type.xml")
        
or::
        
    from plone.supermodel import xmlSchema
    
    IExampleType = xmlSchema("models/example_type.xml")

XML models in a package may be directly edited. (Dexterity will probably also
include a TTW XML-model editor at some point in the future.)

This document is a reference to the tags and attributes you may use in model
XML files. This includes several form-control and security-control attributes
that are not available through the TTW schema editor.

XML Document Structure
----------------------

Dexterity requires that its model XML be well-formed XML, including name space
declarations. The typical structure of a Dexterity XML document is::

    <?xml version="1.0" encoding="UTF-8"?>
    <model xmlns="http://namespaces.plone.org/supermodel/schema"
           xmlns:form="http://namespaces.plone.org/supermodel/form"
           xmlns:security="http://namespaces.plone.org/supermodel/security">
        <schema>
            <field type="zope.schema.TextLine" name="one"
                <title>One</title>
                ... More field attributes
            </field>
            ... More fields
        </schema>
    </model>

Only the default name space (.../supermodel/schema) is required for basic
schema. The ``supermodel/form`` and ``supermodel/schema`` provide additional
attributes to control form presentation and security.

supermodel/schema fields
------------------------

Most of the supermodel/schema field tag and its attributes map directly to what's available via the TTW schema editor::

        <field name="dummy" type="zope.schema.TextLine">
          <default>abc</default>
          <description>Test desc</description>
          <max_length>10</max_length>
          <min_length>2</min_length>
          <missing_value>m</missing_value>
          <readonly>True</readonly>
          <required>False</required>
          <title>Test</title>
        </field>

The field ``type`` needs to be the full dotted name (as if it was being
imported in Python) of the field type.

Fieldsets
~~~~~~~~~

It's easy to add fieldsets by surrounding embedding fields tags in a ``fieldset`` block::

      <schema>
        ...
        <fieldset name="test"
                label="Test Fieldset"
                description="Description of test fieldset">
            <field name="three" type="zope.schema.TextLine">
              <description/>
              <title>Three</title>
            </field>
            <field name="four" type="zope.schema.TextLine">
              <description/>
              <title>Four</title>
            </field>
        </fieldset>
        ...
      </schema>


Vocabularies
~~~~~~~~~~~~

Vocabularies may be specified via dotted names using the ``source`` tag::

    <field name="dummy" type="zope.schema.Choice">
        <default>a</default>
        <description>Test desc</description>
        <missing_value/>
        <readonly>True</readonly>
        <required>False</required>
        <title>Test</title>
        <source>plone.supermodel.tests.dummy_vocabulary_instance</source>
    </field>

Where the full Python dotted-name of a Zope vocabulary in a package::

    from zope.schema.vocabulary import SimpleVocabulary

    dummy_vocabulary_instance = SimpleVocabulary.fromItems([(1, 'a'), (2, 'c')])

Or, a source binder::

    <field name="dummy" type="zope.schema.Choice">
        ...
        <source>plone.supermodel.tests.dummy_binder</source>
    </field>


With Python like::

    from zope.schema.interfaces import IContextSourceBinder

    class Binder(object):
        implements(IContextSourceBinder)

        def __call__(self, context):
            return SimpleVocabulary.fromValues(['a', 'd', 'f'])

    dummy_binder = Binder()

You may also use the ``vocabulary`` tag rather than ``source`` to refer to named vocabularies registered via the ZCA.


Internationalization
~~~~~~~~~~~~~~~~~~~~

Translation domains and message ids can be specified for text
that is interpreted as unicode. This will result in deserialization
as a zope.i18nmessageid message id rather than a basic Unicode string.

Note that we need to add the i18n namespace and a domain specification::

    <model xmlns="http://namespaces.plone.org/supermodel/schema"
           xmlns:i18n="http://xml.zope.org/namespaces/i18n"
           i18n:domain="your.application">
        <schema>

            <field type="zope.schema.TextLine" name="title">
                <title i18n:translate="yourapp_test_title">Title</title>
            </field>

        </schema>
    </model>


supermodel/form attributes
--------------------------

supermodel/form provides attributes that govern presentation and editing.

after/before
~~~~~~~~~~~~

To re-order fields, use ``form:after`` or ``form:before``.

The value should be either ``'*'``, to put the field first/last in the form,
or the name of a another field. Use ``'.fieldname'`` to refer to field in the
current schema (or a base schema). Use a fully prefixed name (e.g.
``'my.package.ISomeSchema'``) to refer to a field in another schema. Use an
unprefixed name to refer to a field in the default schema for the form.

Example::

    <field type="zope.schema.TextLine"
           name="one"
           form:after="two">
        <title>One</title>
    </field>

mode
~~~~

To turn a field into a view mode or hidden field, use ``form:mode``.  The
mode may be set for only some forms by specifying a form interface in the
same manner as for ``form:omitted``.

Example::

    <field type="zope.schema.TextLine"
            name="three"
            form:mode="z3c.form.interfaces.IEditForm:input">
        <title>Three</title>
    </field>


omitted
~~~~~~~

To omit a field from all forms, use ``form:omitted="true"``.  To omit a field
only from some forms, specify a form interface like
``form:omitted="z3c.form.interfaces.IForm:true"``. Multiple interface:value
settings may be specified, separated by spaces.

Examples::

    <field type="zope.schema.TextLine"
           name="one"
           form:omitted="true">
        <title>One</title>
    </field>

    <field type="zope.schema.TextLine" name="three"
            form:omitted="z3c.form.interfaces.IForm:true z3c.form.interfaces.IEditForm:false"
            >
        <title>Three</title>
    </field>

The latter example hides the field on everything except the edit form.


widget
~~~~~~

To set a custom widget for a field, use ``form:widget`` to give a fully
qualified name to the field widget factory.

Example::

    <field type="zope.schema.TextLine"
           name="password"
           form:widget="z3c.form.browser.password.PasswordFieldWidget">
        <title>One</title>
    </field>


Dynamic Defaults
~~~~~~~~~~~~~~~~

To set a dynamic default for a field, use a ``defaultFactory`` tag to
give a fully qualified name for a callable. The defaultFactory callable must
provide either plone.supermodel.interfaces.IDefaultFactory or
zope.schema.interfaces.IContextAwareDefaultFactory.

Example::

    <field type="zope.schema.TextLine" name="three">
        <title>Three</title>
        <defaultFactory>plone.supermodel.tests.dummy_defaultFactory</defaultFactory>
    </field>

Sample Python for the validator factory::

    @provider(IDefaultFactory)
    def dummy_defaultFactory():
        return u'something'

For a callable using context::

    @provider(IContextAwareDefaultFactory)
    def dummy_defaultCAFactory(context):
        return context.something

.. note::

    The ``defaultFactory`` tag was added in plone.supermodel 1.2.3,
    shipping with Plone 4.3.2+.


validator
~~~~~~~~~

To set a custom validator for a field, use ``form:validator`` to give a fully
qualified name to the field validator factory. The validator factory should be
a class derived from one of the validators in z3c.form.validator.

Example::

    <field type="zope.schema.TextLine"
            name="three"
            form:validator="plone.autoform.tests.test_utils.TestValidator">
        <title>Three</title>
    </field>

Sample Python for the validator factory::

    class TestValidator(z3c.form.validator.SimpleFieldValidator):

        def validate(self, value):
            super(TestValidator, self).validate(value)
            raise Invalid("Test")


supermodel/security attributes
------------------------------

read-permission/write-permission
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To set a read or write permission, use ``security:read-permission`` or
``security:write-permission``. The value should be the name of an
``IPermission`` utility.

Example::

    <field type="zope.schema.TextLine"
            name="one"
            security:read-permission="zope2.View"
            security:write-permission="cmf.ModifyPortalContent">
        <title>One</title>
    </field>
