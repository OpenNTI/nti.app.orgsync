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

import fudge

from nti.app.orgsync.synchronize import synchronize_orgsync
from nti.app.orgsync.synchronize import create_orgsync_sync_job

from nti.app.orgsync.tests import NoOpCM

from nti.app.orgsync.tests import OrgSyncApplicationTestLayer

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestSync(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    @fudge.patch('nti.app.orgsync.synchronize.get_redis_lock',
                 'nti.app.orgsync.synchronize.process_classifications',
                 'nti.app.orgsync.synchronize.process_membership_logs',
                 'nti.app.orgsync.synchronize.getUtility',
                 'nti.app.orgsync.subscribers.orgsync_source_snapshot')
    def test_sync(self, mock_lock, mock_cla, mock_pml, mock_gu, mock_snapshot):
        mock_cla.is_callable().returns(True)
        mock_pml.is_callable().returns(True)
        mock_gu.is_callable().returns_fake()
        mock_snapshot.is_callable().returns_fake()
        mock_lock.is_callable().returns(NoOpCM())
        successful = synchronize_orgsync()
        assert_that(successful, is_(True))

    @WithSharedApplicationMockDS
    @fudge.patch('nti.app.orgsync.synchronize.synchronize_orgsync')
    def test_create_orgsync_sync_job(self, mock_sync):
        mock_sync.is_callable().returns_fake()
        job = create_orgsync_sync_job("user",)
        assert_that(job, is_not(none()))
