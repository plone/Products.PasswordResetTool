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

        # XXX see utils/monkey.py
        from Products.PasswordResetTool.tests.utils import monkey
        monkey.monkeyMechanize()

    def beforeTearDown(self):
        self.portal.MailHost = self.portal._original_MailHost

        from Products.PasswordResetTool.tests.utils import monkey
        monkey.unmonkeyMechanize()


def test_suite():
    return unittest.TestSuite((
        FunctionalDocFileSuite('browser.txt',
                               optionflags = doctest.REPORT_ONLY_FIRST_FAILURE,
                               package='Products.PasswordResetTool.tests',
                               test_class=MockMailHostTestCase),
        ))
