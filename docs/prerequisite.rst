Prerequisites
==============

**Setting up a Dexterity project**

Preparing a development environment
-----------------------------------

First, get a working Plone installation. If you don't already have one, the
easiest way to do so is to use one of Plone's installers. Note that for
development purposes, you may use a `standalone` (non-ZEO), non-root install.

Second, add our standard development tools. If you've used one of our
installers, developer tool configurations are in a separate file,
``develop.cfg``. Once your site is running, you may activate the development
configuration by using the command:

.. code-block:: console

    bin/buildout -c develop.cfg

rather than simply running ``bin/buildout``. The `develop.cfg` config file
extends the existing buildout.cfg.

If you've created yor own buildout.cfg file rather than using one of the
installers, you'll need to add an equivalent development configuration. The
easiest way to do so is to pick up a copy from the `Unified Installer's github repository <https://github.com/plone/Installers-UnifiedInstaller/blob/master/base_skeleton/develop.cfg>`_.

The key tools that you'll need, both supplied by develop.cfg, are:

1. A ZopeSkel configuration to supply a package skeleton builder; and
2. A test runner.

.. note::

    If you are using Plone earlier than 4.3, you'll need to add
    `zopeskel.dexterity` to the eggs list for the zopeskel part. This supplies
    the Dexterity skeleton.

Creating a package
-------------------

**Setting up a package to house your content types**

.. note::

    We're going to build a package named example.conference. You may find a
    completed version of it in the `Collective repository
    <https://github.com/collective/example.conference>`_.

Typically, our content types will live in a separate package to our theme and
other customisations.

To create a new package, we can start with *ZopeSkel* and the ``dexterity``
template.

.. note::

    Nothing that we're doing actually requires ZopeSkel or the zopeskel.dexterity skeleton package. It's just a quick way of getting started.

We run the following from the ``src/`` directory

.. code-block:: console

  $ ../bin/zopeskel dexterity example.conference

You may accept all the default suggestions. This will create a directory named
``example.conference`` inside ./src.

Now, take a look at the setup.py file in your new package. Edit the `author,`
`author_email` and `description` fields as you wish. Note a couple of parts of
the generated setup.py file:

.. code-block:: python

          install_requires=[
              ...
              'plone.app.dexterity',
              ...
          ],
          ...
          entry_points="""
          # -*- Entry points: -*-
          [z3c.autoinclude.plugin]
          target = plone
          """,

The addition of `plone.app.dexterity` to our install requirements
assures that we'll have dexterity loaded. Our example
code won't work without it. The specification of `plone` as a
z3c.autoinclude.plugin entry point ensures that we won't need to separately
specify our zcml in buildout.

Now, let's take a look at ``configure.zcml`` in the examples/conference directory of our project. Again, we want to note a few parts:

.. code-block:: xml

    <configure ...>

      <includeDependencies package="." />

      <browser:resourceDirectory
          name="example.conference"
          directory="resources"
          />

      <genericsetup:registerProfile
          name="default"
          title="Example Dexterity Product"
          directory="profiles/default"
          description="Extension profile for Example Dexterity Product"
          provides="Products.GenericSetup.interfaces.EXTENSION"
          />

    </configure>

Here, with the ``includeDependencies`` tag we automatically include the ZCML configuration for all
packages listed under ``install_requires`` in ``setup.py``.
The alternative would be to manually add a line like
``<include package="plone.app.dexterity" />`` for each dependency.

The ``browser.resourceDirectory`` command creates a directory for static resources that we want to make available through the web.

Finally, we register a GenericSetup profile to make the type
installable, which we will build up over the next several sections.

When you've got your project tuned up, return to your buildout/instance directory and edit buildout.cfg to add ``example.conference`` to your eggs list and ``src/example.conference`` to your develop sources list::

.. code-block:: ini

    eggs =
        Plone
        ...
        example.conference

    ...
    develop =
        ...
        src/example.conference

Run ``bin/buildout -c develop.cfg`` to add your new product to the
configuration. (Or, just bin/buildout if you don't have a separate develop.cfg.)

The buildout should now configure Plone, Dexterity and the
*example.conference* package.

We are now ready to start adding types.
