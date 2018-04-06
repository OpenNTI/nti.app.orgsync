#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import six

from requests.structures import CaseInsensitiveDict

from pyramid.view import view_config

from zope import component

from zope.cachedescriptors.property import Lazy

from nti.app.base.abstract_views import AbstractAuthenticatedView

from nti.app.orgsync.interfaces import ACT_VIEW_LOGS

from nti.app.orgsync.views import LogsPathAdapter

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.orgsync_rdbms.entries.alchemy import get_membership_logs

from nti.orgsync_rdbms.utils import parse_date

logger = __import__('logging').getLogger(__name__)


@view_config(route_name="objects.generic.traversal",
             renderer="rest",
             permission=ACT_VIEW_LOGS,
             context=LogsPathAdapter,
             request_method="GET")
class MembershipLogsView(AbstractAuthenticatedView):

    @Lazy
    def database(self):
        return component.getUtility(IOrgSyncDatabase)

    def __call__(self):
        values = CaseInsensitiveDict(self.request.params)
        end_date = parse_date(values.get('endDate'))
        start_date = parse_date(values.get('startDate'))
        orgs = values.get('orgs') or values.get('organizations')
        if isinstance(orgs, six.string_types):
            orgs = orgs.split(',')
        accounts = values.get('account') or values.get('accounts')
        if isinstance(accounts, six.string_types):
            accounts = accounts.split(',')
        result = get_membership_logs(self.database, start_date, 
                                     end_date, orgs, accounts)
        return result
