#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import has_entry
from hamcrest import has_length
from hamcrest import assert_that

from nti.app.orgsync.tests import OrgSyncApplicationTestLayer

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestOrgViews(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_organization(self):
        self.testapp.get('/dataserver2/orgsync/orgs/30000',
                         status=404)

        self.testapp.get('/dataserver2/orgsync/orgs/152512',
                         status=200)

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_orgs(self):
        res = self.testapp.get('/dataserver2/orgsync/orgs',
                                status=200)
        assert_that(res.json_body['Items'], has_length(1))
        assert_that(res.json_body['Items'][0], has_entry('id', 152512))

        # Filter with nonexistent id
        res = self.testapp.get('/dataserver2/orgsync/orgs',
                                params={
                                    'id': 152648
                                },
                                status=200)
        
        assert_that(res.json_body['Items'], has_length(0))

        # Filter with existing id
        res = self.testapp.get('/dataserver2/orgsync/orgs',
                                params={
                                    'id': 152512
                                },
                                status=200)
        assert_that(res.json_body['Items'], has_length(1))
        assert_that(res.json_body['Items'][0], has_entry('id', 152512))

        # Multiple filters empty
        res = self.testapp.get('/dataserver2/orgsync/orgs',
                                params={
                                    'id': 152512,
                                    'short_name': 'doesnt_exist'
                                },
                                status=200)
        
        assert_that(res.json_body['Items'], has_length(0))

        # Multiple filters existing
        res = self.testapp.get('/dataserver2/orgsync/orgs',
                                params={
                                    'id': 152512,
                                    'short_name': '2018 S.O.U.L Conference'
                                },
                                status=200)
        assert_that(res.json_body['Items'], has_length(1))
        assert_that(res.json_body['Items'][0], has_entry('id', 152512))
