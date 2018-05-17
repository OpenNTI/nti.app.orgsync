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

from nti.ou.analysis import OUNET_ID


class TestAccountViews(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    existing_username = 'jfazio@state-university'

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_account(self):
        self.testapp.get('/dataserver2/orgsync/accounts/30000',
                         status=404)

        self.testapp.get('/dataserver2/orgsync/accounts/7170547',
                         status=200)

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_accounts(self):
        res = self.testapp.get('/dataserver2/orgsync/accounts',
                               status=200)

        assert_that(res.json_body['Items'], has_length(1))
        assert_that(res.json_body['Items'][0],
                    has_entry('username', self.existing_username))

        res = self.testapp.get('/dataserver2/orgsync/accounts',
                               params={
                                   'username': 'some_other_username'
                               },
                               status=200)
        assert_that(res.json_body['Items'], has_length(0))

        res = self.testapp.get('/dataserver2/orgsync/accounts',
                               params={
                                   OUNET_ID: '112879506'
                               },
                               status=200)
        assert_that(res.json_body['Items'], has_length(1))

        res = self.testapp.get('/dataserver2/orgsync/accounts',
                               params={
                                   'username': self.existing_username
                               },
                               status=200)

        assert_that(res.json_body['Items'], has_length(1))
        assert_that(res.json_body['Items'][0], 
                    has_entry('username', self.existing_username))
