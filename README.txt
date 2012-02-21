.. contents:: Table of Contents
   :depth: 1

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
  packages should has as few dependencies as possible, and should declare their
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

.. _`installation guide`: http://plone.org/products/dexterity/documentation/how-to/install

Then log in to Plone, go to Site Setup, and go to the ``Dexterity Types``
control panel to get started creating content types through the web.

Or read the `Dexterity developer manual`_ to get started developing
Dexterity content types on the filesystem.

This release of Dexterity is compatible with Plone 3, 4, and 4.1.

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

* `FAQ`_
* `Dexterity Developer Manual`_
* `How to create reusable behaviors for Dexterity types`_

.. _`FAQ`: http://plone.org/products/dexterity/documentation/faq
.. _`Dexterity developer manual`: http://plone.org/products/dexterity/documentation/manual/developer-manual
.. _`How to create reusable behaviors for Dexterity types`: http://plone.org/products/dexterity/documentation/manual/behaviors

The following documents are not Dexterity-specific, but will likely be useful
to users of Dexterity:

* `Schema-driven forms manual`_
* `five.grok manual`_

.. _`Schema-driven forms manual`: http://plone.org/products/dexterity/documentation/manual/schema-driven-forms
.. _`five.grok manual`: http://plone.org/products/dexterity/documentation/manual/five.grok


Mailing list
============

The `dexterity-development group`_ provides a place to discuss development
and use of Dexterity.

.. _`dexterity-development group`: http://groups.google.com/group/dexterity-development

Issue tracker
=============

Please report issues in our `Google Code issue tracker`_.

.. _`Google Code issue tracker`: http://code.google.com/p/dexterity/issues


Contributed Packages
====================

The Dexterity known good set (KGS) of version pins includes a number of
contributed packages that are not installed by default:

plone.app.referenceablebehavior
  Adds support for the Archetypes reference engine to Dexterity content, so
  that Dexterity items can be referenced from Archetypes items. Requires
  Plone 4.1.

plone.app.stagingbehavior
  Adds support for staging Dexterity content, based on plone.app.iterate.
  Requires Plone 4.1.

plone.app.versioningbehavior
  Adds support for storing historic versions of Dexterity content, based on
  Products.CMFEditions. Requires Plone 4.0 or greater.

collective.z3cform.datagridfield
  A z3c.form widget for editing lists of subobjects via a tabular UI.


Contributing
============

Most Dexterity code is owned by the `Plone Foundation`_ and maintained in the
`Plone svn repository`_. We're happy to share commit access so that you can
share code with us, but first you must sign the `Plone contributor agreement`_.

.. _`Plone Foundation`: http://plone.org/foundation
.. _`Plone svn repository`: http://svn.plone.org/plone
.. _`Plone contributor agreement`: http://plone.org/foundation/contributors-agreement

Dexterity wouldn't be possible without the hard work of a lot of people, including:

* Martin Aspeli
* Jian Aijun
* Wichert Akkerman
* Jonas Baumann
* JC Brand
* David Brenneman
* Thomas Buchberger
* Joel Burton
* Roche Compaan
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
* Marco Martinez
* Steve McMahon
* Jason Mehring
* Alec Mitchell
* Daniel Nouri
* Ross Patterson
* Franco Pellegrini
* Martijn Pieters
* Maurits van Rees
* Johannes Raggam
* Lennart Regebro
* Laurence Rowe
* Israel Saeta Perez
* Hanno Schlichting
* Christian Schneider
* Carsten Senger
* Jon Stahl
* Carsten Senger
* Eric Steele
* Gaudenz Steinlin
* Dorneles Tremea
* Sean Upton
* Hector Velarde
* Sylvain Viollon
* Matthew Wilkes
* Matt Yoder
* Andi Zeidler

(Please add your name if we have neglected to.)
