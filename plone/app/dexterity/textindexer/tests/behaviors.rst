Test everything with behaviors::

    >>> from Products.CMFCore.utils import getToolByName
    >>> from plone.app.testing import TEST_USER_NAME
    >>> from plone.app.testing import login
    >>> from plone.dexterity.fti import DexterityFTI
    >>> from plone.dexterity.utils import createContentInContainer

    >>> portal = layer['portal']
    >>> login(portal, TEST_USER_NAME)


Helpers::

    >>> def obj2brain(obj):
    ...     catalog = getToolByName(obj, 'portal_catalog')
    ...     query = {'path': {'query': '/'.join(obj.getPhysicalPath()),
    ...                       'depth': 0}}
    ...     brains = catalog(query)
    ...     if len(brains) == 0:
    ...         raise Exception('Not in catalog: %s' % obj)
    ...     else:
    ...         return brains[0]

    >>> def getSearchableText(obj):
    ...     brain = obj2brain(obj)
    ...     catalog = getToolByName(obj, 'portal_catalog')
    ...     data = catalog.getIndexDataForRID(brain.getRID())
    ...     return data['SearchableText']


First test it with a simple behavior::

    >>> from plone.app.dexterity.textindexer.tests.behaviors import ISimpleBehavior
    >>> fti = DexterityFTI('SimpleFTI')
    >>> fti.behaviors = (
    ...     'plone.textindexer',
    ...     'plone.app.dexterity.textindexer.tests.behaviors.ISimpleBehavior',
    ... )
    >>> portal.portal_types._setObject('SimpleFTI', fti)
    'SimpleFTI'
    >>> schema = fti.lookupSchema()

    >>> obj1 = createContentInContainer(portal, 'SimpleFTI',
    ...                                 checkContstraints=False,
    ...                                 foo='foox',
    ...                                 bar='barx')
    >>> obj1
    <Item at /plone/simplefti>
    >>> getSearchableText(obj1)
    ['foox']


Test, if the value getter works also, when the request has stored another value for this field.

::

    >>> schema = fti.lookupSchema()

    >>> portal.REQUEST.form['foo'] = 'blubb'
    >>> obj1 = createContentInContainer(portal, 'SimpleFTI',
    ...                                 checkContstraints=False,
    ...                                 foo='foox',
    ...                                 bar='barx')
    >>> obj1
    <Item at /plone/simplefti-1>
    >>> getSearchableText(obj1)
    ['foox']


Does a list work?

::

    >>> from plone.app.dexterity.textindexer.tests.behaviors import IListBehavior
    >>> fti = DexterityFTI('ListFTI')
    >>> fti.behaviors = (
    ...     'plone.textindexer',
    ...     'plone.app.dexterity.textindexer.tests.behaviors.IListBehavior',
    ... )
    >>> portal.portal_types._setObject('ListFTI', fti)
    'ListFTI'
    >>> schema = fti.lookupSchema()

    >>> obj2 = createContentInContainer(portal, 'ListFTI',
    ...                                 checkContstraints=False,
    ...                                 list_field=['hello', u'little', 'world'])

    >>> obj2
    <Item at /plone/listfti>
    >>> getSearchableText(obj2)
    ['hello', 'little', 'world']


Do ints work?

::

    >>> from plone.app.dexterity.textindexer.tests.behaviors import IIntBehavior
    >>> fti = DexterityFTI('IntFTI')
    >>> fti.behaviors = (
    ...     'plone.textindexer',
    ...     'plone.app.dexterity.textindexer.tests.behaviors.IIntBehavior',
    ... )
    >>> portal.portal_types._setObject('IntFTI', fti)
    'IntFTI'
    >>> schema = fti.lookupSchema()

    >>> obj3 = createContentInContainer(portal, 'IntFTI',
    ...                                 checkContstraints=False,
    ...                                 int_field=57)

    >>> obj3
    <Item at /plone/intfti>

In Plone 4.3 int-values are stored as unicodes.
Since our test should work also for old Plones, we convert everything
to string here::

    >>> list(map(str, getSearchableText(obj3)))
    ['57']


Do rich-text fields work?

    >>> from plone.app.dexterity.textindexer.tests.behaviors import IRichTextBehavior
    >>> from plone.app.textfield.value import RichTextValue
    >>> fti = DexterityFTI('RichTextFTI')
    >>> fti.behaviors = (
    ...     'plone.textindexer',
    ...     'plone.app.dexterity.textindexer.tests.behaviors.IRichTextBehavior',
    ... )
    >>> portal.portal_types._setObject('RichTextFTI', fti)
    'RichTextFTI'
    >>> schema = fti.lookupSchema()

    >>> rtv = RichTextValue(
    ...     raw='<p>In for an <em>inch</em>, in for a <strong>pound.</strong></p>',
    ...     mimeType='text/html',
    ...     outputMimeType='text/html',
    ...     encoding='utf-8',
    ... )
    >>> obj4 = createContentInContainer(
    ...    portal,
    ...    'RichTextFTI',
    ...    checkContstraints=False,
    ...    richtext_field=rtv,
    ... )

    >>> obj4
    <Item at /plone/richtextfti>

    >>> getSearchableText(obj4)
    ['in', 'for', 'an', 'inch', 'in', 'for', 'a', 'pound']


