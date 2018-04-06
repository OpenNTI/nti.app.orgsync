#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods

import os
import codecs

import fudge

from nti.app.orgsync.tests import OrgSyncApplicationTestLayer

from nti.app.testing.application_webtest import ApplicationLayerTest

from nti.app.testing.decorators import WithSharedApplicationMockDS

from nti.orgsync.organizations.utils import parse_organization_source


class TestOrgViews(ApplicationLayerTest):

    layer = OrgSyncApplicationTestLayer

    @WithSharedApplicationMockDS(testapp=True, users=True)
    @fudge.patch('nti.app.orgsync.views.get_organization')
    def test_organization(self, mock_sync):
        path = os.path.join(os.path.dirname(__file__), 'data',
                            "organization.json")
        with codecs.open(path, "r", "UTF-8") as fp:
            org = parse_organization_source(fp)

        mock_sync.is_callable().returns(None)
        self.testapp.get('/dataserver2/orgsync/orgs/30000',
                         status=404)

        mock_sync.is_callable().returns(org)
        self.testapp.get('/dataserver2/orgsync/orgs/152512',
                         status=200)
