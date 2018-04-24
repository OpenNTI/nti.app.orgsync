#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

from zope import component

from nti.app.orgsync.tests.orgsync_db import drop
from nti.app.orgsync.tests.orgsync_db import synchronize

from nti.app.testing.application_webtest import ApplicationTestLayer

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase


class NoOpCM(object):

    def __enter__(self):
        pass

    def __exit__(self, t, v, tb):
        pass


class OrgSyncApplicationTestLayer(ApplicationTestLayer):

    @classmethod
    def setUp(cls):
        super(OrgSyncApplicationTestLayer, cls).setUp()
        cls.database = component.getUtility(IOrgSyncDatabase)
        synchronize(cls.database)

    @classmethod
    def tearDown(cls):
        super(OrgSyncApplicationTestLayer, cls).tearDown()
        drop(cls.database)