Values are not duplicated in SearchableText when field comes from real interface

    >>> from plone.app.dexterity.textindexer.tests.behaviors import ISimpleBehavior
    >>> fti = DexterityFTI('SimpleFTI2')
    >>> fti.behaviors = (
    ...     'plone.textindexer',
    ...     'plone.app.dexterity.textindexer.tests.behaviors.ISimpleBehavior',
    ... )
    >>> fti.model_source = '<model xmlns="http://namespaces.plone.org/supermodel/schema" xmlns:i18n="http://xml.zope.org/namespaces/i18n" i18n:domain="plone"><schema based-on="plone.app.dexterity.textindexer.tests.test_behaviors.ITestingSchema"></schema></model>'
    >>> portal.portal_types._setObject('SimpleFTI2', fti)
    'SimpleFTI2'
    >>> schema = fti.lookupSchema()

    >>> obj1 = createContentInContainer(portal, 'SimpleFTI2',
    ...                                 checkContstraints=False,
    ...                                 foo='foox',
    ...                                 bar='barx',
    ...                                 testing_field='bla')
    >>> obj1
    <Item at /plone/simplefti2>
    >>> getSearchableText(obj1)
    ['bla', 'foox']


Do empty rich-text fields work?

    >>> from plone.app.dexterity.textindexer.tests.behaviors import IEmptyRichTextBehavior
    >>> fti = DexterityFTI('EmptyRichTextFTI')
    >>> fti.behaviors = (
    ...     'plone.textindexer',
    ...     'plone.app.dexterity.textindexer.tests.behaviors.IEmptyRichTextBehavior',
    ... )
    >>> portal.portal_types._setObject('EmptyRichTextFTI', fti)
    'EmptyRichTextFTI'
    >>> schema = fti.lookupSchema()

    >>> obj_empty_rich_text = createContentInContainer(
    ...    portal,
    ...    'EmptyRichTextFTI',
    ...    checkContstraints=False,
    ...    foo='Hello World',
    ... )

    >>> obj_empty_rich_text
    <Item at /plone/emptyrichtextfti>

    >>> getSearchableText(obj_empty_rich_text)
    ['hello', 'world']


Do tuple fields work?

    >>> from plone.app.dexterity.textindexer.tests.behaviors import IRichTextBehavior
    >>> fti = DexterityFTI('TupleFTI')
    >>> fti.behaviors = (
    ...     'plone.textindexer',
    ...     'plone.app.dexterity.textindexer.tests.behaviors.ITupleBehavior',
    ... )
    >>> portal.portal_types._setObject('TupleFTI', fti)
    'TupleFTI'
    >>> schema = fti.lookupSchema()
    >>> obj5 = createContentInContainer(
    ...    portal,
    ...    'TupleFTI',
    ...    checkContstraints=False,
    ...    tuple_field=('My', 'kingdom', 'for', 'a', 'horse'),
    ... )

    >>> obj5
    <Item at /plone/tuplefti>

    >>> getSearchableText(obj5)
    ['my', 'kingdom', 'for', 'a', 'horse']


Do tuple fields with choice values work?

    >>> from plone.app.dexterity.textindexer.tests.behaviors import IRichTextBehavior
    >>> fti = DexterityFTI('TupleChoiceFTI')
    >>> fti.behaviors = (
    ...     'plone.textindexer',
    ...     'plone.app.dexterity.textindexer.tests.behaviors.ITupleChoiceBehavior',
    ... )
    >>> portal.portal_types._setObject('TupleChoiceFTI', fti)
    'TupleChoiceFTI'
    >>> schema = fti.lookupSchema()
    >>> obj6 = createContentInContainer(
    ...    portal,
    ...    'TupleChoiceFTI',
    ...    checkContstraints=False,
    ...    tuple_choice_field=('Knights', 'ni'),
    ... )

    >>> obj6
    <Item at /plone/tuplechoicefti>

    >>> getSearchableText(obj6)
    ['knights', 'ni']


When a schema marks a field as searchable which does not exist it should:

- not break indexing other fields
- log an error

::

    >>> from plone.app.dexterity.textindexer.tests.behaviors import IMissingFieldBehavior
    >>> fti = DexterityFTI('MissingFieldFTI')
    >>> fti.behaviors = (
    ...     'plone.textindexer',
    ...     'plone.app.dexterity.textindexer.tests.behaviors.IMissingFieldBehavior',
    ... )
    >>> portal.portal_types._setObject('MissingFieldFTI', fti)
    'MissingFieldFTI'
    >>> schema = fti.lookupSchema()

    >>> obj = createContentInContainer(portal, 'MissingFieldFTI',
    ...                                checkContstraints=False,
    ...                                foo='foo value')
    >>> obj
    <Item at /plone/missingfieldfti>
    >>> getSearchableText(obj)
    ['foo', 'value']

    >>> 'IMissingFieldBehavior has no field "bar"' in layer['read_log']()
    True


Test, if a subclassed schema also inherits the searchable configuration of
it's superclass::

    >>> from plone.app.dexterity.textindexer.tests.behaviors import IInheritedBehavior
    >>> fti = DexterityFTI('InheritedFTI')
    >>> fti.behaviors = (
    ...     'plone.textindexer',
    ...     'plone.app.dexterity.textindexer.tests.behaviors.IInheritedBehavior',
    ... )
    >>> portal.portal_types._setObject('InheritedFTI', fti)
    'InheritedFTI'
    >>> schema = fti.lookupSchema()

    >>> obj1 = createContentInContainer(portal, 'InheritedFTI',
    ...                                 checkContstraints=False,
    ...                                 foo='foo value',
    ...                                 bar='bar value')
    >>> obj1
    <Item at /plone/inheritedfti>
    >>> getSearchableText(obj1)
    ['foo', 'value']
