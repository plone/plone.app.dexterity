Value and validator adaptors
============================

**Handy Decorators to set computed defaults and dynamic validators**

Decorators from `plone.directives.form`_ allow you to set dynamic
defaults and validators for schema fields. These are used outside the
interface class, after its declaration.

Defaults
~~~~~~~~

Use the plone.directives.form.default\_value decorator to create an
adaptor to dynamically set a default. For example, to set a Datetime
field to default to the current time:

::

    import datetime
    from plone.directives import form
    from zope import schema

    class IMySchema(form.Schema):

        start = schema.Datetime(title=u"Start Date")

    @form.default_value(field=IMySchema['start'])
    def startDefaultValue(data):
        return datetime.datetime.today()

Validators
~~~~~~~~~~

Use the plone.directives.form.validator decorator to create an adaptor
to validate field input. For example, to validate that a field is not
entered all uppercase:

::

    from plone.directives import form
    from zope import schema

    class IMySchema(form.Schema):

        title = schema.TextLine(title=u"Title")

    @form.validator(field=IMySchema['title'])
    def validateTitle(value):
        if value and value == value.upper():
            raise schema.ValidationError(u"Please don't shout")

.. _plone.directives.form: http://pypi.python.org/pypi/plone.directives.form
