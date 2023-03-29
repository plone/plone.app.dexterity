Custom views
============

**Configuring custom views and using display forms**

Simple views
------------

**Creating basic views**

So far, our types have used the default views.
They use the *display* widgets from `z3c.form`_, much like the add and edit forms use the *edit* widgets.
This is functional, but not very attractive.
Most types will need one or more custom view templates.

Dexterity types are no different from any other content type in Plone.
You can register a view for your schema interface, and it will be available on your type.
If the view is named *view*, it will be the default view, at least if you use the standard FTI configuration.
This is because the FTI’s ``default_view`` property is set to ``view``, and ``view`` is in the list of ``view_methods.``

First create a view registration with a ``<browser:page />`` ZCML directive in your ```configure.zcml`` file:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser">

      ...

      <browser:page
          name="view"
          for="example.conference.program.IProgram"
          class="example.conference.program.ProgramView"
          template="templates/programview.pt"
          permission="zope2.View"
          />

    </configure>

Secondly add a browser view in ``program.py`` as follows:

.. code-block:: python

    from Acquisition import aq_inner
    from example.conference.session import ISession
    from plone import api
    from Products.Five import BrowserView


    class ProgramView(BrowserView):

        def sessions(self):
            """Return a catalog search result of sessions to show."""

            context = aq_inner(self.context)
            catalog = api.portal.get_tool(name='portal_catalog')

            return catalog(
                object_provides=ISession.__identifier__,
                path='/'.join(context.getPhysicalPath()),
                sort_on='sortable_title')

We have added ``sessions``, a helper method which will be used in the view.

You can add any methods to the view.
They will be available to the template via the ``view`` variable.
The content object is available via ``context``.

Finally add a template in ``templates/programview.pt``:

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:metal="http://xml.zope.org/namespaces/metal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="example.conference">
    <body>

    <metal:main fill-slot="main">
        <tal:main-macro metal:define-macro="main"
            tal:define="toLocalizedTime nocall:context/@@plone/toLocalizedTime">

            <div tal:replace="structure provider:plone.abovecontenttitle" />

            <h1 class="documentFirstHeading" tal:content="context/title" />

            <div class="discreet">
                <tal:block condition="context/start">
                    <span i18n:translate="label_from">From:</span>
                    <span tal:content="python:context.start.strftime('%x %X')" />
                </tal:block>
                <tal:block condition="context/end">
                    <span i18n:translate="label_to">To:</span>
                    <span tal:content="python:context.end.strftime('%x %X')" />
                </tal:block>
            </div>

            <div tal:replace="structure provider:plone.belowcontenttitle" />

            <p class="documentDescription" tal:content="context/description" />

            <div tal:replace="structure provider:plone.abovecontentbody" />

            <div tal:content="structure context/details/output" />

            <h2 i18n:translate="heading_sessions">Sessions</h2>
            <dl>
                <tal:block repeat="session view/sessions">
                    <dt>
                        <a tal:attributes="href session/getURL"
                           tal:content="session/Title" />
                    </dt>
                    <dd tal:content="session/Description" />
                </tal:block>
            </dl>

            <div tal:replace="structure provider:plone.belowcontentbody" />

        </tal:main-macro>
    </metal:main>

    </body>
    </html>


For the most part, this template outputs the values of the various fields, using the ``sessions()`` method on the view to obtain the sessions contained within the program.

.. note::

   Notice how the ``details`` *RichText* field is output as ``tal:content="structure context/details/output"``.
   The ``structure`` keyword ensures that the rendered HTML is not escaped.
   The extra traversal to ``details/output`` is necessary because the *RichText* field actually stores a *RichTextValue* object that contains not only the raw text as entered by the user, but also a MIME type (e.g. ``text/html``) and the rendered output text.
   *RichText* fields are covered in more detail :ref:`later in this manual <richtext-label>`.

The view for ``Presenter`` is even simpler:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser">

        ...

        <browser:page
            name="view"
            for="example.conference.program.IPresenter"
            template="templates/presenterview.pt"
            permission="zope2.View"
            />

    </configure>

The template, in ``templates/presenterview.pt``, is similar to the previous template:

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:metal="http://xml.zope.org/namespaces/metal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="example.conference">
    <body>

    <metal:main fill-slot="main">
        <tal:main-macro metal:define-macro="main">

            <div tal:replace="structure provider:plone.abovecontenttitle" />

            <h1 class="documentFirstHeading" tal:content="context/title" />

            <div tal:replace="structure provider:plone.belowcontenttitle" />

            <p class="documentDescription" tal:content="context/description" />

            <div tal:replace="structure provider:plone.abovecontentbody" />

            <div tal:content="structure context/bio/output" />

            <div tal:replace="structure provider:plone.belowcontentbody" />

        </tal:main-macro>
    </metal:main>

    </body>
    </html>

Obviously, these views are very basic.
Much more interesting views could be created by putting a little more work into the templates.

You should also realise that you can create any type of view using this technique.
Your view does not have to be related to a particular content type, even.
You could set the context to ``Interface``, for example, to make a view that’s available on all types.

Display view
------------

**Using display widgets in your views**

In the previous section, we created a browser view.
This kind of view is the most common.
Sometimes we want to make use of the widgets and information in the type’s schema more directly.
For example to invoke transforms or re-use more complex HTML.

To do this, you can use a *display view*.
This is really just a view base class that knows about the schema of a type.
We will use an example in ``session.py``, with a template in ``templates/sessionview.pt``.

.. note::
   *Display view* involve the same type of overhead as add- and edit-forms.
   If you have complex content type with many behaviors, fieldsets and
   widget hints, you may notice a slow-down. This can be a problem
   on high volume sites.

The new view class is pretty much the same as before, except that we derive from ``plone.dexterity.browser.view.DefaultView``:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser">

        ...

        <browser:page
            name="view"
            for="example.conference.program.ISession"
            class="example.conference.session.SessionView"
            template="templates/sessionview.pt"
            permission="zope2.View"
            />

    </configure>

.. code-block:: python

    from plone.dexterity.browser.view import DefaultView

    class SessionView(DefaultView):
        pass

This gives our view a few extra properties that we can use in the template:

``view.w``
    a dictionary of all the display widgets, keyed by field names.
    For fields provided by behaviors, that is usually prefixed with the behavior interface name (``IBehaviorInterface.field_name``).
    For the default schema, unqualified names apply.

``view.widgets``
    contains a list of widgets in schema order for the default fieldset.

``view.groups``
    contains a list of fieldsets in fieldset order.

``view.fieldsets``
    contains a dictionary mapping fieldset name to fieldset.

``widgets``
     On a fieldset (group), you can access a ``widgets`` list to get widgets in that fieldset.

The ``w`` dict is the most commonly used.

The ``templates/sessionview.pt`` template contains the following:

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:metal="http://xml.zope.org/namespaces/metal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          lang="en"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="example.conference">
    <body>

    <metal:main fill-slot="main">
        <tal:main-macro metal:define-macro="main">
            <div tal:replace="structure provider:plone.abovecontenttitle" />
            <h1 class="documentFirstHeading" tal:content="context/title" />
            <div tal:replace="structure provider:plone.belowcontenttitle" />
            <p class="documentDescription" tal:content="context/description" />
            <div tal:replace="structure provider:plone.abovecontentbody" />
            <div tal:content="structure view/w/details/render" />
            <div tal:replace="structure provider:plone.belowcontentbody" />
        </tal:main-macro>
    </metal:main>

    </body>
    </html>

Notice how we use expressions like ``view/w/details/render`` (where ``details`` is the field name) to get the rendering of a widget.
Other properties include ``__name__``, the field name, and ``label``, the field title.

.. _z3c.form: http://pypi.python.org/pypi/z3c.form
