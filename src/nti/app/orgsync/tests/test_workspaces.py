#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

from hamcrest import none
from hamcrest import is_not
from hamcrest import has_item
from hamcrest import has_entry
from hamcrest import assert_that
does_not = is_not

from nti.app.orgsync.interfaces import IOrgSyncWorkspace

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS

from nti.appserver.workspaces import UserService

from nti.dataserver.tests import mock_dataserver

from nti.externalization.externalization import toExternalObject


class TestUserService(ApplicationLayerTest):

    @WithSharedApplicationMockDS(testapp=False, users=True)
    def test_workspace(self):
        with mock_dataserver.mock_db_trans(self.ds):
            user = self._get_user(self.default_username)
            # find the workspace
            orgsync_wss = None
            service = UserService(user)
            for ws in service.workspaces or ():
                if IOrgSyncWorkspace.providedBy(ws):
                    orgsync_wss = ws
                    break
            assert_that(orgsync_wss, is_not(none()))
            # externalize
            ext_object = toExternalObject(service)
            assert_that(ext_object['Items'],
                        has_item(has_entry('Title', 'orgsync')))
