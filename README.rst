.. contents:: Table of Contents

.. note:: ``2.1.1`` is the last Plone 4 compatible release.


Introduction
============

Dexterity wants to make some things really easy. These are:

* Create a "real" content type entirely through-the-web without having to
  know programming.
* As a business user, create a schema using visual or through-the-web tools,
  and augment it with adapters, event handlers, and other Python code written
  on the filesystem by a Python programmer.
* Create content types in filesystem code quickly and easily, without losing
  the ability to customise any aspect of the type and its operation later if
  required.
* Support general "behaviours" that can be enabled on a custom type in a
  declarative fashion. Behaviours can be things like title-to-id naming,
  support for locking or versioning, or sets of standard metadata with
  associated UI elements.
* Easily package up and distribute content types defined through-the-web, on
  the filesystem, or using a combination of the two.

Philosophy
==========

Dexterity is designed with a specific philosophy in mind. This can be
summarised as follows:

Reuse over reinvention
  As far as possible, Dexterity should reuse components and technologies that
  already exist. More importantly, however, Dexterity should reuse concepts that
  exist elsewhere. It should be easy to learn Dexterity by analogy, and to work
  with Dexterity types using familiar APIs and techniques.

Small over big
  Mega-frameworks be damned. Dexterity consists of a number of specialised
  packages, each of which is independently tested and reusable. Furthermore,
  packages should have as few dependencies as possible, and should declare their
  dependencies explicitly. This helps keep the design clean and the code
  manageable.

Natural interaction over excessive generality
  The Dexterity design was driven by several use cases that express the way in
  which we want people to work with Dexterity. The end goal is to make it easy
  to get started, but also easy to progress from an initial prototype to a
  complex set of types and associated behaviours through step-wise learning and
  natural interaction patterns. Dexterity aims to consider its users - be they
  business analysts, light integrators or Python developers, and be they new or
  experienced - and cater to them explicitly with obvious, well-documented,
  natural interaction patterns.

Real code over generated code
  Generated code is difficult to understand and difficult to debug when it
  doesn't work as expected. There is rarely, if ever, any reason to scribble
  methods or 'exec' strings of Python code.

Zope 3 over Zope 2
  Although Dexterity does not pretend to work with non-CMF systems, as many
  components as possible should work with plain Zope 3, and even where there are
  dependencies on Zope 2, CMF or Plone, they should - as far as is practical -
  follow Zope 3 techniques and best practices. Many operations (e.g. managing
  objects in a folder, creating new objects or manipulating objects through a
  defined schema) are better designed in Zope 3 than they were in Zope 2.

Zope concepts over new paradigms
  We want Dexterity to be "Zope-ish". Zope is a mature, well-designed (well,
  mostly) and battle tested platform. We do not want to invent brand new
  paradigms and techniques if we can help it.

Automated testing over wishful thinking
  "Everything" should be covered by automated tests. Dexterity necessarily has a
  lot of moving parts. Untested moving parts tend to come loose and fall on
  people's heads. Nobody likes that.

Getting started
===============

Please read the `installation guide`_ to get Dexterity up and running.

.. _`installation guide`: http://docs.plone.org/external/plone.app.dexterity/docs/install.html

Then log in to Plone, go to Site Setup, and go to the ``Dexterity Types``
control panel to get started creating content types through the web.

Or read the `Dexterity Developer Manual`_ to get started developing
Dexterity content types on the filesystem.

The 2.0.x release series of Dexterity is compatible with
and included with Plone 4.3.

Upgrading
=========

If you are upgrading from a previous release of Dexterity, you need to:

1. Update your buildout with the new versions (or extend the updated KGS),
   and re-run it.
2. Restart Zope.
3. Go to the Add-ons control panel in Plone Site Setup, and run the
   upgrade steps for "Dexterity Content Types" if there are any available.

Documentation
=============

Various documentation is available:

* `Dexterity Developer Manual`_
* `How to create reusable behaviors for Dexterity types`_

.. _`Dexterity Developer Manual`: http://docs.plone.org/external/plone.app.dexterity/docs/index.html
.. _`How to create reusable behaviors for Dexterity types`: http://docs.plone.org/external/plone.app.dexterity/docs/behaviors/index.html

The following documents are not Dexterity-specific, but will likely be useful
to users of Dexterity:

* `Schema-driven forms manual`_

.. _`Schema-driven forms manual`: http://docs.plone.org/develop/addons/schema-driven-forms/index.html


Issue tracker
=============

Please report issues via the `Plone issue tracker`_.

.. _`Plone issue tracker`: https://github.com/plone/plone.app.dexterity/issues

Support
=======

Dexterity use questions may be answered via `Plone's support channels`_.

.. _`Plone's support channels`: http://plone.org/support

Contributing
============

Contributors please read the document `Process for Plone core's development <http://docs.plone.org/develop/plone-coredev/index.html>`_

Sources are at the `Plone code repository hosted at Github <https://github.com/plone/plone.app.dexterity>`_.

Dexterity wouldn't be possible without the hard work of a lot of people, including:

* Martin Aspeli
* Jian Aijun
* Wichert Akkerman
* Jonas Baumann
* David Brenneman
* Joel Burton
* Vincent Fretin
* Rok Garbas
* Anthony Gerrard
* Nathan van Gheem
* David Glick
* Craig Haynal
* Wouter Vanden Hove
* Jean-Michel Francois
* Jim Fulton
* Jamie Lentin
* Alex Limi
* Steve McMahon
* Jason Mehring
* Alec Mitchell
* Daniel Nouri
* Ross Patterson
* Maurits van Rees
* Lennart Regebro
* Laurence Rowe
* Israel Saeta Perez
* Hanno Schlichting
* Christian Schneider
* Carsten Senger
* Jon Stahl
* Eric Steele
* Gaudenz Steinlin
* Dorneles Tremea
* Sean Upton
* Sylvain Viollon
* Matthew Wilkes
* Matt Yoder
* Andi Zeidler
* Hector Velarde
* Giacomo Spettoli
* Jens Klein

(Please add your name if we have neglected to.)
