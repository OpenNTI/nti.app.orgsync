#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from datetime import datetime

import isodate

from pyramid.view import view_config
from pyramid.view import view_defaults

from requests.structures import CaseInsensitiveDict

from zope import component

from zope.cachedescriptors.property import Lazy

from nti.app.base.abstract_views import AbstractAuthenticatedView

from nti.app.externalization.view_mixins import ModeledContentUploadRequestUtilsMixin

from nti.app.orgsync.interfaces import ACT_SNAPSHOPT

from nti.app.orgsync.snapshot import is_snapshot_lock_held
from nti.app.orgsync.snapshot import create_orgsync_source_snapshot_job

from nti.app.orgsync.views import OrgSyncPathAdapter

from nti.app.spark.common import parse_timestamp

from nti.app.spark.views import SPARK_JOB_ERROR
from nti.app.spark.views import SPARK_JOB_STATUS

from nti.orgsync_spark import CREATED_AT

from nti.orgsync_spark.accounts import IHistoricalAccounts

from nti.orgsync_spark.entries import IMembershipLogs

from nti.orgsync_spark.organizations import IHistoricalOrganizations

from nti.common.string import is_true

from nti.externalization.interfaces import LocatedExternalDict

logger = __import__('logging').getLogger(__name__)


@view_config(name="snapshot")
@view_defaults(route_name='objects.generic.traversal',
               renderer='rest',
               request_method='POST',
               context=OrgSyncPathAdapter,
               permission=ACT_SNAPSHOPT)
class SnapshotOrgSyncView(AbstractAuthenticatedView,
                          ModeledContentUploadRequestUtilsMixin):
    """
    Schedule a orgsync snapshop job
    """

    def readInput(self, value=None):
        result = None
        if self.request.body:
            result = super(SnapshotOrgSyncView, self).readInput(value)
        return CaseInsensitiveDict(result or {})

    def __call__(self):
        result = LocatedExternalDict()
        result.__name__ = self.request.view_name
        result.__parent__ = self.request.context
        # read params
        data = self.readInput()
        # pylint: disable=no-member
        creator = self.remoteUser.username
        # parse dates
        end_date = data.get('endDate')
        end_date = parse_timestamp(end_date) if end_date else None
        start_date = data.get('startDate')
        start_date = parse_timestamp(start_date) if start_date else None
        # parse timestamp
        timestamp = parse_timestamp(data.get('timestamp'))
        # parse bools
        logs = is_true(data.get('logs', False))
        archive = is_true(data.get('archive', True))
        # create job
        result = create_orgsync_source_snapshot_job(creator, timestamp, start_date,
                                                    end_date, logs, archive)
        return result


@view_config(name="snapshot")
@view_defaults(route_name='objects.generic.traversal',
               renderer="templates/snapshot.pt",
               request_method='GET',
               context=OrgSyncPathAdapter,
               permission=ACT_SNAPSHOPT)
class SnapshotView(AbstractAuthenticatedView):

    @Lazy
    def timestamps(self):
        historical = component.getUtility(IHistoricalAccounts)
        result = set(historical.timestamps or ())
        historical = component.getUtility(IHistoricalOrganizations)
        result.intersection(set(historical.timestamps or ()))
        return sorted(result, reverse=True)

    @Lazy
    def last_entry(self):
        entries = component.getUtility(IMembershipLogs).entries
        if entries is not None:
            tdt = entries.agg({CREATED_AT: "max"}).collect()[0][0]
            return isodate.datetime_isoformat(tdt, isodate.DATE_EXT_COMPLETE)
    
    @Lazy
    def snapshots(self):
        result = []
        accounts = component.getUtility(IHistoricalAccounts)
        organizations = component.getUtility(IHistoricalOrganizations)
        # pylint: disable=not-an-iterable
        for timestamp in self.timestamps or ():
            tdt = datetime.fromtimestamp(timestamp)
            result.append({
                'timestamp': isodate.datetime_isoformat(tdt, isodate.DATE_EXT_COMPLETE),
                'accounts': accounts.partition(timestamp).count(),
                'organizations': organizations.partition(timestamp).count(),
            })
        return result
    
    def __call__(self):
        # exclude final forward slash for join
        context_url = self.request.resource_url(self.context)[:-1]
        snapshot_url = "/".join((context_url, '@@snapshot'))
        job_poll_url = "/".join((context_url, SPARK_JOB_STATUS + '?jobId='))
        job_error_url = "/".join((context_url, SPARK_JOB_ERROR + '?jobId='))
        result = {
            'snapshots': self.snapshots,
            'snapshot_url': snapshot_url,
            'job_poll_url': job_poll_url,
            'job_error_url': job_error_url,
            'last_entry': self.last_entry,
            'lock_held': is_snapshot_lock_held(),
        }
        return result
