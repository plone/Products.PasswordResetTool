from zope.interface import implementer
from zope.component import getMultiAdapter
from Products.Five import BrowserView
from plone.memoize import view
from Products.CMFPlone.utils import safe_unicode
from zope.i18n import translate

from Products.PasswordResetTool.interfaces import IPasswordResetToolView
from Products.PasswordResetTool import passwordresetMessageFactory as _
from email.Header import Header

from plone.registry.interfaces import IRegistry
from zope.component import getUtility
try:
    from Products.CMFPlone.interfaces.controlpanel import IMailSchema
    HAS_REGISTRY_MAIL_SETTINGS = True
    # work with plone 4 yet...
except ImportError:
    HAS_REGISTRY_MAIL_SETTINGS = False


@implementer(IPasswordResetToolView)
class PasswordResetToolView(BrowserView):

    @view.memoize_contextless
    def portal_state(self):
        """ returns
            http://dev.plone.org/plone/browser/plone.app.layout/trunk/plone/app/layout/globals/portal.py
        """
        return getMultiAdapter((self.context, self.request), name=u"plone_portal_state")

    def encode_mail_header(self, text):
        """ Encodes text into correctly encoded email header """
        return Header(safe_unicode(text), 'utf-8')

    def encoded_mail_sender(self):
        """ returns encoded version of Portal name <portal_email> """
        if HAS_REGISTRY_MAIL_SETTINGS:
            registry = getUtility(IRegistry)
            mail_settings = registry.forInterface(IMailSchema, prefix="plone")
            from_ = mail_settings.email_from_name
            mail = mail_settings.email_from_address
        else:
            portal = self.portal_state().portal()
            from_ = portal.getProperty('email_from_name')
            mail = portal.getProperty('email_from_address')
        return '"%s" <%s>' % (self.encode_mail_header(from_), mail)

    def registered_notify_subject(self):
        portal_name = self.portal_state().portal_title()
        return translate(_(u"mailtemplate_user_account_info",
                           default=u"User Account Information for ${portal_name}",
                           mapping={'portal_name': safe_unicode(portal_name)}),
                           context=self.request)

    def mail_password_subject(self):
        return translate(_(u"mailtemplate_subject_resetpasswordrequest",
                           default=u"Password reset request"),
                           context=self.request)
