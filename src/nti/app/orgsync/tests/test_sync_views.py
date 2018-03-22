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

from nti.dataserver.tests import mock_dataserver

class TestSyncViews(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    @WithSharedApplicationMockDS(testapp=True, users=True)
    @fudge.patch('nti.app.orgsync.views.sync_views.synchronize_orgsync')
    def test_sync(self, mock_sync):
        with mock_dataserver.mock_db_trans(self.ds):
            self._create_user("pgreazy")
        
        unauthed_environ = self._make_extra_environ("pgreazy")
        self.testapp.post('/dataserver2/orgsync/@@sync',
                          extra_environ=unauthed_environ,
                          status=403)

        mock_sync.is_callable().returns(False)
        self.testapp.post_json('/dataserver2/orgsync/@@sync',
                               status=422)

        mock_sync.is_callable().returns(True)
        self.testapp.post_json('/dataserver2/orgsync/@@sync',
                               status=200)
