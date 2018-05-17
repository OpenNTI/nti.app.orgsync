#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import six

from pyramid import httpexceptions as hexc

from pyramid.view import view_config
from pyramid.view import view_defaults

from requests.structures import CaseInsensitiveDict

from sqlalchemy import func

from sqlalchemy.orm import aliased

from zope import component

from zope.cachedescriptors.property import Lazy

from nti.app.base.abstract_views import AbstractAuthenticatedView

from nti.app.externalization.view_mixins import BatchingUtilsMixin

from nti.app.orgsync import LAST_ENTRY

from nti.app.orgsync.interfaces import ACT_VIEW_LOGS

from nti.app.orgsync.views import LogsPathAdapter

from nti.externalization.interfaces import LocatedExternalDict
from nti.externalization.interfaces import StandardExternalFields

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.orgsync_rdbms.entries.alchemy import MembershipLog
from nti.orgsync_rdbms.entries.alchemy import get_membership_logs

from nti.orgsync_rdbms.utils import parse_date

ITEMS = StandardExternalFields.ITEMS
TOTAL = StandardExternalFields.TOTAL

logger = __import__('logging').getLogger(__name__)


@view_config(route_name="objects.generic.traversal",
             renderer="rest",
             permission=ACT_VIEW_LOGS,
             context=LogsPathAdapter,
             request_method="GET")
class MembershipLogsView(AbstractAuthenticatedView,
                         BatchingUtilsMixin):

    _DEFAULT_BATCH_START = 0
    _DEFAULT_BATCH_SIZE = 30

    @Lazy
    def database(self):
        return component.getUtility(IOrgSyncDatabase)

    def __call__(self):
        values = CaseInsensitiveDict(self.request.params)
        # parse dates
        end_date = parse_date(values.get('endDate'))
        start_date = parse_date(values.get('startDate'))
        # parse orgs
        orgs = values.get('orgs') or values.get('organizations')
        if isinstance(orgs, six.string_types):
            orgs = orgs.split(',')
        # parse accounts
        accounts = values.get('account') or values.get('accounts')
        if isinstance(accounts, six.string_types):
            accounts = accounts.split(',')
        # get logs
        result = LocatedExternalDict()
        result.__name__ = self.request.view_name
        result.__parent__ = self.request.context
        logs = get_membership_logs(self.database, start_date,
                                   end_date, orgs, accounts)()
        items = result[ITEMS] = logs
        self._batch_items_iterable(result, items)
        result[TOTAL] = len(accounts)
        return result


@view_config(name="lastentry")
@view_config(name=LAST_ENTRY)
@view_defaults(route_name="objects.generic.traversal",
               renderer="rest",
               permission=ACT_VIEW_LOGS,
               context=LogsPathAdapter,
               request_method="GET")
class LastEntryView(AbstractAuthenticatedView):

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
        end_date = self.latest
        if end_date is None:  # pragma: no cover
            raise hexc.HTTPNotFound()
        return end_date
