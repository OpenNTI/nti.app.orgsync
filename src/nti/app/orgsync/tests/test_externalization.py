#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import assert_that
from hamcrest import has_entries

from zope import component

from nti.app.orgsync.common import get_all_accounts
from nti.app.orgsync.common import get_all_organizations

from nti.app.orgsync.tests import OrgSyncApplicationTestLayer

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS

from nti.externalization.externalization import to_external_object

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.orgsync_rdbms.entries.alchemy import get_membership_logs


class TestExternalization(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    @WithSharedApplicationMockDS(testapp=False, users=False)
    def test_org_external(self):
        orgs = get_all_organizations()
        result = to_external_object(orgs[0])
        assert_that(result, has_entries('id', 152512))

        accounts = get_all_accounts()
        result = to_external_object(accounts[0])
        assert_that(result, has_entries('id', 7170547))

        db = component.getUtility(IOrgSyncDatabase)
        logs = get_membership_logs(db)
        result = to_external_object(logs[0])
        assert_that(result, has_entries('id', 59227531))
