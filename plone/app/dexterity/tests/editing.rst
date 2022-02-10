Through-the-web content type editing
====================================

This package, plone.app.dexterity, provides the UI for creating and editing
Dexterity content types through the Plone control panel.

To demonstrate this, we'll need a logged in test browser::

  >>> from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, TEST_USER_PASSWORD, setRoles
  >>> portal = layer['portal']
  >>> setRoles(portal, TEST_USER_ID, ['Manager'])
  >>> import transaction; transaction.commit()
  >>> from plone.testing.z2 import Browser
  >>> browser = Browser(layer['app'])
  >>> browser.handleErrors = False
  >>> browser.addHeader('Authorization', 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD,))


Dexterity Types Configlet
-------------------------

Once the 'Dexterity Content Configlet' product is installed, site managers
can navigate to the configlet via the control panel::

  >>> browser.open('http://nohost/plone')
  >>> browser.getLink('Site Setup').click()
  >>> browser.getLink('Content Types').click()
  >>> browser.url
  'http://nohost/plone/@@dexterity-types'
  >>> 'Content Types' in browser.contents
  True

Adding a content type
---------------------

Let's add a 'Plonista' content type to keep track of members of the Plone
community::

  >>> browser.getLink('Add New Content Type').click()
  >>> browser.getControl('Type Name').value = 'Plonista'
  >>> browser.getControl('Short Name').value = 'plonista'
  >>> browser.getControl('Description').value = 'Represents a Plonista.'
  >>> browser.getControl('Add').click()
  >>> browser.url
  'http://nohost/plone/dexterity-types/plonista/@@fields'

Now we should also have a 'plonista' FTI in portal_types::

  >>> 'plonista' in portal.portal_types
  True

The new type should have the dublin core behavior assigned by default::

  >>> plonista = portal.portal_types.plonista
  >>> 'plone.dublincore' in plonista.behaviors
  True
  >>> 'file-earmark-text' in plonista.getIconExprObject().text
  True

The listing needs to not break if a type description was stored encoded::

  >>> plonista.description = '\xc3\xbc'
  >>> transaction.commit()
  >>> browser.open('http://nohost/plone/dexterity-types')
  >>> '\xc3\xbc' in browser.contents
  True

The listing should also feature a CSS class for display in the listing
using the short name. Add a new content type to ensure the short name
is present on the page::

  >>> browser.open('http://nohost/plone/dexterity-types')
  >>> browser.getLink('Add New Content Type').click()
  >>> browser.getControl('Type Name').value = 'Plonista Content'
  >>> browser.getControl('Short Name').value = 'plonista-content-short-name'
  >>> browser.getControl('Add').click()
  >>> browser.url
  'http://nohost/plone/dexterity-types/plonista-content-short-name/@@fields'

  >>> browser.open('http://nohost/plone/dexterity-types')
  >>> 'class="contenttype-plonista-content-short-name"' in browser.contents
  True


Adding an instance of the new type
----------------------------------

Now a 'Plonista' can be created within the site::

  >>> browser.open('http://nohost/plone')
  >>> browser.getLink('Plonista').click()
  >>> browser.getControl('Title').value = 'Martin Aspeli'
  >>> browser.getControl('Save').click()
  >>> browser.url
  'http://nohost/plone/martin-aspeli/view'


Editing a content type
----------------------

Editing schemata is handled by the plone.schemaeditor package and is tested
there.  However, let's at least make sure that we can navigate to the
schema for the 'plonista' type we just created::

  >>> browser.open('http://nohost/plone/@@dexterity-types')
  >>> browser.getLink('Plonista').click()
  >>> browser.getLink(url='/@@fields').click()
  >>> schemaeditor_url = browser.url
  >>> schemaeditor_url
  'http://nohost/plone/dexterity-types/plonista/@@fields'

