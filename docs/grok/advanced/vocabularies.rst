Vocabularies
-------------

**Creating your own static and dynamic vocabularies**

Vocabularies are normally used in conjunction with selection fields, and
are supported by the `zope.schema`_ package, with widgets provided by
`z3c.form`_.

Selection fields use the ``Choice`` field type. To allow the user to
select a single value, use a ``Choice`` field directly::

    class IMySchema(model.Schema):
        myChoice = schema.Choice(...)

For a multi-select field, use a ``List``, ``Tuple``, ``Set`` or
``Frozenset`` with a ``Choice`` as the ``value_type``::

    class IMySchema(model.Schema):
        myList = schema.List(..., value_type=schema.Choice(...))

The choice field must be passed one of the following arguments:

- ``values`` can be used to give a list of static values;
- ``source`` can be used to refer to an ``IContextSourceBinder`` or
  ``ISource`` instance;
- ``vocabulary`` can be used to refer to an ``IVocabulary`` instance or
  (more commonly) a string giving the name of an ``IVocabularyFactory``
  named utility.

In the remainder of this section, we will show the various techniques
for defining vocabularies through several iterations of a new field
added to the Program type allowing the user to pick the organiser
responsible for the program.

Static vocabularies
~~~~~~~~~~~~~~~~~~~~

Our first attempt uses a static list of organisers. We use the message
factory to allow the labels (term titles) to be translated. The values
stored in the ``organizer`` field will be a unicode object representing
the chosen label, or ``None`` if no value is selected::

    from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

    organizers = SimpleVocabulary(
        [SimpleTerm(value=u'Bill', title=_(u'Bill')),
         SimpleTerm(value=u'Bob', title=_(u'Bob')),
         SimpleTerm(value=u'Jim', title=_(u'Jim'))]
        )

    organizer = schema.Choice(
                title=_(u"Organiser"),
                vocabulary=organizers,
                required=False,
            )

Since ``required`` is ``False``, there will be a :guilabel:`no value` option
in the drop-down list.

Dynamic sources
~~~~~~~~~~~~~~~~

The static vocabulary is obviously a bit limited. Not only is it
hard-coded in Python, it also does not allow separation of the stored
values and the labels shown in the selection widget.

We can make a one-off dynamic vocabulary using a context source binder.
This is simply a callable (usually a function or an object with a
``__call__`` method) that provides the ``IContextSourceBinder``
interface and takes a ``context`` parameter. The ``context`` argument is the
context of the form (i.e. the folder on an add form, and the content
object on an edit form). The callable should return a vocabulary, which
is most easily achieved by using the ``SimpleVocabulary`` class from
`zope.schema`_.

Here is an example using a function to return all users in a particular
group::

    from zope.schema.interfaces import IContextSourceBinder
    from zope.schema.vocabulary import SimpleVocabulary
    from Products.CMFCore.utils import getToolByName

    @grok.provider(IContextSourceBinder)
    def possibleOrganizers(context):
        acl_users = getToolByName(context, 'acl_users')
        group = acl_users.getGroupById('organizers')
        terms = []

        if group is not None:
            for member_id in group.getMemberIds():
                user = acl_users.getUserById(member_id)
                if user is not None:
                    member_name = user.getProperty('fullname') or member_id
                    terms.append(SimpleVocabulary.createTerm(member_id, str(member_id), member_name))

        return SimpleVocabulary(terms)

We use the PAS API to get the group and its members, building a list,
which we then turn into a vocabulary.

When working with vocabularies, you’ll come across some terminology that
is worth explaining:

- A *term* is an entry in the vocabulary. The term has a value. Most
  terms are *tokenised* terms which also have a token, and some terms
  are *titled*, meaning they have a title that is different to the
  token.
- The *token* must be an ASCII string. It is the value passed with the
  request when the form is submitted. A token must uniquely identify a
  term.
- The *value* is the actual value stored on the object. This is not
  passed to the browser or used in the form. The value is often a
  unicode object, but can be any type of object.
- The *title* is a unicode object or translatable message. It is used
  in the form.

The ``SimpleVocabulary`` class contains two class methods that can be used
to create vocabularies from lists:

