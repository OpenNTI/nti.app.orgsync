#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that

from datetime import datetime

import fudge

from nti.app.orgsync.snapshot import is_snapshot_lock_held

from nti.app.orgsync.snapshot import create_orgsync_source_snapshot_job

from nti.app.orgsync.tests import NoOpCM
from nti.app.orgsync.tests import OrgSyncApplicationTestLayer

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestSnapshot(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    @WithSharedApplicationMockDS(testapp=False, users=False)
    @fudge.patch('nti.app.orgsync.snapshot.db_snapshot',
                 'nti.app.orgsync.snapshot.get_redis_lock')
    def test_db_snapshot(self, mock_dbs, mock_sl):
        mock_dbs.is_callable().returns_fake()
        mock_sl.is_callable().returns(NoOpCM())
        job = create_orgsync_source_snapshot_job("user", datetime.now())
        assert_that(job, is_not(none()))

    @fudge.patch('nti.app.orgsync.snapshot.is_locked_held',)
    def test_is_snapshot_lock_held(self, mock_ilh):
        mock_ilh.is_callable().returns(True)
        assert_that(is_snapshot_lock_held(), is_(True))
