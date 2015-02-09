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
from transaction import commit

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_ONLY_FIRST_FAILURE)

class MockMailFixture(testing.PloneSandboxLayer):

    defaultBases = (testing.PLONE_FIXTURE,)

    def setUpPloneSite(self, portal):
        portal._original_MailHost = portal.MailHost
        portal.MailHost = mailhost = MockMailHost('MailHost')
        mailhost.smtp_host = 'localhost'
        sm = getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(mailhost, provided=IMailHost)
        portal.email_from_address = 'test@example.com'
        commit()

    def tearDownPloneSite(self, portal):
        portal.MailHost = portal._original_MailHost
        sm = getSiteManager(context=portal)
        sm.unregisterUtility(provided=IMailHost)
        sm.registerUtility(aq_base(portal._original_MailHost), provided=IMailHost)


MOCK_MAIL_FIXTURE = MockMailFixture()
MM_FUNCTIONAL_TESTING = testing.FunctionalTesting(
            bases=(MOCK_MAIL_FIXTURE,), name='PloneTestCase:Functional')


def test_suite():
    return unittest.TestSuite((
        layered(doctest.DocFileSuite('browser.txt',
            optionflags=OPTIONFLAGS,
            package='Products.PasswordResetTool.tests',),
            layer=MM_FUNCTIONAL_TESTING),
        layered(doctest.DocFileSuite('view.txt',
            optionflags=OPTIONFLAGS,
            package='Products.PasswordResetTool.tests',),
            layer=MM_FUNCTIONAL_TESTING)))