``fromValues()``
    takes a simple list of values and returns a tokenised vocabulary where
    the values are the items in the list, and the tokens are created by
    calling ``str()`` on the values.
``fromItems()``
    takes a list of ``(token, value)`` tuples and creates a tokenised
    vocabulary with the token and value specified.

You can also instantiate a ``SimpleVocabulary`` yourself and pass a list
of terms in the initialiser.
The ``createTerm()`` class method can be used to create a term from a
``value``, ``token`` and ``title``. Only the value is required.

In the example above, we have chosen to create a ``SimpleVocabulary`` from
terms with the user id used as value and token, and the user’s full name
as a title.

To use this context source binder, we use the ``source`` argument to the
``Choice`` constructor::

    organizer = schema.Choice(
        title=_(u"Organiser"),
        source=possibleOrganizers,
        required=False,
    )

Parameterised sources
~~~~~~~~~~~~~~~~~~~~~~

We can improve this example by moving the group name out of the
function, allowing it to be set on a per-field basis. To do so, we turn
our ``IContextSourceBinder`` into a class that is initialised with the
group name::

    class GroupMembers(object):
        """Context source binder to provide a vocabulary of users in a given
        group.
        """

        grok.implements(IContextSourceBinder)

        def __init__(self, group_name):
            self.group_name = group_name

        def __call__(self, context):
            acl_users = getToolByName(context, 'acl_users')
            group = acl_users.getGroupById(self.group_name)
            terms = []

            if group is not None:
                for member_id in group.getMemberIds():
                    user = acl_users.getUserById(member_id)
                    if user is not None:
                        member_name = user.getProperty('fullname') or member_id
                        terms.append(SimpleVocabulary.createTerm(member_id, str(member_id), member_name))

            return SimpleVocabulary(terms)

Again, the source is set using the ``source`` argument to the ``Choice``
constructor::

    organizer = schema.Choice(
        title=_(u"Organiser"),
        source=GroupMembers('organizers'),
        required=False,
    )

When the schema is initialised on startup, a ``GroupMembers`` object
is instantiated, storing the desired group name. Each time the
vocabulary is needed, this object will be called (i.e. the
``__call__()`` method is invoked) with the context as an argument,
expected to return an appropriate vocabulary.

Named vocabularies
~~~~~~~~~~~~~~~~~~~~

Context source binders are great for simple dynamic vocabularies. They
are also re-usable, since you can import the source from a single
location and use it in multiple instances.

Sometimes, however, we want to provide an additional level of
decoupling, by using *named* vocabularies. These are similar to context
source binders, but are components registered as named utilities,
referenced in the schema by name only. This allows local overrides of
the vocabulary via the Component Architecture, and makes it easier to
distribute vocabularies in third party packages.

.. note::

    Named vocabularies cannot be parameterised in the way as we did
    with the ``GroupMembers`` context source binder, since they are looked up
    by name only.

We can turn our first "members in the *organizers* group" vocabulary
into a named vocabulary by creating a named utility providing
``IVocabularyFactory``, like so::

    from zope.schema.interfaces import IVocabularyFactory
    ...

    class OrganizersVocabulary(object):
        grok.implements(IVocabularyFactory)

        def __call__(self, context):
            acl_users = getToolByName(context, 'acl_users')
            group = acl_users.getGroupById('organizers')
            terms = []

            if group is not None:
                for member_id in group.getMemberIds():
                    user = acl_users.getUserById(member_id)
                    if user is not None:
                        member_name = user.getProperty('fullname') or member_id
                        terms.append(SimpleVocabulary.createTerm(member_id, str(member_id), member_name))

            return SimpleVocabulary(terms)

    grok.global_utility(OrganizersVocabulary, name=u"example.conference.Organizers")

.. note::

    By convention, the vocabulary name is prefixed with the package name, to
    ensure uniqueness.

We can make use of this vocabulary in any schema by passing its name to
the ``vocabulary`` argument of the ``Choice`` field constructor::

    organizer = schema.Choice(
        title=_(u"Organiser"),
        vocabulary=u"example.conference.Organizers",
        required=False,
    )

