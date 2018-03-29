#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import has_length
from hamcrest import assert_that
from hamcrest import has_entries

import os
import codecs

from zope import component

from nti.app.orgsync.tests import OrgSyncApplicationTestLayer

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS

from nti.externalization.externalization import to_external_object

from nti.orgsync.accounts.utils import parse_account_source

from nti.orgsync.organizations.utils import parse_organization_source

from nti.orgsync_rdbms.accounts.alchemy import load_accounts

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.orgsync_rdbms.organizations.alchemy import load_organizations


class TestExternalization(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    @WithSharedApplicationMockDS(testapp=False, users=False)
    def test_org_external(self):
        path = os.path.join(os.path.dirname(__file__), 'data',
                            "organization.json")
        with codecs.open(path, "r", "UTF-8") as fp:
            org = parse_organization_source(fp)

        db = component.getUtility(IOrgSyncDatabase)
        orgs = load_organizations(db, (org,))
        assert_that(orgs, has_length(1))
        
        result = to_external_object(orgs[0])
        assert_that(result, has_entries('id', 152512))
        
    @WithSharedApplicationMockDS(testapp=False, users=False)
    def test_account_external(self):
        path = os.path.join(os.path.dirname(__file__), 'data',
                            "account.json")
        with codecs.open(path, "r", "UTF-8") as fp:
            account = parse_account_source(fp)

        db = component.getUtility(IOrgSyncDatabase)
        accounts = load_accounts(db, (account,))
        assert_that(accounts, has_length(1))
        
        result = to_external_object(accounts[0])
        assert_that(result, has_entries('id', 7170547))
