#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import none
from hamcrest import is_not
from hamcrest import assert_that

import unittest

import fudge

from nti.app.orgsync.common import get_account
from nti.app.orgsync.common import get_redis_lock
from nti.app.orgsync.common import get_organization


class TestCommon(unittest.TestCase):

    @fudge.patch('nti.app.orgsync.common.RedisLock')
    def test_get_redis_lock(self, mock_rl):
        mock_rl.is_callable().returns_fake()
        assert_that(get_redis_lock('foo'), is_not(none()))

    @fudge.patch('nti.app.orgsync.common.AccountClient.get_account')
    def test_get_account(self, mock_ga):
        mock_ga.is_callable().returns_fake()
        assert_that(get_account('foo'), is_not(none()))

    @fudge.patch('nti.app.orgsync.common.OrgClient.get_organization')
    def test_get_organization(self, mock_go):
        mock_go.is_callable().returns_fake()
        assert_that(get_organization('foo'), is_not(none()))
