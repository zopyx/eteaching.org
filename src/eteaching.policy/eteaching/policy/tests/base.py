################################################################
# eteaching.policy
# (C) 2013, ZOPYX Ltd.
################################################################

import os
import unittest2
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import setRoles, login
from plone.testing import z2

from zope.configuration import xmlconfig
from AccessControl.SecurityManagement import newSecurityManager
from zope.component import getUtility

import eteaching.policy
import plone.supermodel
import z3c.jbot

class PolicyFixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):

        xmlconfig.file('meta.zcml', z3c.jbot, context=configurationContext)
        for mod in [plone.supermodel,
                    eteaching.policy]: 
            xmlconfig.file('configure.zcml', mod, context=configurationContext)

        xmlconfig.file('patches.zcml', eteaching.policy, context=configurationContext)
        # Install product and call its initialize() function
        z2.installProduct(app, 'eteaching.policy')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        applyProfile(portal, 'eteaching.policy:default')
        portal.acl_users.userFolderAddUser('god', 'dummy', ['Manager'], []) 
        setRoles(portal, 'god', ['Manager'])
        portal.acl_users.userFolderAddUser('ppr', 'dummy', ['PPR'], []) 
        setRoles(portal, 'ppr', ['Member', 'PPR'])
        portal.acl_users.userFolderAddUser('member', 'dummy', ['Member'], []) 
        setRoles(portal, 'member', ['Member'])
        login(portal, 'god')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'eteaching.policy')


POLICY_FIXTURE = PolicyFixture()
POLICY_INTEGRATION_TESTING = IntegrationTesting(bases=(POLICY_FIXTURE,), name="PolicyFixture:Integration")

class TestBase(unittest2.TestCase):

    layer = POLICY_INTEGRATION_TESTING

    @property
    def portal(self):
        return self.layer['portal']

    def login(self, uid='god'):
        """ Login as manager """
        user = self.portal.acl_users.getUser(uid)
        newSecurityManager(None, user.__of__(self.portal.acl_users))

