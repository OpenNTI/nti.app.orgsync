#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

from nti.app.orgsync.tests import OrgSyncApplicationTestLayer

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS


class TestOrgViews(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_organization(self):
        self.testapp.get('/dataserver2/orgsync/orgs/30000',
                         status=404)

        self.testapp.get('/dataserver2/orgsync/orgs/152512',
                         status=200)

    @WithSharedApplicationMockDS(testapp=True, users=True)
    def test_orgs(self):
        self.testapp.get('/dataserver2/orgsync/orgs',
                         status=200)
