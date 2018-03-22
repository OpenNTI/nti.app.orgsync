#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import assert_that

import fudge

from nti.app.orgsync.sync import synchronize_orgsync

from nti.app.orgsync.tests import OrgSyncApplicationTestLayer

from nti.app.testing.application_webtest import ApplicationLayerTest

class TestSync(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    @fudge.patch('nti.app.orgsync.sync.synchronize',
                 'nti.app.orgsync.sync.get_api_key')
    def test_sync(self, mock_sy, mock_key):
        mock_sy.is_callable().returns_fake()
        mock_key.is_callable().returns('abc')
        successful = synchronize_orgsync()
        assert_that(successful, is_(True))