Some common vocabularies
~~~~~~~~~~~~~~~~~~~~~~~~

As you might expect, there are a number of standard vocabularies that
come with Plone. These are found in the `plone.app.vocabularies`_
package. Some of the more useful ones include:

``plone.app.vocabularies.AvailableContentLanguages``
    a list of all available content languages;
``plone.app.vocabularies.SupportedContentLanguages``
    a list of currently supported content languages;
``plone.app.vocabularies.Roles``
    the user roles available in the site;
``plone.app.vocabularies.PortalTypes``
    a list of types installed in ``portal_types``;
``plone.app.vocabularies.ReallyUserFriendlyTypes``
    a list of those types that are likely to mean something to users;
``plone.app.vocabularies.Workflows``
    a list of workflows;
``plone.app.vocabularies.WorkflowStates``
    a list of all states from all workflows;
``plone.app.vocabularies.WorkflowTransitions``
    a list of all transitions from all workflows.

In addition, the package `plone.principalsource`_ provides several
vocabularies that are useful for selecting users and groups in a
Dexterity context:

``plone.principalsource.Users``
    provides users

``plone.principalsource.Groups``
    provides groups

``plone.principalsource.Principals``
    provides security principals (users or groups)

Importantly, these sources are not iterable, which means that you cannot
use them to provide a list of all users in the site. This is
intentional: calculating this list can be extremely expensive if you
have a large site with many users, especially if you are connecting to
LDAP or Active Directory. Instead, you should use a search-based source
such as one of these.

We will use one of these together with an auto-complete widget to
finalise our ``organizer`` field. To do so, we need to add
``plone.principalsource`` as a dependency of ``example.conference``. In
``setup.py``, we add::

    install_requires=[
          ...
          'plone.principalsource',
      ],

.. note::

    Since we use an ``<includeDependencies />`` line in ``configure.zcml``,
    we do not need a separate ``<include />`` line in ``configure.zcml`` for
    this new dependency.

The ``organizer`` field now looks like::

    organizer = schema.Choice(
        title=_(u"Organiser"),
        vocabulary=u"plone.principalsource.Users",
        required=False,
    )

The autocomplete selection widget
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``organizer`` field now has a query-based source. The standard
selection widget (a drop-down list) is not capable of rendering such a
source. Instead, we need to use a more powerful widget. For a basic
widget, see `z3c.formwidget.query`_, but in a Plone context, you will
more likely want to use `plone.formwidget.autocomplete`_, which extends
``z3c.formwidget.query`` to provide friendlier user interface.

The widget is provided with `plone.app.dexterity`_, so we do not need to
configure it ourselves. We only need to tell Dexterity to use this
widget instead of the default, using a form widget hint as shown
earlier. At the top of ``program.py``, we add the following import::

    from plone.formwidget.autocomplete import AutocompleteFieldWidget

.. note::

    If we were using a multi-valued field, such as a ``List`` with a
    ``Choice`` ``value_type``, we would use the
    ``AutocompleteMultiFieldWidget`` instead.

In the ``IProgram`` schema (which, recall, derives from ``model.Schema`` and
is therefore processed for form hints at startup), we then add the
following::

    form.widget(organizer=AutocompleteFieldWidget)
    organizer = schema.Choice(
        title=_(u"Organiser"),
        vocabulary=u"plone.principalsource.Users",
        required=False,
    )

You should now see a dynamic auto-complete widget on the form, so long
as you have JavaScript enabled. Start typing a user name and see what
happens. The widget also has fall-back for non-JavaScript capable
browsers.

.. _plone.app.dexterity: http://pypi.python.org/pypi/plone.app.dexterity
.. _plone.principalsource: http://pypi.python.org/pypi/plone.principalsource
.. _plone.app.vocabularies: http://pypi.python.org/pypi/plone.app.vocabularies
.. _z3c.form: http://pypi.python.org/pypi/z3c.form
.. _zope.schema: http://pypi.python.org/pypi/zope.schema
.. _z3c.formwidget.query: http://pypi.python.org/pypi/z3c.formwidget.query
.. _plone.formwidget.autocomplete: http://pypi.python.org/pypi/plone.formwidget.autocomplete
