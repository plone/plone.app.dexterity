Fields
========

**The standard schema fields**

The following tables shows the most common field types for use in
Dexterity schemata.
See the documentation on `creating schemata`_ for information about how to
use these.

Field properties
----------------

Fields are initialised with properties passed in their constructors.
To avoid having to repeat the available properties for each field, we’ll
list them once here, grouped into the interfaces that describe them.
You’ll see those interfaces again in the tables below that describe the
various field types.
Refer to the table below to see what properties a particular interface
implies.

=========== =================== ========== ===================================================
Interface   Property            Type       Description
=========== =================== ========== ===================================================
IField      title               unicode    The title of the field. Used in the widget.
\           description         unicode    A description for the field. Used in the widget.
\           required            bool       Whether or not the field is required. Used for
                                           form validation. The default is ``True``.
\           readonly            bool       Whether or not the field is read-only. Default
                                           is ``False``.
\           default                        The default value for the field. Used in forms
                                           and sometimes as a fallback value. Must be a
                                           valid value for the field if set. The default
                                           is ``None``.
\           missing_value                  A value that represents "this field is not set".
                                           Used by form validation. Defaults to ``None``. For
                                           lists and tuples, it is sometimes useful to set
                                           this to an empty list/tuple.
IMinMaxLen  min_length          int        The minimum required length or minimum number
                                           of elements. Used for string, sequence, mapping
                                           or set fields. Default is ``0``.
\           max_length          int        The maximum allowed length or maximum number
                                           of elements. Used for string, sequence, mapping
                                           or set fields. Default is ``None`` (no check).
IMinMax     min                            The minimum allowed value. Must be a valid value
                                           for the field, e.g. for an ``Int`` field this
                                           should be an integer. Default is ``None`` (no
                                           check).
\           max                            The maximum allowed value. Must be a valid value
                                           for the field, e.g. for an Int field this should
                                           be an integer. Default is ``None`` (no check).
ICollection value_type                     Another ``Field`` instance that describes the
                                           allowable values in a list, tuple or other
                                           collection. Must be set for any collection field.
                                           One common usage is to set this to a ``Choice``,
                                           to model a multi-selection field with a vocabulary.
\           unique              bool       Whether or not values in the collection must be
                                           unique. Usually not set directly – use a ``Set``
                                           or ``Frozenset`` to guarantee uniqueness in an
                                           efficient way.
IDict       key_type                       Another ``Field`` instance that describes the
                                           allowable keys in a dictionary. Similar to the
                                           ``value_type`` of a collection. Must be set.
\           value_type                     Another ``Field`` instance that describes the
                                           allowable values in a dictionary. Similar to the
                                           ``value_type`` of a collection. Must be set.
IObject     schema              Interface  An interface that must be provided by any object
                                           stored in this field.
IRichText   default_mime_type   str        Default MIME type for the input text of a rich
                                           text field. Defaults to ``text/html``.
\           output_mime_type    str        Default output MIME type for the transformed
                                           value of a rich text field. Defaults to
                                           ``text/x-html-safe``. There must be a
                                           transformation chain in the ``portal_transforms``
                                           tool that can transform from the input value to
                                           the ``output`` value for the output property of
                                           the ``RichValue`` object to contain a value.
\           allowed_mime_types  tuple      A list of allowed input MIME types. The default
                                           is ``None``, in which case the site-wide settings
                                           (from the ``Markup`` control panel) will be used.
=========== =================== ========== ===================================================

Field types
-----------

The following tables describe the most commonly used field types,
grouped by the module from which they can be imported.

Fields in zope.schema
~~~~~~~~~~~~~~~~~~~~~

================= ============ ================================================================================= ================================
Name              Type         Description                                                                       Properties
================= ============ ================================================================================= ================================
Choice            N/A          Used to model selection from a vocabulary, which must be supplied.                See `vocabularies`_.
                               Often used as the ``value_type`` of a selection field. The value
                               type is the value of the terms in the vocabulary.
Bytes             str          Used for binary data.                                                             IField, IMinMaxLen
ASCII             str          ASCII text (multi-line).                                                          IField, IMinMaxLen
BytesLine         str          A single line of binary data, i.e. a ``Bytes`` with newlines                      IField, IMinMaxLen
                               disallowed.
ASCIILine         str          A single line of ASCII text.                                                      IField, IMinMaxLen
Text              unicode      Unicode text (multi-line). Often used with a WYSIWYG widget,                      IField, IMinMaxLen
                               although the default is a text area.
