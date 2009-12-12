"""
PasswordResetTool doctests
"""

import doctest
import unittest
from Testing.ZopeTestCase import FunctionalDocFileSuite
from Products.PloneTestCase import PloneTestCase
from Products.CMFPlone.tests.test_mails import MockMailHostTestCase

PloneTestCase.setupPloneSite()


def test_suite():
    return unittest.TestSuite((
        FunctionalDocFileSuite('browser.txt',
                               optionflags = doctest.REPORT_ONLY_FIRST_FAILURE,
                               package='Products.PasswordResetTool.tests',
                               test_class=MockMailHostTestCase),
        ))
