Installing Dexterity
====================

*How to install Dexterity and use it in your project*

Dexterity is distributed as a number of eggs, published on
`PyPI <http://pypi.python.org>`_. The
`plone.app.dexterity <http://pypi.python.org/pypi/plone.app.dexterity>`_
egg pulls in all the required dependencies and should get you up and
running. This how-to explains what you need to do use Dexterity in a
standard Plone buildout.

Installing Dexterity on Plone 4.3
---------------------------------

Note: Plone 4.3 is the latest release of Plone. Dexterity is included
with Plone 4.3, but must be activated via the "Add-ons" configlet in site setup.

**If you wish to follow the examples in this manual, you must do one extra
installation step:** activate the `grok` extra for Dexterity.
To do so, add the following line to the `eggs` section of yor buildout::

    eggs =
        Plone
        ...
        plone.app.dexterity [grok]

**Important: If you installed Dexterity on a Plone site that you
upgraded to Plone 4.3, you must include the relations extra. Otherwise
your site will have a broken intid utility.**

    eggs =
        Plone
        ...
        plone.app.dexterity [grok,relations]


Installing Dexterity on Plone 4.2
---------------------------------

Plone 4.2 is the previous stable release of Plone. The Plone KGS (known
good set of package versions) includes version pins for the packages
that make up Dexterity, so all you need to do is add plone.app.dexterity
to the eggs in your buildout, and re-run the buildout::

    [buildout]
    extensions = buildout.dumppickedversions
    unzip = true
    parts = instance
    extends =
        http://dist.plone.org/release/4.2.1/versions.cfg
    versions = versions
    develop =

    [instance]
    recipe = plone.recipe.zope2instance
    user = admin:admin
    http-address = 8080
    debug-mode = on
    verbose-security = on
    eggs =
        Plone
        plone.app.dexterity

Note that:

-   We use the
    `buildout.dumppickedversions <http://pypi.python.org/pypi/buildout.dumppickedversions>`_
    extension to help show what versions buildout picked for any
    dependencies not pinned in the buildout. This helps trace any
    dependency issues.
-   We extend the official Plone release known good set for Plone 4.2.1.
-   In the instance configuration, we load the *Plone* egg and
    *plone.app.dexterity*. The latter will pull in all the Dexterity
    dependencies.
-   Since *plone.app.dexterity* configures a *z3c.autoinclude* entry
    point, there is no need to load a separate ZCML slug.

Your own buildout may be more extensive. The developer manual shows a
more comprehensive one with some debugging tools, for example. However,
the buildout above should be enough for creating types through the web.
If you are using a package that itself depends on plone.app.dexterity,
then the second eggs line becomes superfluous as well, of course.

Installing Dexterity on older versions of Plone
-----------------------------------------------

Prior to Plone 4.2, the official Plone KGS did not include version pins
for the packages that make up Dexterity. Instead, you can extend a KGS
from the `good-py service <http://good-py.appspot.com>`_. That looks like
this::

    [buildout]
    extensions = buildout.dumppickedversions
    unzip = true
    parts = instance
    extends =
        http://good-py.appspot.com/release/dexterity/1.2.1?plone=4.1.6
    versions = versions
    develop =

    [instance]
    recipe = plone.recipe.zope2instance
    user = admin:admin
    http-address = 8080
    debug-mode = on
    verbose-security = on
    eggs =
        Plone
        plone.app.dexterity

Notice that the extends line has been changed to point at good-py and
specify both a particular version of Dexterity and a particular version
of Plone. good-py returns a set of versions that will work for that
combination.

Dexterity 1.2.1 is the last version of Dexterity supported for Plone <
4.2. No version of Dexterity is compatible with Plone < 3.3.