TextLine          unicode      A single line of Unicode text.                                                    IField, IMinMaxLen
Bool              bool         ``True`` or ``False``.                                                            IField
Int               int, long    An integer number. Both ints and longs are allowed.                               IField, IMinMax
Float             float        A floating point number.                                                          IField, IMinMax
Tuple             tuple        A tuple (non-mutable).                                                            IField, ICollection, IMinMaxLen
List              list         A list.                                                                           IField, ICollection, IMinMaxLen
Set               set          A set.                                                                            IField, ICollection, IMinMaxLen
Frozenset         frozenset    A frozenset (non-mutable).                                                        IField, ICollection, IMinMaxLen
Password          unicode      Stores a simple string, but implies a password widget.                            IField, IMinMaxLen
Dict              dict         Stores a dictionary. Both ``key_type`` and ``value_type`` must be set to fields.  IField, IMinMaxLen, IDict
Datetime          datetime     Stores a Python ``datetime`` (not a Zope 2 ``DateTime``).                         IField, IMinMax
Date              date         Stores a python ``date``.                                                         IField, IMinMax
Timedelta         timedelta    Stores a python ``timedelta``.                                                    IField, IMinMax
SourceText        unicode      A textfield intended to store source text (e.g. HTML or Python code).             IField, IMinMaxLen
Object            N/A          Stores a Python object that conforms to the interface given as the                IField, IObject
                               ``schema``. There is no standard widget for this.
URI               str          A URI (URL) string.                                                               IField, MinMaxLen
Id                str          A unique identifier – either a URI or a dotted name.                              IField, IMinMaxLen
DottedName        str          A dotted name string.                                                             IField, IMinMaxLen
InterfaceField    Interface    A Zope interface.                                                                 IField
Decimal           Decimal      Stores a Python ``Decimal``. Requires version 3.4 or later of                     IField, IMinMax
                               `zope.schema`_. Not available by default in Zope 2.10.
================= ============ ================================================================================= ================================

Fields in ``plone.namedfile.field``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See `plone.namedfile`_ and `plone.formwidget.namedfile`_ for more
details.

=============== =============== ================================================================================= ==========
Name            Type            Description                                                                       Properties
=============== =============== ================================================================================= ==========
NamedFile       NamedFile       A binary uploaded file. Normally used with the widget from                        IField
                                `plone.formwidget.namedfile`_.
NamedImage      NamedImage      A binary uploaded image. Normally used with the widget from                       IField
                                `plone.formwidget.namedfile`_.
NamedBlobFile   NamedBlobFile   A binary uploaded file stored as a ZODB BLOB. Requires the ``[blobs]`` extra to   IField
                                `plone.namedfile`_. Otherwise identical to ``NamedFile``.
NamedBlobImage  NamedBlobImage  A binary uploaded image stored as a ZODB BLOB. Requires the ``[blobs]`` extra to  IField
                                `plone.namedfile`_. Otherwise identical to ``NamedImage``.
=============== =============== ================================================================================= ==========

Fields in ``z3c.relationfield.schema``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See `z3c.relationfield`_ for more details.

================= ================ ================================================================ ===============
Name              Type             Description                                                      Properties
================= ================ ================================================================ ===============
Relation          RelationValue    Stores a single ``RelationValue``.                               IField
RelationList      list             A ``List`` field that defaults to ``Relation`` as the value type See ``List``
RelationChoice    RelationValue    A ``Choice`` field intended to store ``RelationValue``’s         See ``Choice``
================= ================ ================================================================ ===============

Fields in `plone.app.textfield`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See `plone.app.textfield`_  for more details.

========= ============== ====================================================================================== ==================
Name      Type           Description                                                                            Properties
========= ============== ====================================================================================== ==================
RichText  RichTextValue  Stores a ``RichTextValue``, which encapsulates a raw text value, the source MIME type, IField, IRichText
                         and a cached copy of the raw text transformed to the default output MIME type.
========= ============== ====================================================================================== ==================

Fields in `plone.schema`_
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See `plone.schema`_  for more details.

========= ============== ====================================================================================== ==================
Name      Type           Description                                                                            Properties
========= ============== ====================================================================================== ==================
Email     str            A field containing an email address                                                    IField, IMinMaxLen
========= ============== ====================================================================================== ==================

.. _creating schemata: ../schema-driven-types.html#the-schema
.. _plone.app.textfield: http://pypi.python.org/pypi/plone.app.textfield
.. _plone.formwidget.namedfile: http://pypi.python.org/pypi/plone.formwidget.namedfile
.. _plone.namedfile: http://pypi.python.org/pypi/plone.namedfile
.. _plone.schema: http://pypi.python.org/pypi/plone.schema
.. _vocabularies: ../advanced/vocabularies.html
.. _z3c.relationfield: http://pypi.python.org/pypi/z3c.relationfield
.. _zope.schema: http://pypi.python.org/pypi/zope.schema
