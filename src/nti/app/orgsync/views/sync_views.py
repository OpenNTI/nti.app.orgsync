#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from datetime import datetime
from datetime import timedelta

from requests.structures import CaseInsensitiveDict

from pyramid.view import view_config
from pyramid.view import view_defaults

from sqlalchemy import func

from sqlalchemy.orm import aliased

from zope import component

from zope.cachedescriptors.property import Lazy

from nti.app.base.abstract_views import AbstractAuthenticatedView

from nti.app.externalization.view_mixins import ModeledContentUploadRequestUtilsMixin

from nti.app.orgsync import SYNCHRONIZE

from nti.app.orgsync.interfaces import ACT_SYNC_DB

from nti.app.orgsync.synchronize import create_orgsync_sync_job

from nti.app.orgsync.views import OrgSyncPathAdapter

from nti.orgsync.client import DEFAULT_MAX_WORKERS

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.orgsync_rdbms.entries.alchemy import MembershipLog

from nti.orgsync_rdbms.utils import parse_date

logger = __import__('logging').getLogger(__name__)


@view_config(name="sync")
@view_config(name=SYNCHRONIZE)
@view_defaults(route_name="objects.generic.traversal",
               renderer="rest",
               permission=ACT_SYNC_DB,
               context=OrgSyncPathAdapter,
               request_method="POST")
class OrgSyncSyncView(AbstractAuthenticatedView,
                      ModeledContentUploadRequestUtilsMixin):

    def readInput(self, value=None):
        result = None
        if self.request.body:
            result = super(OrgSyncSyncView, self).readInput(value)
        return CaseInsensitiveDict(result or {})

    @Lazy
    def database(self):
        return component.getUtility(IOrgSyncDatabase)

    @Lazy
    def latest(self):
        session = getattr(self.database, 'session', self.database)
        # pylint: disable=no-member
        entries = aliased(MembershipLog)
        return session.query(func.max(entries.created_at)).scalar()

    def __call__(self):
        data = self.readInput()
        # parse dates
        end_date = data.get('endDate') or None
        end_date = parse_date(end_date) if end_date else None
        start_date = data.get('startDate') or None
        start_date = parse_date(start_date) if start_date else None
        if end_date is None:
            end_date = self.latest or datetime.now()
            end_date = end_date + timedelta(days=7)
        if start_date is None:
            start_date = end_date - timedelta(days=7)
        # parse workers
        workers = int(data.get('workers') or DEFAULT_MAX_WORKERS)
        # pylint: disable=no-member
        creator = self.remoteUser.username
        return create_orgsync_sync_job(creator, start_date, end_date, workers)