Demonstrate that all the registered field types can be added edited
and saved::

  >>> from zope import component
  >>> from plone.i18n.normalizer.interfaces import IIDNormalizer
  >>> from plone.schemaeditor import interfaces
  >>> normalizer = component.getUtility(IIDNormalizer)
  >>> import time
  >>> for name, factory in sorted(component.getUtilitiesFor(
  ...     interfaces.IFieldFactory)):
  ...     if hasattr(factory, 'protected') and factory.protected(None):
  ...         continue
  ...     browser.open(schemaeditor_url)
  ...     # If two changes happen in the same second, the schema lookup will find an old schema,
  ...     # so we sleep till the next second.
  ...     now = time.time()
  ...     time.sleep(int(now) + 1 - now)
  ...     browser.getLink('Add new field').click()
  ...     browser.getControl('Title').value = name
  ...     field_id = normalizer.normalize(name).replace('-', '_')
  ...     browser.getControl('Short Name').value = field_id
  ...     browser.getControl('Field type').getControl(
  ...         value=factory.title).selected = True
  ...     browser.getControl('Add').click()
  ...     schema = plonista.lookupSchema()
  ...     assert browser.url == "http://nohost/plone/dexterity-types/plonista/@@add-field", (
  ...         "Couldn't successfully add %r" % name)
  ...     assert field_id in schema, '%r not in %r' % (
  ...         field_id, schema)
  ...     assert factory.fieldcls._type is None or isinstance(
  ...         schema[field_id], factory.fieldcls
  ...         ), '%r is not an instance of %r' % (
  ...             schema[field_id], factory.fieldcls)
  ...     browser.open(schemaeditor_url)
  ...     browser.getLink(url=field_id).click()
  ...     browser.getControl('Save').click()


Editing the XML model directly
------------------------------

Much of what the XML model editor does is happening in JavaScript, but we can
still test the Zope side.

Get some tools::

  >>> try:
  ...     from html import escape
  ... except ImportError:
  ...     from cgi import escape
  >>> from six.moves.urllib.parse import quote_plus

We should be able to navigate to the modeleditor view by clicking a
button on the field list form::

  >>> browser.open('http://nohost/plone/dexterity-types/plonista/@@fields')
  >>> browser.getControl('Edit XML Field Model').click()
  >>> browser.url
  'http://nohost/plone/dexterity-types/plonista/@@modeleditor'

We should be telling the browser to load our keys resources::

  >>> browser.contents
  '...<script...src="http://nohost/plone/++plone++static/components/ace-builds/src/ace.js"...'

  >>> browser.contents
  '...<script...src="http://nohost/plone/++resource++plone.app.dexterity.modeleditor.js"...'

Both of those should be available::

  browser.open('http://nohost/plone/++plone++static/components/ace-builds/src/ace.js')
  browser.open('http://nohost/plone/++resource++plone.app.dexterity.modeleditor.js')

Return to our view and find the XML model source in a div, ready for the Ace editor::

  >>> browser.open('http://nohost/plone/dexterity-types/plonista/@@modeleditor')
  >>> '<div id="modelEditor">' in browser.contents
  True

  >>> '&lt;schema&gt;' in browser.contents
  True

  >>> model_source = portal.portal_types.plonista.model_source
  >>> escaped_model_source = escape(model_source, quote=False)
  >>> escaped_model_source in browser.contents
  True

There should be an authenticator in the `save` form::

  >>> authenticator = browser.getControl(name="_authenticator", index=0).value

Save is via AJAX. Let's check the save view's functionality.

First, prove this won't work without an authenticator

  >>> browser.open('http://nohost/plone/dexterity-types/plonista/@@model-edit-save?source=something')
  Traceback (most recent call last):
  ...
  AccessControl.unauthorized.Unauthorized: ...

Check rejection of bad XML "something"::

  >>> browser.open('http://nohost/plone/dexterity-types/plonista/@@model-edit-save?source=something&_authenticator=%s' % authenticator)
  >>> import json
  >>> result = json.loads(browser.contents)
  >>> u"XMLSyntaxError: Start tag expected" in result['message']
  True

We should refuse source that doesn't have `model` for the root tag::

  >>> bad_source = model_source.replace('model', 'mode')
  >>> browser.open('http://nohost/plone/dexterity-types/plonista/@@model-edit-save?source=%s&_authenticator=%s' % (quote_plus(bad_source), authenticator))
  >>> from pprint import pprint
  >>> result = json.loads(browser.contents)
  >>> u"Error: root tag must be 'model'" in result['message']
  True

