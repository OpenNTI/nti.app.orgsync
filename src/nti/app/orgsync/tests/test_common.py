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

from redis_lock import AlreadyAcquired

from nti.app.orgsync.common import get_account
from nti.app.orgsync.common import get_redis_lock
from nti.app.orgsync.common import is_locked_held
from nti.app.orgsync.common import get_organization

from nti.app.orgsync.tests import OrgSyncApplicationTestLayer

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestCommon(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    @fudge.patch('nti.app.orgsync.common.RedisLock')
    def test_get_redis_lock(self, mock_rl):
        mock_rl.is_callable().returns_fake()
        assert_that(get_redis_lock('foo'), is_not(none()))

    @fudge.patch('nti.app.orgsync.common.RedisLock.acquire',
                 'nti.app.orgsync.common.RedisLock.release')
    def test_is_locked_held(self, mock_ac, mockl_rel):
        mock_ac.is_callable().returns(True)
        mockl_rel.is_callable().returns_fake()
        assert_that(is_locked_held('foo'), is_(False))

        mock_ac.is_callable().returns(False)
        assert_that(is_locked_held('foo'), is_(True))
        
        mock_ac.is_callable().raises(AlreadyAcquired)
        assert_that(is_locked_held('foo'), is_(True))

    @WithSharedApplicationMockDS
    @fudge.patch('nti.app.orgsync.common.load_account')
    def test_get_account(self, mock_ga):
        mock_ga.is_callable().returns_fake()
        assert_that(get_account('foo'), is_not(none()))
    
    @WithSharedApplicationMockDS
    @fudge.patch('nti.app.orgsync.common.load_organization')
    def test_get_organization(self, mock_go):
        mock_go.is_callable().returns_fake()
        assert_that(get_organization('foo'), is_not(none()))
