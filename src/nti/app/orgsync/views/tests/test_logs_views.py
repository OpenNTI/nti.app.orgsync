#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

import fudge

from nti.app.orgsync.tests import OrgSyncApplicationTestLayer

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestLogsViews(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    @WithSharedApplicationMockDS(testapp=True, users=True)
    @fudge.patch('nti.app.orgsync.views.logs_views.get_membership_logs')
    def test_logs(self, mock_gml):
        mock_gml.is_callable().returns([1,2,3])

        self.testapp.get('/dataserver2/orgsync/logs',
                         params={'orgs': '152512',
                                 'accounts': '7170547'},
                         status=200)


        self.testapp.get('/dataserver2/orgsync/logs/@@last_entry',
                         status=200)
