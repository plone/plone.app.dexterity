Providing marker interfaces
=============================

**How to use behaviors to set marker interfaces on instances of a given type.**

Sometimes, it is useful for objects that provide a particular behavior
to also provide a specific marker interface. For example, you can
register a viewlet for a particular marker and use a behavior to enable
that marker on all instances of a particular content type. The viewlet
will then only show up when the behavior is enabled. The same principle
can be applied to event handlers, views and other components.

.. note::
    There is usually no need to use markers to enable a custom adapter since
    a standard behavior is already a conditional adapter. However, in
    certain cases, you may want to provide one or more adapters to an
    interface that is not the behavior interface, e.g. to use a particular
    extension point provided by another component. In this case, it may
    easier to set a marker interface and provide an adapter from this
    marker.

*plone.behavior’s* marker support can be used in two ways:

-  As the behavior interface itself. In this case, there is no behavior
   adapter factory. The behavior interface and the marker interface are
   one and the same.
-  As a supplement to a standard behavior adapter. In this case, a
   factory is provided, and the behavior interface (which the behavior
   adapter factory implements) is different to the marker interface.

Primary marker behaviors
------------------------

In the first case, where the behavior interface and the marker interface
are the same, you can simply use the *<plone:behavior />*directive
without a *factory*. For example:

.. code-block:: xml

        <plone:behavior
            title="Pony viewlet"
            description="Shows a pony next to the content"
            provides=".behaviors.IWantAPony"
            />

One could imagine a viewlet based on `plone.pony`_ registered for the
*IWantAPony* marker interface. If the behavior is enabled for a
particular object, *IWantAPony.providedBy(object)* would be true.

Supplementary marker behaviors
------------------------------

In the second case, we want to provide a behavior interface with a
behavior adapter factory as usual (e.g. with some form fields and a
custom storage or a few methods implemented in an adapter), but we also
need a custom marker. Here, we use both the *provides* and *marker*
attributes to *<plone:behavior />* to reference the two interfaces, as
well as a *factory*.

To show a slightly more interesting example, here is a behavior from a
project that lets content authors with particular permissions
(*iz.EditOfficialReviewers* and *iz.EditUnofficialReviewers*), nominate
the “official” and any “unofficial” reviewers for a given content item.
The behavior provides the necessary form fields to support this, but it
also sets a marker interface that enables an *ILocalRoleProvider*
adapter to automatically grant local roles to the chosen reviewers, as
well as a custom indexer that lists the reviewers.

The ZCML registration looks like this:

.. code-block:: xml

        <plone:behavior
            title="Reviewers"
            description="The ability to assign a list of official and/or unofficial reviewers to an item, granting those users special powers."
            provides=".reviewers.IReviewers"
            factory="plone.behavior.AnnotationStorage"
            marker=".reviewers.IReviewersMarker"
            />

Notice the use of the *AnnotationStorage* factory. This is a re-usable
factory that can be used to easily create behaviors from schema
interfaces that store their values in annotations. We’ll describe this
in more detail later. We could just as easily have provided our own
factory in this example.

This whole package is grokked, so in *configure.zcml* we have:

.. code-block:: xml

        <grok:grok package="." />

The *reviewers.py* module contains the following:

::

    """Behavior to enable certain users to nominate reviewers

    Includes form fields, an indexer to make it easy to find the items with
    specific reviewers, and a local role provider to grant the Reviewer and
    OfficialReviewer roles appropriately.
    """

    from five import grok

    from zope.interface import alsoProvides, Interface

    from plone.directives import form
    from zope import schema

    from plone.formwidget.autocomplete.widget import AutocompleteMultiFieldWidget

    from borg.localrole.interfaces import ILocalRoleProvider
    from plone.indexer.interfaces import IIndexer
    from Products.ZCatalog.interfaces import IZCatalog

    from iz.behaviors import MessageFactory as _

    class IReviewers(form.Schema):
        """Support for specifying official and unofficial reviewers
        """

        form.fieldset(
                'ownership',
                label=_(u'Ownership'),
                fields=('official_reviewers', 'unofficial_reviewers'),
            )

        form.widget(official_reviewers=AutocompleteMultiFieldWidget)
        form.write_permission(official_reviewers='iz.EditOfficialReviewers')
        official_reviewers = schema.Tuple(
                title=_(u'Official reviewers'),
                description=_(u'People or groups who may review this item in an official capacity.'),
                value_type=schema.Choice(title=_(u"Principal"), source="plone.principalsource.Principals"),
                required=False,
                missing_value=(), # important!
            )

        form.widget(unofficial_reviewers=AutocompleteMultiFieldWidget)
        form.write_permission(unofficial_reviewers='iz.EditUnofficialReviewers')
        unofficial_reviewers = schema.Tuple(
                title=_(u'Unofficial reviewers'),
                description=_(u'People or groups who may review this item in a supplementary capacity'),
                value_type=schema.Choice(title=_(u"Principal"), source="plone.principalsource.Principals"),
                required=False,
                missing_value=(), # important!
            )

    alsoProvides(IReviewers, form.IFormFieldProvider)

    class IReviewersMarker(Interface):
        """Marker interface that will be provided by instances using the
        IReviewers behavior. The ILocalRoleProvider adapter is registered for
        this marker.
        """

    class ReviewerLocalRoles(grok.Adapter):
        """Grant local roles to reviewers when the behavior is used.
        """

        grok.implements(ILocalRoleProvider)
        grok.context(IReviewersMarker)
        grok.name('iz.behaviors.reviewers')

        def getRoles(self, principal_id):
            """If the user is in the list of reviewers for this item, grant
            the Reader, Editor and Contributor local roles.
            """

            c = IReviewers(self.context, None)
            if c is None or (not c.official_reviewers and not c.unofficial_reviewers):
                return ()

            if principal_id in c.official_reviewers:
                return ('Reviewer', 'OfficialReviewer',)
            elif principal_id in c.unofficial_reviewers:
                return ('Reviewer',)

            return ()

        def getAllRoles(self):
            """Return a list of tuples (principal_id, roles), where roles is a
            list of roles for the given user id.
            """

            c = IReviewers(self.context, None)
            if c is None or (not c.official_reviewers and not c.unofficial_reviewers):
                return

            seen = set ()

            for principal_id in c.official_reviewers:
                seen.add(principal_id)
                yield (principal_id, ('Reviewer', 'OfficialReviewer'),)

            for principal_id in c.unofficial_reviewers:
                if principal_id not in seen:
                    yield (principal_id, ('Reviewer',),)

    class ReviewersIndexer(grok.MultiAdapter):
        """Catalog indexer for the 'reviewers' index.
        """

        grok.implements(IIndexer)
        grok.adapts(IReviewersMarker, IZCatalog)
        grok.name('reviewers')

        def __init__(self, context, catalog):
            self.reviewers = IReviewers(context)

        def __call__(self):
            official = self.reviewers.official_reviewers or ()
            unofficial = self.reviewers.unofficial_reviewers or ()
            return tuple(set(official + unofficial))

Note that the *iz.EditOfficialReviewers* and
*iz.EditUnofficialReviewers* permissions are defined and granted
elsewhere.

This is quite a complex behavior, but hopefully you can see what’s going
on:

-  There is a standard schema interface, which is grokked for form hints
   using *plone.directives.form* and marked as an *IFormFieldProvider*.
   It uses *plone.formwidget.autocomplete* and *plone.principalsource*
   to implement the fields.
-  We define a marker interface (*IReviewersMarker*) and register this
   with the *marker* attribute of the *<plone:behavior />* directive.
-  We define an adapter from this marker to *ILocalRoles* from
   *borg.localrole*. Here, we have chosen to use *grokcore.component*
   (via *five.grok*) to register the adapter. We could have used an
   *<adapter />* ZCML statement as well, of course.
-  Similarly, we define a multi-adapter to *IIndexer*, as provided by
   *plone.indexer*. Again, we’ve chosen to use
   convention-over-configuration via *five.grok* to register this.

Although this behavior provides a lot of functionality, it is no more
difficult for integrators to use than any other: they would simply list
the behavior interface (*iz.behaviors.reviewers.IReviewers* in this
case) in the FTI, and all this functionality comes to life. This is the
true power of behaviors: developers can bundle up complex functionality
into re-usable behaviors, which can then be enabled on a per-type basis
by integrators (or the same developers in lazier moments).

.. _plone.pony: http://pypi.python.org/pypi/plone.pony