Likewise, only `schema` tags are allowed inside the model::

  >>> bad_source = model_source.replace('schema>', 'scheme>')
  >>> browser.open('http://nohost/plone/dexterity-types/plonista/@@model-edit-save?source=%s&_authenticator=%s' % (quote_plus(bad_source), authenticator))
  >>> result = json.loads(browser.contents)
  >>> u"Error: all model elements must be 'schema'" in result['message']
  True

Should work with real XML

::

  >>> browser.open('http://nohost/plone/dexterity-types/plonista/@@model-edit-save?source=%s&_authenticator=%s' % (quote_plus(model_source), authenticator))
  >>> pprint(json.loads(browser.contents))
  {'message': 'Saved', 'success': True}

That response should have a JSON content type::

  >>> browser.headers['content-type']
  'application/json'

We should be providing a link back to the fields editor::

  >>> browser.open('http://nohost/plone/dexterity-types/plonista/@@modeleditor')
  >>> link = browser.getLink('Back to the schema editor')
  >>> link.click()
  >>> browser.url
  'http://nohost/plone/dexterity-types/plonista/@@fields'


Enabling a behavior
-------------------

For each content type, a number of behaviors may be enabled. Let's disable a
behavior for 'plonista' and make sure that the change is reflected on the
FTI::

  >>> browser.getLink('Behaviors').click()
  >>> browser.url
  'http://nohost/plone/dexterity-types/plonista/@@behaviors'

  >>> browser.getControl(name='form.widgets.plone.dublincore:list').value = []
  >>> browser.getControl('Save').click()
  >>> 'plone.namefromtitle' in portal.portal_types.plonista.behaviors
  True

Let's enable one that is not enable and make sure that
the change is reflected on the FTI::

  >>> sorted(portal.portal_types.plonista.behaviors)
  ['plone.namefromtitle']
  >>> 'plone.versioning' in portal.portal_types.plonista.behaviors
  False
  >>> browser.getControl(name='form.widgets.plone.versioning:list').value = "selected"
  >>> browser.getControl('Save').click()
  >>> sorted(portal.portal_types.plonista.behaviors)
  ['plone.namefromtitle', 'plone.versioning']

Viewing a non-editable schema
-----------------------------

If a type's schema is not stored as XML in its FTI's schema property, it cannot
currently be edited through the web.  However, the fields of the schema can at
least be listed.

::

  >>> from zope.interface import Interface
  >>> from zope import schema
  >>> import plone.app.dexterity.tests
  >>> class IFilesystemSchema(Interface):
  ...     irc_nick = schema.TextLine(title=u'IRC Nickname')
  >>> plone.app.dexterity.tests.IFilesystemSchema = IFilesystemSchema
  >>> plonista.schema = 'plone.app.dexterity.tests.IFilesystemSchema'
  >>> transaction.commit()
  >>> browser.open('http://nohost/plone/dexterity-types/plonista/@@fields')
  >>> 'crud-edit.form.buttons.delete' in browser.contents
  False
  >>> 'IRC Nickname' in browser.contents
  True

We should not be offering the 'Edit XML' button::

  >>> 'Edit XML Field Model' in browser.contents
  False


Cloning a content type
----------------------

A content type can be cloned::

  >>> browser.open('http://nohost/plone/dexterity-types')
  >>> browser.getControl(name='crud-edit.plonista.widgets.select:list').controls[0].selected = True
  >>> browser.getControl('Clone').click()
  >>> browser.url
  'http://nohost/plone/dexterity-types/plonista/@@clone'
  >>> browser.getControl('Type Name').value = 'Plonista2'
  >>> browser.getControl('Short Name').value = 'plonista2'
  >>> browser.getControl('Add').click()
  >>> browser.url
  'http://nohost/plone/dexterity-types'
  >>> 'plonista2' in browser.contents
  True
  >>> 'plonista2' in portal.portal_types
  True

The new content type has its own factory.

  >>> portal.portal_types.plonista2.factory
  'plonista2'

Validation to prevent duplicate content types
---------------------------------------------

A new content type cannot be created if its name is the same as an existing
content type::

  >>> browser.getLink('Add New Content Type').click()
  >>> browser.getControl('Type Name').value = 'foobar'
  >>> browser.getControl('Short Name').value = 'plonista'
  >>> browser.getControl('Add').click()
  >>> browser.url
  'http://nohost/plone/dexterity-types/@@add-type'
  >>> "There is already a content type named 'plonista'" in browser.contents
  True

