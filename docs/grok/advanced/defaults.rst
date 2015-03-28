Defaults
---------

**Default values for fields on add forms**

It is often useful to calculate a default value for a field. This value
will be used on the add form, before the field is set.

To continue with our conference example, let’s set the default values
for the ``start`` and ``end`` dates to one week in the future and ten days
in the future, respectively. We can do this by adding the following to
``program.py``:

.. code-block:: python

    @form.default_value(field=IProgram['start'])
    def startDefaultValue(data):
        # To get hold of the folder, do: context = data.context
        return datetime.datetime.today() + datetime.timedelta(7)

    @form.default_value(field=IProgram['end'])
    def endDefaultValue(data):
        # To get hold of the folder, do: context = data.context
        return datetime.datetime.today() + datetime.timedelta(10)

We also need to import ``datetime`` at the top of the file, of course.

Notice how the functions specify a particular schema field that they
provide the default value for. The decorator will actually register
these as “value adapters” for `z3c.form <http://pypi.python.org/pypi/z3c.form>`_, but you probably don’t need to
worry about that.

The ``data`` argument is an object that contains an attribute for each
field in the schema. On the add form, most of these are likely to be
``None``, but on a different form, the values may be populated from the
context. The ``data`` object also has a ``context`` attribute that you can
use to get the form’s context. For add forms, that’s the containing
folder; for other forms, it is normally a content object being edited or
displayed. If you need to look up tools (``getToolByName``) or acquire a
value from a parent object, use ``data.context`` as the starting point,
e.g.:

.. code-block:: python

    from Products.CMFCore.utils import getToolByName
    ...
    catalog = getToolByName(data.context, 'portal_catalog')

The value returned by the method should be a value that’s allowable for
the field. In the case of ``Datetime`` fields, that’s a Python ``datetime``
object.

It is possible to provide different default values depending on the type
of context, a request layer, the type of form, or the type of widget
used. See the `plone.directives.form`_ documentation for more details.

For example, if you wanted to have a differently calculated default for
a particular form, you could use a decorator like:

.. code-block:: python

    @form.default_value(field=IProgram['start'], form=FormClass)

We’ll cover creating custom forms later in this manual.

.. _plone.directives.form: http://pypi.python.org/pypi/plone.directives.form

If the default_value decorator is not working, check that you have installed
plone.directives.form installed with buildout or in your setup.py. Further
ensure that you have "groked" your package.
