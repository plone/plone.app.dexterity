from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from plone.z3cform.interfaces import IWrappedForm
from z3c.form import form

from plone.app.dexterity import MessageFactory as _


class TypeOverviewForm(form.EditForm):
    implements(IWrappedForm)
    
    layout = ViewPageTemplateFile('tabbed_forms.pt')
    label = _(u'Overview')

    def __call__(self):
        self.update()

        # Don't render anything if we are doing a redirect
        if self.request.response.getStatus() in (300, 301, 302, 303, 304, 305, 307,):
            return u''

        return self.layout()

    @property
    def tabs(self):
        return (
            (_('Overview'), None),
            (_('Fields'), '@@fields'),
            (_('Behaviors'), '@@behaviors'),
            )
