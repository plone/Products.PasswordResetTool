"""
PasswordResetTool doctests
"""

import doctest
import unittest
from Testing.ZopeTestCase import FunctionalDocFileSuite
from Products.PloneTestCase import PloneTestCase

PloneTestCase.installProduct('PlacelessTranslationService')
PloneTestCase.installProduct('PasswordResetTool')
PloneTestCase.setupPloneSite(products=['PasswordResetTool'])

from Products.PasswordResetTool.tests import utils


class MockMailHostTestCase(PloneTestCase.FunctionalTestCase):

    def afterSetUp(self):
        self.portal._original_MailHost = self.portal.MailHost
        self.portal.MailHost = utils.MockMailHost('MailHost')

    def beforeTearDown(self):
        self.portal.MailHost = self.portal._original_MailHost


def test_suite():
    return unittest.TestSuite((
        FunctionalDocFileSuite('browser.txt',
                               optionflags = doctest.REPORT_ONLY_FIRST_FAILURE,
                               package='Products.PasswordResetTool.tests',
                               test_class=MockMailHostTestCase),
        ))
