How is Dexterity related to Archetypes?
=======================================

Dexterity is an alternative to Archetypes, Plone's venerable content
type framework. Being more recent, Dexterity has been able to learn from
some of the mistakes that were made Archetypes, and - more importantly -
leverage some of the technologies that did not exist when Archetypes was
first conceived.

An exhaustive comparison is beyond the scope of this FAQ, but some of
the main differences include:

-   Dexterity is able to leverage many technologies that come with newer
    versions of CMF and Zope 3. This means that the Dexterity framework
    contains significantly less code than Archetypes. Dexterity also has
    better automated test coverage.
-   Dexterity is more modular where Archetypes is more monolithic. This
    promises to make it easier to support things like SQL
    database-backed types, alternative workflow systems,
    instance-specific sub-types and so on. It also means that many of
    the components developed for Dexterity, such as the through-the-web
    schema editor, the "behaviors" system, or the forms construction API
    (plone.autoform) are re-usable in other contexts, e.g. to build
    standalone forms or even to augment existing Archetypes-based types.
-   Archetypes has its own Schema implementation which is incompatible
    with the interface-based approached found in zope.interface and
    zope.schema. The latter is used throughout the Zope stack to
    describe components and build forms. Various techniques exist to
    bridge the Archetypes schema to the Zope 3 schema notation, but none
    are particularly attractive.
-   Archetypes uses accessor and mutator methods to get/set values.
    These are generated and scribbled onto a class at startup. Dexterity
    uses attribute notation, so whereas in Archetypes you may write
    *context.getFirstName()*, in Dexterity you would write
    *context.first\_name*.
-   Archetypes has its own implementation of fields and widgets. It is
    difficult to re-use these in standalone forms or templates, because
    they are tied to the idea of a content object. Dexterity uses the
    de-facto standard z3c.form library instead, which means that the
    widgets used for standalone forms are the same as those used for
    content type add- and edit forms.
-   Archetypes does not support add forms. Dexterity does, via z3c.form.
    This means that Dexterity types do not need to use the
    *portal\_factory* hack to avoid stale objects in content space, and
    are thus significantly faster and less error prone.
-   Archetypes requires a chunk of boilerplate in your product's
    *initialize()* method (and requires that your package is registered
    as a Zope 2 product) and elsewhere. It requires a particular
    sequence of initialisation calls to register content classes, run
    the class generator to add accessors/mutators, and set up
    permissions. Dexterity does away with all that boilerplate, and
    tries to minimise repetition.
-   It is possible to extend the schemata of existing Archetypes types
    with the *archetypes.schemaextender* product, although this adds
    some performance overhead and relies on a somewhat awkward
    programming technique. Dexterity types were built to be extensible
    from the beginning, and it is possible to declaratively turn on or
    off aspects of a type (such as Dublin Core metadata, locking
    support, ratings, tagging, etc) with re-usable "behaviors".
-   Dexterity is built from the ground up to support through-the-web
    type creation. There are products that achieve the same thing with
    Archetypes types, but they have to work around a number of
    limitations in the design of Archetypes that make them somewhat
    brittle or slow. Dexterity also allows types to be developed jointly
    through-the-web and on the filesystem. For example, a schema can be
    written in Python and then extended through the web.

All that said, Archetypes is still a significantly more mature
framework, used in thousands of real-world deployments. Dexterity is
still new. As it moves towards version 1.0 and beyond, we hope that it
will be a viable alternative to Archetypes in many projects, but if you
are happy with Archetypes, you should not immediately rush to rewrite
your types to use Dexterity.

There are also some things that Dexterity does not yet support, or, more
commonly, services that Plone ships with that currently assume all
content objects are built using Archetypes. The current list of "gaps"
can be found in the [Dexterity issue
tracker](http://code.google.com/p/dexterity/issues/list). You should
take a look at this before deciding whether Dexterity will work for you.
If in doubt, don't hesitate to write to the [Dexterity mailing
list](http://groups.google.com/group/dexterity-development) and ask for
advice.

Dexterity, Archetypes and the future of Plone
---------------------------------------------

At the time of writing (as of Plone 3.3), it is likely that Dexterity
will form some part of Plone's future as we move to Plone 4 and Plone 5.
The default page content type in Plone 5 may use Dexterity, or at least
some of Dexterity's components and concepts, instead of Archetypes.

None of this is actually decided, though. The final decision will be up
to the framework team and release manager for Plone 5 and beyond. For
Plone 4, it is safe to assume the default content type story won't
change, although Plone 4 is likely to include some fixes and backports
that will make Dexterity a bit easier to install and use. It is possible
that parts of Dexterity may be moved into the Plone core in Plone 4.2.

Archetypes is still the recommended, documented, supported and most
widely used way to create content types for Plone 3, and will almost
certainly remain so for Plone 4. It is not going to go away any time
soon. We obviously hope that Dexterity will be an attractive choice for
many people, but if you're not an "early adopter" type of person, we
would recommend that you stick with Archetypes until Dexterity has seen
a 1.0 final, and probably a 1.1 or 1.2, to be safe.

Finally, whilst Dexterity and Archetypes share very little code, they
are also similar in many ways. Your type has a schema, from which forms
are generated. The type is installed in the *portal\_types* tool, and is
subject to workflow and security, may have an add permission, may have
custom views, and so on. If you are familiar with Archetypes, you should
be able to pick up Dexterity pretty easily.
