Installing Dexterity
====================

*How to install Dexterity and use it in your project*

.. note::

    Dexterity is an **already installed part of Plone 5.x**, no action is needed here.


Installing Dexterity on Plone 4.3
---------------------------------

Dexterity is included with Plone 4.3, but must be activated via the "Add-ons" configlet in site setup.

.. note::
    Important: If you installed Dexterity on a Plone site that you upgraded to Plone 4.3,
    you must include the relations extra ``plone.app.dexterity [relations]``.
    Otherwise your site will have a broken intid utility.**

Dexterity is distributed as a number of eggs, published on `PyPI <http://pypi.python.org>`_.
The `plone.app.dexterity <http://pypi.python.org/pypi/plone.app.dexterity>`_ egg pulls in all the required dependencies and should get you up and running.
This how-to explains what you need to do use Dexterity in a standard Plone buildout.
