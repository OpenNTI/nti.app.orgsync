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

import simplejson

from zope import component

from nti.app.orgsync.tests import OrgSyncApplicationTestLayer

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS

from nti.externalization.externalization import to_external_object

from nti.orgsync.accounts.utils import parse_account_source

from nti.orgsync.entries.utils import membershiplog_object_hook
from nti.orgsync.entries.utils import parse_membership_log_from_external

from nti.orgsync.organizations.utils import parse_organization_source

from nti.orgsync_rdbms.accounts.alchemy import load_accounts

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.orgsync_rdbms.entries.alchemy import load_membership_logs

from nti.orgsync_rdbms.organizations.alchemy import load_organizations


class TestExternalization(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    @WithSharedApplicationMockDS(testapp=False, users=False)
    def test_org_external(self):
        db = component.getUtility(IOrgSyncDatabase)

        # org
        path = os.path.join(os.path.dirname(__file__), 'data',
                            "organization.json")
        with codecs.open(path, "r", "UTF-8") as fp:
            org = parse_organization_source(fp)

        orgs = load_organizations(db, (org,))
        assert_that(orgs, has_length(1))
        
        result = to_external_object(orgs[0])
        assert_that(result, has_entries('id', 152512))
        
        # account
        path = os.path.join(os.path.dirname(__file__), 'data',
                            "account.json")
        with codecs.open(path, "r", "UTF-8") as fp:
            account = parse_account_source(fp)

        accounts = load_accounts(db, (account,))
        assert_that(accounts, has_length(1))        
        result = to_external_object(accounts[0])
        assert_that(result, has_entries('id', 7170547))
        
        # log
        path = os.path.join(os.path.dirname(__file__), 'data',
                            "membership_log.json")
        with codecs.open(path, "r", "UTF-8") as fp:
            data = membershiplog_object_hook(simplejson.load(fp))
            entry = parse_membership_log_from_external(data)

        entries = load_membership_logs(db, (entry,))
        assert_that(entries, has_length(1))
        
        result = to_external_object(entries[0])
        assert_that(result, has_entries('id', 59227531))
