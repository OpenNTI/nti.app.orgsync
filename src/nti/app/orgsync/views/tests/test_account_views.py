#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

import os
import codecs

import fudge

from nti.app.orgsync.tests import OrgSyncApplicationTestLayer

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS

from nti.orgsync.accounts.utils import parse_account_source


class TestAccountViews(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    @WithSharedApplicationMockDS(testapp=True, users=True)
    @fudge.patch('nti.app.orgsync.views.get_account')
    def test_sync(self, mock_sync):
        path = os.path.join(os.path.dirname(__file__), 'data',
                            "account.json")
        with codecs.open(path, "r", "UTF-8") as fp:
            org = parse_account_source(fp)

        mock_sync.is_callable().returns(None)
        self.testapp.get('/dataserver2/orgsync/accounts/30000',
                         status=404)

        mock_sync.is_callable().returns(org)
        self.testapp.get('/dataserver2/orgsync/accounts/7170547',
                         status=200)
