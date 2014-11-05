Event handlers
---------------

**Adding custom event handlers for your type**

So far, we have mainly been concerned with content types’ schemata and
forms created from these. However, we often want to add more dynamic
functionality, reacting when something happens to objects of our type.
In Zope, that usually means writing event subscribers.

Zope’s event model is *synchronous*. When an event is broadcast (via the
``notify()`` function from the `zope.event`_ package), for example from the
``save`` action of an add form, all registered event handlers will be
called. There is no guarantee of which order the event handlers will be
called in, however.

Each event is described by an interface, and will typically carry some
information about the event. Some events are known as *object events*,
and provide ``zope.component.interfaces.IObjectEvent``. These have an
``object`` attribute giving access to the (content) object that the event
relates to. Object events allow event handlers to be registered for a
specific type of object as well as a specific type of event.

Some of the most commonly used event types in Plone are shown below.
They are all object events.

``zope.lifecycleevent.interfaces.IObjectCreatedEvent``
    fired by the standard add form just after an object has been created,
    but before it has been added on the container. Note that it is often
    easier to write a handler for ``IObjectAddedEvent`` (see below), because
    at this point the object has a proper acquisition context.

``zope.lifecycleevent.interfaces.IObjectModifiedEvent``
    fired by the standard edit form when an object has been modified.

``zope.lifecycleevent.interfaces.IObjectAddedEvent``
    fired when an object has been added to its container. The container is
    available as the ``newParent`` attribute, and the name the new item holds
    in the container is available as ``newName``.

``zope.lifecycleevent.interfaces.IObjectRemovedEvent``
    fired when an object has been removed from its container. The container
    is available as the ``oldParent`` attribute, and the name the item held
    in the container is available as ``oldName``.

``zope.lifecycleevent.interfaces.IObjectMovedEvent``
    fired when an object is added to, removed from, renamed in, or moved
    between containers. This event is a super-type of ``IObjectAddedEvent``
    and ``IObjectRemovedEvent``, shown above, so an event handler registered
    for this interface will be invoked for the ‘added’ and ‘removed’ cases
    as well. When an object is moved or renamed, all of ``oldParent``,
    ``newParent``, ``oldName`` and ``newName`` will be set.

``Products.CMFCore.interfaces.IActionSucceededEvent``
    fired when a workflow event has completed. The ``workflow`` attribute
    holds the workflow instance involved, and the ``action`` attribute holds
    the action (transition) invoked.

Event handlers can be registered using ZCML with the ``<subscriber />``
directive, but when working with Dexterity types, we’ll more commonly
use the ``grok.subscriber()`` in Python code.

As an example, let’s add an event handler to the ``Presenter`` type that
tries to find users with matching names matching the presenter id, and
send these users an email.

First, we require a few additional imports at the top of ``presenter.py``::

    from zope.lifecycleevent.interfaces import IObjectAddedEvent
    from Products.CMFCore.utils import getToolByName

Then, we’ll add the following event subscriber after the schema
definition::

    @grok.subscribe(IPresenter, IObjectAddedEvent)
    def notifyUser(presenter, event):
        acl_users = getToolByName(presenter, 'acl_users')
        mail_host = getToolByName(presenter, 'MailHost')
        portal_url = getToolByName(presenter, 'portal_url')

        portal = portal_url.getPortalObject()
        sender = portal.getProperty('email_from_address')

        if not sender:
            return

        subject = "Is this you?"
        message = "A presenter called %s was added here %s" % (presenter.title, presenter.absolute_url(),)

        matching_users = acl_users.searchUsers(fullname=presenter.title)
        for user_info in matching_users:
            email = user_info.get('email', None)
            if email is not None:
                mail_host.secureSend(message, email, sender, subject)

There are many ways to improve this rather simplistic event handler, but
it illustrates how events can be used. The first argument to
``grok.subscribe()`` is an interface describing the object type. For
non-object events, this is omitted. The second argument is the event
type. The arguments to the function reflects these two, so the first
argument is the ``IPresenter`` instance and the second is an
``IObjectAddedEvent`` instance.

.. _zope.event: http://pypi.python.org/pypi/zope.event
