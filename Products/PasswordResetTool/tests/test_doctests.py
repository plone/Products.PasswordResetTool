"""
PasswordResetTool doctests
"""

import doctest
import unittest
from Products.MailHost.interfaces import IMailHost
from zope.component import getSiteManager
from Acquisition import aq_base

from Products.CMFPlone.tests.utils import MockMailHost
from plone.app import testing
from plone.testing import layered

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

class MockMailFixture(testing.PloneSandboxLayer):

    defaultBases = (testing.PLONE_FIXTURE,)

    def setUpPloneSite(self, portal):
        portal._original_MailHost = self.portal.MailHost
        portal.MailHost = mailhost = MockMailHost('MailHost')
        mailhost.smtp_host = 'localhost'
        sm = getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)
        portal.email_from_address = 'test@example.com'

#    def beforeTearDown(self):
#        self.portal.MailHost = self.portal._original_MailHost
#        sm = getSiteManager(context=self.portal)
#        sm.unregisterUtility(provided=IMailHost)
#        sm.registerUtility(aq_base(self.portal._original_MailHost), provided=IMailHost)

MOCK_MAIL_FIXTURE = MockMailFixture()

def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite('browser.txt',
                               optionflags=OPTIONFLAGS,
                               package='Products.PasswordResetTool.tests',
                               test_class=MockMailHostTestCase),
        doctest.DocFileSuite('view.txt',
                               optionflags=OPTIONFLAGS,
                               package='Products.PasswordResetTool.tests',
                               test_class=MockMailHostTestCase),
        ))
