from z3c.form import form, field
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.dottedname.resolve import resolve as resolveDottedName
from Products.CMFCore.interfaces import IFolderish
from plone.app.dexterity.browser.layout import TypeFormLayout
from plone.app.dexterity.interfaces import ITypeSettings
from plone.app.dexterity import MessageFactory as _


class TypeOverviewForm(form.EditForm):
    enableCSRFProtection = True
    template = ViewPageTemplateFile('overview.pt')

    @property
    def fields(self):
        # if this type's class is not a container,
        # remove the field for filtering contained content types
        klass = resolveDottedName(self.context.fti.klass)
        fields = field.Fields(ITypeSettings)
        filtered = fields.select('title', 'description',
                                 'allowed_content_types',
                                 'filter_content_types')
        if not IFolderish.implementedBy(klass):
            del filtered['filter_content_types']
        return filtered

    def getContent(self):
        return self.context.fti


class TypeOverviewPage(TypeFormLayout):
    form = TypeOverviewForm
    label = _(u'Overview')
