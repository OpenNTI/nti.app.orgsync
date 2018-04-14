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

import isodate

from requests.structures import CaseInsensitiveDict

from pyramid import httpexceptions as hexc

from pyramid.view import view_config
from pyramid.view import view_defaults

from sqlalchemy import func

from sqlalchemy.orm import aliased

from zope import component

from zope.cachedescriptors.property import Lazy

from nti.app.base.abstract_views import AbstractAuthenticatedView

from nti.app.externalization.view_mixins import ModeledContentUploadRequestUtilsMixin

from nti.app.orgsync.interfaces import ACT_SYNC_DB

from nti.app.orgsync.synchronize import is_sync_lock_held
from nti.app.orgsync.synchronize import synchronize_orgsync

from nti.app.orgsync.views import OrgSyncPathAdapter

from nti.orgsync.client import DEFAULT_MAX_WORKERS

from nti.orgsync_rdbms.accounts.alchemy import Account

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.orgsync_rdbms.entries.alchemy import MembershipLog

from nti.orgsync_rdbms.organizations.alchemy import Organization

from nti.orgsync_rdbms.utils import parse_date

logger = __import__('logging').getLogger(__name__)


@view_config(name="sync")
@view_config(name="synchronize")
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
        end_date = parse_date(data.get('endDate'))
        start_date = parse_date(data.get('startDate'))
        if end_date is None:
            end_date = self.latest or datetime.now()
            end_date = end_date + timedelta(days=7)
        if start_date is None:
            start_date = end_date - timedelta(days=7)
        workers = int(data.get('workers') or DEFAULT_MAX_WORKERS)
        synchronize_orgsync(start_date, end_date, workers)
        return hexc.HTTPOk()


@view_config(context=OrgSyncPathAdapter)
@view_defaults(route_name="objects.generic.traversal",
               renderer="templates/sync.pt",
               name="synchronization",
               request_method="GET",
               permission=ACT_SYNC_DB)
class SynchronizationView(AbstractAuthenticatedView):

    @Lazy
    def database(self):
        return component.getUtility(IOrgSyncDatabase)

    @Lazy
    def accounts(self):
        session = getattr(self.database, 'session', self.database)
        return session.query(Account).count()

    @Lazy
    def organizations(self):
        session = getattr(self.database, 'session', self.database)
        return session.query(Organization).count()

    @Lazy
    def entries(self):
        session = getattr(self.database, 'session', self.database)
        return session.query(MembershipLog).count()

    @Lazy
    def latest(self):
        session = getattr(self.database, 'session', self.database)
        # pylint: disable=no-member
        entries = aliased(MembershipLog)
        return session.query(func.max(entries.created_at)).scalar()

    def __call__(self):
        # exclude final forward slash for join
        context_url = self.request.resource_url(self.context)[:-1]
        sync_url = "/".join((context_url, '@@sync'))
        last_entry = isodate.datetime_isoformat(self.latest,
                                                isodate.DATE_EXT_COMPLETE)
        result = {
            'sync_url': sync_url,
            'entries': self.entries,
            'accounts': self.accounts,
            'last_entry': last_entry,
            'lock_held': is_sync_lock_held(),
            'organizations': self.organizations,
        }
        return result