To avoid confusion, the title must also be unique::

  >>> browser.open('http://nohost/plone/dexterity-types')
  >>> browser.getLink('Add New Content Type').click()
  >>> browser.getControl('Type Name').value = 'Plonista'
  >>> browser.getControl('Short Name').value = 'foobar'
  >>> browser.getControl('Add').click()
  >>> browser.url
  'http://nohost/plone/dexterity-types/@@add-type'
  >>> "There is already a content type named 'Plonista'" in browser.contents
  True

Similar checks are performed when cloning::

  >>> browser.open('http://nohost/plone/dexterity-types')
  >>> browser.getControl(name='crud-edit.plonista.widgets.select:list').controls[0].selected = True
  >>> browser.getControl('Clone').click()
  >>> browser.getControl('Type Name').value = 'foobar'
  >>> browser.getControl('Short Name').value = 'plonista'
  >>> browser.getControl('Add').click()
  >>> browser.url
  'http://nohost/plone/dexterity-types/plonista/@@clone'
  >>> "There is already a content type named 'plonista'" in browser.contents
  True

  >>> browser.open('http://nohost/plone/dexterity-types')
  >>> browser.getControl(name='crud-edit.plonista.widgets.select:list').controls[0].selected = True
  >>> browser.getControl('Clone').click()
  >>> browser.getControl('Type Name').value = 'Plonista'
  >>> browser.getControl('Short Name').value = 'foobar'
  >>> browser.getControl('Add').click()
  >>> browser.url
  'http://nohost/plone/dexterity-types/plonista/@@clone'
  >>> "There is already a content type named 'Plonista'" in browser.contents
  True


Adding a container
------------------

We can create a content type that is a container for other content::

  >>> browser.open('http://nohost/plone/@@dexterity-types')
  >>> browser.getLink('Add New Content Type').click()
  >>> browser.getControl('Type Name').value = 'Plonista Folder'
  >>> browser.getControl('Short Name').value = 'plonista-folder'
  >>> browser.getControl('Add').click()
  >>> browser.url
  'http://nohost/plone/dexterity-types/plonista-folder/@@fields'

Now we should have a 'plonista-folder' FTI in portal_types, and it should be
using the Container base class::

  >>> 'plonista-folder' in portal.portal_types
  True
  >>> pf = getattr(portal.portal_types, 'plonista-folder')
  >>> pf.klass
  'plone.dexterity.content.Container'
  >>> 'file-earmark-text' in pf.getIconExprObject().text
  True

We can configure the plonista-folder to allow contained content types::

  >>> browser.open('http://nohost/plone/dexterity-types/plonista-folder')
  >>> browser.getControl('All content types').click()
  >>> browser.getControl('Apply').click()

If we add a plonista-folder, we can then add other content items inside it::

  >>> browser.open('http://nohost/plone')
  >>> browser.getLink('Plonista Folder').click()
  >>> browser.getControl('Title').value = 'Plonista Folder 1'
  >>> browser.getControl('Save').click()
  >>> browser.url
  'http://nohost/plone/plonista-folder-1/view'
  >>> browser.getLink(url='Document').click()
  >>> browser.getControl('Title').value = 'Introduction'
  >>> browser.getControl('Save').click()
  >>> browser.url
  'http://nohost/plone/plonista-folder-1/introduction'

We can control which content types are allowed to be added into the
container::

  >>> browser.open('http://nohost/plone/dexterity-types/plonista-folder')
  >>> browser.getControl('Some content types', index=0).click()
  >>> select = browser.getControl(name="form.widgets.allowed_content_types:list")
  >>> select
  <ListControl name='form.widgets.allowed_content_types:list' type='select'>

  >>> select.getControl('Page').selected = True
  >>> browser.getControl('Apply').click()
  >>> 'Data successfully updated' in browser.contents
  True

Now only the allowed types may be added::

  >>> browser.open('http://nohost/plone/plonista-folder-1')

  >>> browser.getLink(url='Folder')
  Traceback (most recent call last):
  ...
  zope.testbrowser.browser.LinkNotFoundError...

  >>> browser.getLink(url='Document').click()
  >>> browser.getControl('Title').value = 'Foo Plonista Page'
  >>> browser.getControl('Save').click()


