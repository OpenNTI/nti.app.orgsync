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

from nti.app.orgsync_spark.interfaces import ACT_SNAPSHOPT

from nti.app.orgsync_spark.snapshot import is_snapshot_lock_held
from nti.app.orgsync_spark.snapshot import create_orgsync_source_snapshot_job

from nti.app.orgsync_spark.views import SparkPathAdapter

from nti.app.spark.common import parse_timestamp

from nti.app.spark.views import SPARK_JOB_ERROR
from nti.app.spark.views import SPARK_JOB_STATUS

from nti.orgsync_spark import CREATED_AT

from nti.orgsync_spark.entries import IMembershipLogs

from nti.common.string import is_true

from nti.externalization.interfaces import LocatedExternalDict

from nti.spark.utils import get_timestamp

logger = __import__('logging').getLogger(__name__)


@view_config(name="snapshot")
@view_defaults(route_name='objects.generic.traversal',
               renderer='rest',
               request_method='POST',
               context=SparkPathAdapter,
               permission=ACT_SNAPSHOPT)
class SnapshotOrgSyncView(AbstractAuthenticatedView,
                          ModeledContentUploadRequestUtilsMixin):
    """
    Schedule a orgsync snapshop job
    """

    DEFAULT_START = 20170101

    @Lazy
    def last_entry(self):
        entries = component.getUtility(IMembershipLogs).entries
        if entries is not None:
            tdt = entries.agg({CREATED_AT: "max"}).collect()[0][0]
            return isodate.datetime_isoformat(tdt, isodate.DATE_EXT_COMPLETE)

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
        end_date = parse_timestamp(end_date) if end_date else get_timestamp()
        start_date = data.get('startDate')
        alternate_start = self.last_entry() or self.DEFAULT_START
        start_date = parse_timestamp(start_date) if start_date else alternate_start
        # parse timestamp
        timestamp = parse_timestamp(data.get('timestamp'))
        # parse bools
        logs = is_true(data.get('logs', False))
        archive = is_true(data.get('archive', True))
        # create job
        result = create_orgsync_source_snapshot_job(creator, timestamp, start_date,
                                                    end_date, logs, archive)
        return result
