Creating and registering behaviors
====================================

**How to create a basic behavior that provides form fields**

The following example is based on the `collective.gtags`_ product, which
comes with a behavior that adds a *tags* field to the “Categorization”
fieldset, storing the actual tags in the Dublin Core *Subject* field.

*collective.gtags* is a standard package, with a *configure.zcml*, a
GenericSetup profile, and a number of modules. We won’t describe those
here, though, since we are only interested in the behavior.

First, there are a few dependencies in *setup.py*:

.. code-block:: python

          install_requires=[
              ...,
              'plone.behavior',
              'plone.directives.form',
              'zope.schema',
              'zope.interface',
              'zope.component',
              'rwproperty',
          ],

The dependency on *plone.directives.form* is there to support form
fields. If your behavior does not require form fields, you can skip this
dependency. The *rwproperty* dependency provides some convenience
decorators that are used in the behavior adapter factory class.

Next, we have *behaviors.zcml*, which is included from *configure.zcml*
and contains all necessary configuration to set up the behaviors. It
looks like this:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:plone="http://namespaces.plone.org/plone"
        xmlns:grok="http://namespaces.zope.org/grok"
        i18n_domain="collective.gtags">

        <include package="plone.behavior" file="meta.zcml" />

        <include package="plone.directives.form" file="meta.zcml" />
        <include package="plone.directives.form" />

        <grok:grok package=".behaviors" />

        <plone:behavior
            title="GTags"
            description="Use the Dublin Core Subject (keywords) field for Google Code like tags."
            provides=".behaviors.ITags"
            factory=".behaviors.Tags"
            />

    </configure>

We first include the *plone.behavior meta.zcml* file, so that we get
access to the *<plone:behavior />* ZCML directive.

The next three lines include *plone.directives.form* and its *meta.zcml*
file, and then invoke the *grok* action on the *behaviors* module. This
is not directly related to the behavior, but rather to the configuration
of a schema interface that provides form fields and display hints to
*plone.autoform* (and thus Dexterity’s standard add and edit forms). If
your behavior is not a form field provider, you can omit these lines.
Similarly, if you have grokked the entire package elsewhere with
*<grok:grok package=“.” />*, you can omit the *<grok:grok
package=“.behaviors” />* line. Otherwise, adjust it to reflect the
module or package where your behaviors are kept.

The behavior itself is registered with the *<plone:behavior />*
directive. We set a *title* and a *description*, and then speicfy the
**behavior interface** with the *provides* attribute. This attribute is
required, and is used to construct the unique name for the behavior. In
this case, the behavior name is *collective.gtags.behaviors.ITags*, the
full dotted name to the behavior interface. When the behavior is enabled
for a type, it will be possible to adapt instances of that type to
*ITags*. That adaptation will invoke the factory specified by the
*factory* attribute.

The *behaviors.py* module looks like this:

::

    """Behaviours to assign tags (to ideas).

    Includes a form field and a behaviour adapter that stores the data in the
    standard Subject field.
    """

    from rwproperty import getproperty, setproperty

    from zope.interface import implements, alsoProvides
    from zope.component import adapts

    from plone.directives import form
    from collective.gtags.field  import Tags

    from Products.CMFCore.interfaces import IDublinCore

    from collective.gtags import MessageFactory as _

    class ITags(form.Schema):
        """Add tags to content
        """

        form.fieldset(
                'categorization',
                label=_(u'Categorization'),
                fields=('tags',),
            )

        tags = Tags(
                title=_(u"Tags"),
                description=_(u"Applicable tags"),
                required=False,
                allow_uncommon=True,
            )

    alsoProvides(ITags, form.IFormFieldProvider)

    class Tags(object):
        """Store tags in the Dublin Core metadata Subject field. This makes
        tags easy to search for.
        """
        implements(ITags)
        adapts(IDublinCore)

        def __init__(self, context):
            self.context = context

        @getproperty
        def tags(self):
            return set(self.context.Subject())
        @setproperty
        def tags(self, value):
            if value is None:
                value = ()
            self.context.setSubject(tuple(value))

We first define the *ITags* interface, which is also the behavior
interface. Here, we define a single attribute, *tags*, but we could also
have added methods and additional fields if required. Naturally, these
need to be implemented by the behavior adapter.

Since we want this behavior to provide form fields, we derive the
behavior interface from *form.Schema* and set form hints using
*plone.directives.form*(remember that these will only take effect if the
package is *grokked*). We also mark the *ITags* interface with
*IFormFieldProvider* to signal that it should be processed for form
fields by the standard forms. See the `Dexterity Developer Manual`_ for
more information about setting form hints in schema interfaces.

If your behavior does not provide form fields, you can just derive from
*zope.interface.Interface* and omit the *alsoProvides()* line.

Next, we write the class that implements the behavior adapter and acts
the adapter factory. Notice how it implements the behavior interface
(*ITags*), and adapts a broad interface *(IDublinCore*). The behavior
cannot be enabled on types not supporting this interface. In many cases,
you will omit the *adapts()* line, provided your behavior is generic
enough to work on any context.

The adapter is otherwise identical to any other adapter. It implements
the interface, here by storing values in the *Subject* field. The use of
*getproperty* and *setproperty* from the `rwproperty`_ package is for
convenience only.

.. _Dexterity Developer Manual: ../index.html
.. _rwproperty: http://pypi.python.org/pypi/rwproperty
.. _collective.gtags: http://svn.plone.org/svn/collective/collective.gtags