Removing a content type
-----------------------

We can also delete a content type via the configlet::

  >>> browser.open('http://nohost/plone/@@dexterity-types')
  >>> browser.getControl(name='crud-edit.plonista.widgets.select:list').controls[0].selected = True
  >>> browser.getControl('Delete').click()

Now the FTI for the type should no longer be present in portal_types::

  >>> 'plonista' in portal.portal_types
  False

We should still be able to view a container that contains an instance of the
removed type::

  >>> browser.open('http://nohost/plone/folder_contents')

But actually trying to view the type will now cause an error, as expected::

  >>> browser.open('http://nohost/plone/martin-aspeli/view')
  Traceback (most recent call last):
  ...
  zope.interface.interfaces.ComponentLookupError...


Dexterity Types Export
----------------------

Try out the types export button. We should be able to select our types from
their checkboxes, push the export types button, and get a download for a
zip archive containing files ready to drop into our profile::

    >>> browser.open('http://nohost/plone/dexterity-types')
    >>> browser.getControl(name='crud-edit.plonista2.widgets.select:list').controls[0].selected = True
    >>> browser.getControl(name='crud-edit.plonista-folder.widgets.select:list').controls[0].selected = True
    >>> browser.getControl('Export Type Profiles').click()
    >>> browser.url
    'http://nohost/plone/dexterity-types/@@types-export?selected=plonista2%2Cplonista-folder'

    >>> browser.headers['content-type']
    'application/zip'

    >>> browser.headers['content-disposition']
    'attachment; filename=dexterity_export-....zip'

    >>> import zipfile
    >>> import six
    >>> fd = six.BytesIO(browser.contents)
    >>> archive = zipfile.ZipFile(fd, mode='r')
    >>> archive.namelist()
    ['types.xml', 'types/plonista2.xml', 'types/plonista-folder.xml']

    >>> types_xml = archive.read('types.xml')
    >>> b'<object name="plonista2" meta_type="Dexterity FTI"/>' in types_xml
    True
    >>> b'<object name="plonista-folder" meta_type="Dexterity FTI"/>' in types_xml
    True

Try out the models export button. We should be able to select our types from
their checkboxes, push the export models button, and get a download for a
zip archive containing supermodel xml files::

    >>> browser.open('http://nohost/plone/dexterity-types')
    >>> browser.getControl(name='crud-edit.plonista2.widgets.select:list').controls[0].selected = True
    >>> browser.getControl(name='crud-edit.plonista-folder.widgets.select:list').controls[0].selected = True
    >>> browser.getControl('Export Schema Models').click()
    >>> browser.url
    'http://nohost/plone/dexterity-types/@@models-export?selected=plonista2%2Cplonista-folder'

    >>> browser.headers['content-type']
    'application/zip'

    >>> browser.headers['content-disposition']
    'attachment; filename=dexterity_models-....zip'

    >>> import zipfile
    >>> import six
    >>> fd = six.BytesIO(browser.contents)
    >>> archive = zipfile.ZipFile(fd, mode='r')
    >>> archive.namelist()
    ['models/plonista2.xml', 'models/plonista-folder.xml']

    >>> from Products.CMFPlone.utils import safe_unicode
    >>> print(safe_unicode(archive.read('models/plonista2.xml')))
    <model...xmlns="http://namespaces.plone.org/supermodel/schema"...>
      <schema>
      ...
      </schema>
    </model>

If there's only one item selected, we get a single XML file rather than a zip
file::

    >>> browser.open('http://nohost/plone/dexterity-types')
    >>> browser.getControl(name='crud-edit.plonista2.widgets.select:list').controls[0].selected = True
    >>> browser.getControl('Export Schema Models').click()
    >>> browser.url
    'http://nohost/plone/dexterity-types/@@models-export?selected=plonista2'

    >>> browser.headers['content-type']
    'application/xml'

    >>> browser.headers['content-disposition']
    'attachment; filename=plonista2.xml'

    >>> print(safe_unicode(browser.contents))
    <model...xmlns="http://namespaces.plone.org/supermodel/schema"...>
      <schema>
      ...
      </schema>
    </model>
