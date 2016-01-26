Testing behaviors
=====================

**How to write unit tests for behaviors**

Behaviors, like any other code, should be tested. If you are writing a
behavior with just a marker interface or schema interface, it is
probably not necessary to test the interface. However, any actual code,
such as a behavior adapter factory, ought to be tested.

Writing a behavior integration test is not very difficult if you are
happy to depend on Dexterity in your test. You can create a dummy type
by instantiating a Dexterty FTI in *portal\_types* and enable your
behavior by adding its interface name to the *behaviors* property.

In many cases, however, it is better not to depend on Dexterity at all.
It is not too difficult to mock what Dexterity does to enable behaviors
on its types. The following example is taken from *collective.gtags* and
tests the *ITags* behavior we saw on the first page of this manual.

::

    Behaviors
    =========

    This package provides a behavior called `collective.gtags.behaviors.ITags`.
    This adds a `Tags` field called `tags` to the "Categorization" fieldset, with
    a behavior adapter that stores the chosen tags in the Subject metadata field.

    To learn more about the `Tags` field and how it works, see `tagging.rst`.

    Test setup
    ----------

    Before we can run these tests, we need to load the collective.gtags
    configuration. This will configure the behavior.

        >>> configuration = """\
        ... <configure
        ...      xmlns="http://namespaces.zope.org/zope"
        ...      i18n_domain="collective.gtags">
        ...
        ...     <include package="Products.Five" file="meta.zcml" />
        ...     <include package="collective.gtags" file="behaviors.zcml" />
        ...
        ... </configure>
        ... """

        >>> from StringIO import StringIO
        >>> from zope.configuration import xmlconfig
        >>> xmlconfig.xmlconfig(StringIO(configuration))

    This behavior can be enabled for any `IDublinCore`. For the purposes of
    testing, we will use the CMFDefault Document type and a custom
    IBehaviorAssignable adapter to mark the behavior as enabled.

        >>> from Products.CMFDefault.Document import Document

        >>> from plone.behavior.interfaces import IBehaviorAssignable
        >>> from collective.gtags.behaviors import ITags
        >>> from zope.component import adapts
        >>> from zope.interface import implements
        >>> class TestingAssignable(object):
        ...     implements(IBehaviorAssignable)
        ...     adapts(Document)
        ...
        ...     enabled = [ITags]
        ...
        ...     def __init__(self, context):
        ...         self.context = context
        ...
        ...     def supports(self, behavior_interface):
        ...         return behavior_interface in self.enabled
        ...
        ...     def enumerate_behaviors(self):
        ...         for e in self.enabled:
        ...             yield queryUtility(IBehavior, name=e.__identifier__)

        >>> from zope.component import provideAdapter
        >>> provideAdapter(TestingAssignable)

    Behavior installation
    ---------------------

    We can now test that the behavior is installed when the ZCML for this package
    is loaded.

        >>> from zope.component import getUtility
        >>> from plone.behavior.interfaces import IBehavior
        >>> tags_behavior = getUtility(IBehavior, name='collective.gtags.behaviors.ITags')
        >>> tags_behavior.interface
        <InterfaceClass collective.gtags.behaviors.ITags>

    We also expect this behavior to be a form field provider. Let's verify that.

        >>> from plone.directives.form import IFormFieldProvider
        >>> IFormFieldProvider.providedBy(tags_behavior.interface)
        True

    Using the behavior
    ------------------

    Let's create a content object that has this behavior enabled and check that
    it works.

        >>> doc = Document('doc')
        >>> tags_adapter = ITags(doc, None)
        >>> tags_adapter is not None
        True

    We'll check that the `tags` set is built from the `Subject()` field:

        >>> doc.setSubject(['One', 'Two'])
        >>> doc.Subject()
        ('One', 'Two')

        >>> tags_adapter.tags == set(['One', 'Two'])
        True

        >>> tags_adapter.tags = set(['Two', 'Three'])
        >>> doc.Subject() == ('Two', 'Three')
        True

This test tries to prove that the behavior is correctly installed and
works as intended on a suitable content class. It is not a true unit
test, of course. For that, we would simply test the *Tags* adapter
directly on a dummy context, but that is not terribly interesting, since
all it does is convert sets to tuples.

First, we configure the package. To keep the test small, we limit
ourselves to the *behaviors.zcml* file, which in this case will suffice.
We still need to include a minimal set of ZCML from Five.

Next, we implement an *IBehaviorAssignable*adapter. This is a low-level
component used by *plone.behavior* to determine if a behavior is enabled
on a particular object. Dexterity provides an implementation that checks
the type’s FTI. Our test version is much simpler - it hardcodes the
supported behaviors.

With this in place, we first check that the *IBehavior* utility has been
correctly registered. This is essentially a test to show that we’ve used
the *<plone:behavior />* directive as intended. We also verify that our
schema interface is an *IFormFieldsProvider*. For a non-form behavior,
we’d obviously omit this.

Finally, we test the behavior. We’ve chosen to use CMFDefault’s
*Document* type for our test, as the behavior adapter requires an object
providing *IDublinCore*. If we were less lazy, we’d write our own class
and implement *IDublinCore* directly. However, in many cases, the types
from CMFDefault are going to provide convenient test fodder.

Obviously, if our behavior was more complex, we’d add more intricate
tests. By the last section of the doctest, we have enough context to
test the adapter factory.

To run the test, we need a test suite. In *tests.py*, we have:

::

    import doctest
    import unittest
    from zope.app.testing import setup

    def setUp(test):
        pass

    def tearDown(test):
        setup.placefulTearDown()

    def test_suite():
        return unittest.TestSuite((
            doctest.DocFileSuite(
                'behaviors.rst',
                setUp=setUp, tearDown=tearDown,
                optionflags=doctest.NORMALIZE_WHITESPACE|doctest.ELLIPSIS),
            ))

This runs the *behaviors.rst* doctest from the same directory as the
*tests.py* file. To run the test, we can use the usual test runner:

::

    $ ./bin/instance test -s collective.gtags

A note about marker interfaces
------------------------------

Note that marker interface support depends on code that is implemented
in Dexterity and is non-trivial to reproduce in a test. If you need a
marker interface in a test, set it manually with
*zope.interface.alsoProvides*, or write an integration test with
Dexterity content.
