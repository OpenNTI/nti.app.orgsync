#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import isodate

from pyramid.view import view_config
from pyramid.view import view_defaults

from requests.structures import CaseInsensitiveDict

from sqlalchemy import func

from sqlalchemy.orm import aliased

from zope import component

from zope.cachedescriptors.property import Lazy

from nti.app.base.abstract_views import AbstractAuthenticatedView

from nti.app.externalization.view_mixins import ModeledContentUploadRequestUtilsMixin

from nti.app.orgsync import SNAPSHOT

from nti.app.orgsync.interfaces import ACT_SNAPSHOPT

from nti.app.orgsync.snapshot import create_orgsync_source_snapshot_job

from nti.app.orgsync.views import OrgSyncPathAdapter

from nti.app.spark.common import parse_timestamp

from nti.orgsync_rdbms.entries.alchemy import MembershipLog

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.common.string import is_true

from nti.externalization.interfaces import LocatedExternalDict

logger = __import__('logging').getLogger(__name__)


@view_config(name=SNAPSHOT)
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

    DEFAULT_START = isodate.parse_date("2017-01-01")

    @Lazy
    def last_entry(self):
        session = component.getUtility(IOrgSyncDatabase).session
        entries = aliased(MembershipLog)
        return session.query(func.max(entries.created_at)).scalar()

    def readInput(self, value=None):
        result = None
        if self.request.body:
            result = super(SnapshotOrgSyncView, self).readInput(value)
        return CaseInsensitiveDict(result or {})

    def create_job(self, creator, timestamp, start_date, end_date, logs=True, archive=True):
        result = create_orgsync_source_snapshot_job(creator, timestamp, start_date,
                                                    end_date, logs, archive)
        return result

    def parse_endDate(self, values):
        # parse end date. Default to today if not present
        return parse_timestamp(values.get('endDate'))
    
    def parse_startDate(self, values):
        start_date = values.get('startDate')
        alt_start = self.last_entry or self.DEFAULT_START
        return parse_timestamp(start_date) if start_date else alt_start

    def parse_timestamp(self, values):
        return parse_timestamp(values.get('timestamp'))

    def __call__(self):
        result = LocatedExternalDict()
        result.__name__ = self.request.view_name
        result.__parent__ = self.request.context
        # read params
        data = self.readInput()
        # pylint: disable=no-member
        creator = self.remoteUser.username
        # parse end date. Default to today if not present
        end_date = self.parse_endDate(data)
        # parse start date
        start_date = self.parse_startDate(data)
        # parse timestamp
        timestamp = self.parse_timestamp(data)
        # parse bools
        logs = is_true(data.get('logs', False))
        archive = is_true(data.get('archive', True))
        # create job
        result = self.create_job(creator, timestamp, start_date, 
                                 end_date, logs, archive)
        return result
