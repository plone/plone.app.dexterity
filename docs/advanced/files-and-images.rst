Files and images
-----------------

**Working with file and image fields, including BLOBs**

Plone has dedicated ``File`` and ``Image`` types, and it is often preferable
to use these for managing files and images. However, it is sometimes
useful to treat fields on an object as binary data. When working with
Dexterity, you can accomplish this by using `plone.namedfile`_ and
`plone.formwidget.namedfile`_.

The `plone.namedfile`_ package includes four field types, all found in
the ``plone.namedfile.field`` module:

- ``NamedFile`` stores non-BLOB files. This is useful for small files
  when you don’t want to configure BLOB storage.
- ``NamedImage`` stores non-BLOB images.
- ``NamedBlobFile`` stores BLOB files (see note below). It is otherwise
  identical to ``NamedFile``.
- ``NamedBlobImage`` stores BLOB images (see note below). It is otherwise
  identical to ``NamedImage``.

In use, the four field types are all pretty similar. They actually store
persistent objects of type ``plone.namedfile.NamedFile``,
``plone.namedfile.NamedImage``, ``plone.namedfile.NamedBlobFile`` and ``plone.namedfile.NamedBlobImage``,
respectively. Note the different module! These objects have attributes
like ``data``, to access the raw binary data, ``contentType``, to get a MIME
type, and ``filename``, to get the original filename. The image values
also support ``_height`` and ``_width`` to get image dimensions.

To use the non-BLOB image and file fields, it is sufficient to depend on
``plone.formwidget.namedfile``, since this includes ``plone.namefile`` as a
dependency. We prefer to be explicit in ``setup.py``, however, since we
will actually import directly from ``plone.namedfile``:

.. code-block:: ini

    install_requires=[
      ...
      'plone.namedfile',
      'plone.formwidget.namedfile',
    ],

.. note::

    Again, we do not need separate ``<include />`` lines in
    ``configure.zcml`` for these new dependencies, because we use
    ``<includeDependencies />``.

For the sake of illustration, we will add an image of the
speaker to the ``Presenter`` type. In ``presenter.py``, we add::

    from plone.namedfile.field import NamedImage

    class IPresenter(model.Schema):
        ...

        picture = NamedBlobImage(
            title=_(u"Please upload an image"),
            required=False,
        )

To use this in a view, we can either use a display widget via a
``DisplayForm``, or construct a download URL manually. Since we don’t have
a ``DisplayForm`` for the ``Presenter`` type, we’ll do the latter (of
course, we could easily turn the view into a display form as well).

In ``presenter_templates/view.pt``, we add this block of TAL::

    <div tal:define="picture nocall:context/picture"
         tal:condition="nocall:picture">
        <img tal:attributes="src string:${context/absolute_url}/@@download/picture/${picture/filename};
                             height picture/_height | nothing;
                             width picture/_width | nothing;"
            />
    </div>

This constructs an image URL using the ``@@download`` view from
``plone.namedfile``. This view takes the name of the field containing the
file or image on the traversal subpath (``/picture``), and optionally a
filename on a further sub-path. The filename is used mainly so that the
URL ends in the correct extension, which can help ensure web browsers
display the picture correctly. We also define the ``height`` and ``width``
of the image based on the values set on the object.

For file fields, you can construct a download URL in a similar way,
using an ``<a />`` tag, e.g.::

    <a tal:attributes="href string:${context/absolute_url}/@@download/some_field/${context/some_field/filename}" />

.. _z3c.blobfile: http://pypi.python.org/pypi/z3c.blobfile
.. _plone.namedfile: http://pypi.python.org/pypi/plone.namedfile
.. _plone.formwidget.namedfile: http://pypi.python.org/pypi/plone.formwidget.namedfile
.. _extra: http://peak.telecommunity.com/DevCenter/setuptools#declaring-extras-optional-features-with-their-own-dependencies
