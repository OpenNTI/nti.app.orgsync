#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from hamcrest import is_
from hamcrest import assert_that

import fudge

from nti.app.orgsync.synchronize import synchronize_orgsync

from nti.app.orgsync.tests import OrgSyncApplicationTestLayer

from nti.app.testing.application_webtest import ApplicationLayerTest


class TestSync(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    @fudge.patch('nti.app.orgsync.synchronize.process_classifications',
                 'nti.app.orgsync.synchronize.process_membership_logs',)
    def test_sync(self, mock_cla, mock_pml):
        mock_cla.is_callable().returns_fake()
        mock_pml.is_callable().returns_fake()
        successful = synchronize_orgsync()
        assert_that(successful, is_(True))
