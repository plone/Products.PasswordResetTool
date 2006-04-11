"""
PasswordResetTool doctests
"""

import os, sys

if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest
from Testing.ZopeTestCase import FunctionalDocFileSuite, FunctionalDocTestSuite
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
                                package='Products.PasswordResetTool.tests',
                                test_class=MockMailHostTestCase),
        ))

if __name__ == '__main__':
    framework()

