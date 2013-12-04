################################################################
# eteaching.policy
# (C) 2013, ZOPYX Ltd.
################################################################

import os
from base import TestBase

from zExceptions import Unauthorized

class BasicTests(TestBase):

    def testLanguageSettings(self):
        lang_tool = self.portal.portal_languages
        default_language = self.portal.portal_languages.getDefaultLanguage()
        self.assertEqual(default_language == 'en', True)

    def testSetupSite(self):
        self.login('god')
        view = self.portal.restrictedTraverse('@@new-site')
        view(self.portal)

    def testCreateTestFolder(self):
        self.login('god')
        self.portal.invokeFactory('eteaching.policy.testfolder', id='foo')
        assert self.portal['foo'].portal_type == 'eteaching.policy.testfolder'

def test_suite():
    from unittest2 import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(BasicTests))
    return suite
