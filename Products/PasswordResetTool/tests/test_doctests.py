"""
PasswordResetTool doctests
"""

import doctest
import unittest

from Acquisition import aq_base
from Products.CMFPlone.tests.utils import MockMailHost
from Products.MailHost.interfaces import IMailHost
from plone.app import testing
from plone.registry.interfaces import IRegistry
from plone.testing import layered
from transaction import commit
from zope.component import getSiteManager
from zope.component import getUtility

try:
    from Products.CMFPlone.interfaces.controlpanel import IMailSchema, ISiteSchema
    HAS_REGISTRY_MAIL_SETTINGS = True
    # work with plone 4 yet...
except ImportError:
    HAS_REGISTRY_MAIL_SETTINGS = False


OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_ONLY_FIRST_FAILURE)


class MockMailFixture(testing.PloneSandboxLayer):

    defaultBases = (testing.PLONE_FIXTURE, )

    def setUpPloneSite(self, portal):
        portal._original_MailHost = portal.MailHost
        portal.MailHost = mailhost = MockMailHost('MailHost')
        registry = getUtility(IRegistry)
        mail_settings = registry.forInterface(IMailSchema, prefix='plone')
        mail_settings.smtp_host = u'localhost'
        mail_settings.email_from_address = 'john@doe.com'
        sm = getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)
        commit()

    def tearDownPloneSite(self, portal):
        portal.MailHost = portal._original_MailHost
        sm = getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(
            aq_base(portal._original_MailHost),
            provided=IMailHost
        )


class Layer(testing.FunctionalTesting):

    def set_email_from_name(self, name):
        if HAS_REGISTRY_MAIL_SETTINGS:
            registry = getUtility(IRegistry)
            mail_settings = registry.forInterface(IMailSchema, prefix="plone")
            mail_settings.email_from_name = name
        else:
            self['portal'].email_from_name = name

    def set_email_from_address(self, address):
        if HAS_REGISTRY_MAIL_SETTINGS:
            registry = getUtility(IRegistry)
            mail_settings = registry.forInterface(IMailSchema, prefix="plone")
            mail_settings.email_from_address = address
        else:
            self['portal'].email_from_address = address

    def set_portal_title(self, name):
        if HAS_REGISTRY_MAIL_SETTINGS:
            registry = getUtility(IRegistry)
            site_settings = registry.forInterface(ISiteSchema, prefix='plone')
            site_settings.site_title = name
        else:
            self['portal'].title = name

MOCK_MAIL_FIXTURE = MockMailFixture()
MM_FUNCTIONAL_TESTING = Layer(
    bases=(MOCK_MAIL_FIXTURE, ),
    name='PloneTestCase:Functional'
)


def test_suite():
    return unittest.TestSuite((
        layered(
            doctest.DocFileSuite(
                'browser.txt',
                optionflags=OPTIONFLAGS,
                package='Products.PasswordResetTool.tests',
            ),
            layer=MM_FUNCTIONAL_TESTING
        ),
        layered(
            doctest.DocFileSuite(
                'view.txt',
                optionflags=OPTIONFLAGS,
                package='Products.PasswordResetTool.tests',
            ),
            layer=MM_FUNCTIONAL_TESTING))
        )
