#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid.view import view_config
from pyramid.view import view_defaults

from nti.app.base.abstract_views import AbstractAuthenticatedView

from nti.app.externalization.view_mixins import BatchingUtilsMixin

from nti.app.orgsync.interfaces import ACT_VIEW_ACCOUNTS

from nti.app.orgsync.common import get_all_accounts

from nti.app.orgsync.views import AccountsPathAdapter

from nti.externalization.externalization import to_external_object

from nti.externalization.interfaces import LocatedExternalDict
from nti.externalization.interfaces import StandardExternalFields

from nti.orgsync.accounts.interfaces import IAccount

from nti.orgsync_rdbms.accounts.interfaces import IStorableAccount

ITEMS = StandardExternalFields.ITEMS
TOTAL = StandardExternalFields.TOTAL

logger = __import__('logging').getLogger(__name__)


@view_config(context=IAccount)
@view_config(context=IStorableAccount)
@view_defaults(route_name="objects.generic.traversal",
               renderer="rest",
               permission=ACT_VIEW_ACCOUNTS,
               request_method="GET")
class AccountView(AbstractAuthenticatedView):

    def __call__(self):
        result = to_external_object(self.context)
        result.__name__ = self.request.view_name
        result.__parent__ = self.request.context
        return result


@view_config(context=AccountsPathAdapter)
@view_defaults(route_name="objects.generic.traversal",
               renderer="rest",
               permission=ACT_VIEW_ACCOUNTS,
               request_method="GET")
class AccountsView(AbstractAuthenticatedView,
                   BatchingUtilsMixin):

    _DEFAULT_BATCH_START = 0
    _DEFAULT_BATCH_SIZE = 30

    def __call__(self):
        result = LocatedExternalDict()
        result.__name__ = self.request.view_name
        result.__parent__ = self.request.context
        accounts = get_all_accounts()
        items = result[ITEMS] = accounts
        self._batch_items_iterable(result, items)
        result[TOTAL] = len(accounts)
        return result
