from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from zope import schema
from zope.interface import alsoProvides
from zope.container.interfaces import INameChooser
from plone.app.dexterity import MessageFactory as _
from plone.autoform import directives as form
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
import transaction


class IShortName(model.Schema):

    model.fieldset(
        'settings',
        label=_(u"Settings"),
        fields=['id'],
    )

    id = schema.ASCIILine(
        title=_(u'Short name'),
        description=_(u'This name will be displayed in the URL.'),
        required=False,
    )
    form.write_permission(id='cmf.AddPortalContent')

alsoProvides(IShortName, IFormFieldProvider)


class ShortName(object):

    def __init__(self, context):
        self.context = context

    def _get_id(self):
        return self.context.getId()

    def _set_id(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        parent = aq_parent(context)
        if parent is None:
            # Object hasn't been added to graph yet; just set directly
            context.id = value
            return
        new_id = INameChooser(parent).chooseName(value, context)
        if getattr(aq_base(context), 'id', None):
            transaction.savepoint()
            parent.manage_renameObject(context.getId(), new_id)
        else:
            context.id = new_id
    id = property(_get_id, _set_id)
