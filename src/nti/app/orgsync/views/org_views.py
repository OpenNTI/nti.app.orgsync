#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import six
import collections

from requests.structures import CaseInsensitiveDict

from pyramid.view import view_config
from pyramid.view import view_defaults

from nti.app.base.abstract_views import AbstractAuthenticatedView

from nti.app.externalization.view_mixins import BatchingUtilsMixin

from nti.app.orgsync.interfaces import ACT_VIEW_ORGS

from nti.app.orgsync.common import get_all_organizations

from nti.app.orgsync.views import OrgsPathAdapter

from nti.externalization.externalization import to_external_object

from nti.externalization.interfaces import LocatedExternalDict
from nti.externalization.interfaces import StandardExternalFields

from nti.orgsync.organizations.interfaces import IOrganization

from nti.orgsync_rdbms.organizations.interfaces import IStorableOrganization

ITEMS = StandardExternalFields.ITEMS
TOTAL = StandardExternalFields.TOTAL

logger = __import__('logging').getLogger(__name__)


@view_config(context=IOrganization)
@view_config(context=IStorableOrganization)
@view_defaults(route_name="objects.generic.traversal",
               renderer="rest",
               permission=ACT_VIEW_ORGS,
               context=IOrganization,
               request_method="GET")
class OrganizationView(AbstractAuthenticatedView):

    def __call__(self):
        result = to_external_object(self.context)
        result.__name__ = self.request.view_name
        result.__parent__ = self.request.context
        return result


@view_config(context=OrgsPathAdapter)
@view_defaults(route_name="objects.generic.traversal",
               renderer="rest",
               permission=ACT_VIEW_ORGS,
               request_method="GET")
class OrganizationsView(AbstractAuthenticatedView,
                        BatchingUtilsMixin):

    _DEFAULT_BATCH_START = 0
    _DEFAULT_BATCH_SIZE = 30

    def __call__(self):
        result = LocatedExternalDict()
        result.__name__ = self.request.view_name
        result.__parent__ = self.request.context
        filters = CaseInsensitiveDict(self.request.params)
        for f in filters.keys():
            filt = filters[f]
            # listify any singular values to match multi value searches
            if isinstance(filt, six.string_types) or not isinstance(filt, collections.Iterable):
                filters[f] = [filt]
        orgs = get_all_organizations(filters=filters)
        items = result[ITEMS] = orgs
        self._batch_items_iterable(result, items)
        result[TOTAL] = len(orgs)
        return result
