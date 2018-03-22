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

from nti.app.orgsync.common import get_redis_lock


class TestCommon(unittest.TestCase):

    @fudge.patch('nti.app.orgsync.common.RedisLock')
    def test_get_redis_lock(self, mock_rl):
        mock_rl.is_callable().returns_fake()
        assert_that(get_redis_lock('foo'), is_not(none()))
