Form schema hints
==================

**Directives which can be used to configure forms from schemata**

Dexterity uses the `plone.autoform`_ package to configure its
`z3c.form`_-based add and edit forms. This allows a schema to be
annotated with “form hints”, which are used to configure the form.

The easiest way to apply form hints in Python code is to use the
directives from `plone.autoform` and `plone.supermodel`.
For the directives to work, the schema
must derive from *plone.supermodel.model.Schema*. Directives can be
placed anywhere in the class body. By convention they are kept next to
the fields they apply to.

For example, here is a schema that omits a field:

.. code-block:: python

    from plone.autoform import directives as form
    from plone.supermodel import model
    from zope import schema


    class ISampleSchema(model.Schema):

        title = schema.TextLine(title=u"Title")

        form.omitted('additionalInfo')
        additionalInfo = schema.Bytes()

The form directives take parameters in the form of a list of field
names, or a set of field name/value pairs as keyword arguments. Each
directive can be used zero or more times.

Form directives
---------------

These form directives are included in the *plone.autoform.directives* module:

+-----------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Name            | Description                                                                                                                                                                                                                                                                                                                                  |
+=================+==============================================================================================================================================================================================================================================================================================================================================+
| widget          | Specify an alternate widget for a field. Pass the field name as a key and a widget as the value. The widget can either be a z3c.form widget instance or a string giving the dotted name to one.                                                                                                                                              |
+-----------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| omitted         | Omit one or more fields from forms. Takes a sequence of field names as parameters.                                                                                                                                                                                                                                                           |
+-----------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| mode            | Set the widget mode for one or more fields. Pass the field name as a key and the string ‘input’, ‘display’ or ‘hidden’ as the value.                                                                                                                                                                                                         |
+-----------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| order\_before   | Specify that a given field should be rendered before another. Pass the field name as a key and name of the other field as a value. If the other field is in a supplementary schema (i.e. one from a behaviour), its name will be e.g. “IOtherSchema.otherFieldName”. Alternatively, pass the string “\*” to put a field first in the form.   |
+-----------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| order\_after    | The inverse of order\_before(), putting a field after another. Passing “\*” will put the field at the end of the form.                                                                                                                                                                                                                       |
+-----------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

These form directives are included in the *plone.supermodel.directives* module:

+-----------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| primary         | Designate a given field as the primary field in the schema. This is not used for form rendering, but is used for WebDAV marshaling of the content object.                                                                                                                                                                                    |
+-----------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| fieldset        | Creates a fieldset (rendered in Plone as a tab on the edit form).                                                                                                                                                                                                                                                                            |
+-----------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

The code sample below illustrates each of these directives:

.. code-block:: python

    from plone.autoform import directives as form
    from plone.supermodel import model
    from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
    from zope import schema


    class ISampleSchema(model.Schema):

        # A fieldset with id 'extra' and label 'Extra information' containing
        # the 'footer' and 'dummy' fields. The label can be omitted if the
        # fieldset has already been defined.

        form.fieldset('extra',
                label=u"Extra information",
                fields=['footer', 'dummy']
            )

        # Here a widget is specified as a dotted name.
        # The body field is also designated as the priamry field for this schema

        form.widget(body='plone.app.z3cform.wysiwyg.WysiwygFieldWidget')
        model.primary('body')
        body = schema.Text(
                title=u"Body text",
                required=False,
                default=u"Body text goes here"
            )

        # The widget can also be specified as an object

        form.widget(footer=WysiwygFieldWidget)
        footer = schema.Text(
                title=u"Footer text",
                required=False
            )

        # An omitted field. Use form.omitted('a', 'b', 'c') to omit several fields

        form.omitted('dummy')
        dummy = schema.Text(
                title=u"Dummy"
            )

        # A field in 'hidden' mode

        form.mode(secret='hidden')
        secret = schema.TextLine(
                title=u"Secret",
                default=u"Secret stuff"
            )

        # This field is moved before the 'description' field of the standard
        # IBasic behaviour, if this is in use.

        form.order_before(importantNote='IBasic.description')
        importantNote = schema.TextLine(
                title=u"Important note",
            )

Security directives
-------------------

The security directives in the *plone.autoform.directives* module are
shown below. Note that these are also used to control reading and
writing of fields on content instances.

+---------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Name                | Description                                                                                                                                                                                                                          |
+=====================+======================================================================================================================================================================================================================================+
| read\_permission    | Set the (Zope 3) name of a permission required to read the field’s value. Pass the field name as a key and the permission name as a string value. Among other things, this controls the field’s appearance in display forms.         |
+---------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| write\_permission   | Set the (Zope 3) name of a permission required to write the field’s value. Pass the field name as a key and the permission name as a string value. Among other things, this controls the field’s appearance in add and edit forms.   |
+---------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

The code sample below illustrates each of these directives:

.. code-block:: python

    from plone.autoform import directives as form
    from plone.supermodel import model
    from zope import schema

    class ISampleSchema(model.Schema):

        # This field requires the 'cmf.ReviewPortalContent' to be read and
        # written

        form.read_permission(reviewNotes='cmf.ReviewPortalContent')
        form.write_permission(reviewNotes='cmf.ReviewPortalContent')
        reviewNotes = schema.Text(
                title=u"Review notes",
                required=False,
            )

.. _plone.autoform: http://pypi.python.org/pypi/plone.autoform
.. _z3c.form: http://docs.zope.org/z3c.form
