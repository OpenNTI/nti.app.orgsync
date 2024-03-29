#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid import httpexceptions as hexc

from pyramid.view import view_config
from pyramid.view import view_defaults

from zope import component

from zope.cachedescriptors.property import Lazy

from nti.app.base.abstract_views import AbstractAuthenticatedView

from nti.app.externalization.error import raise_json_error

from nti.app.orgsync import MessageFactory as _

from nti.app.externalization.view_mixins import BatchingUtilsMixin

from nti.app.orgsync import ID
from nti.app.orgsync import LONG_NAME

from nti.app.orgsync.interfaces import ACT_VIEW_ORGS

from nti.app.orgsync.common import get_all_organizations

from nti.app.orgsync.views import OrgsPathAdapter

from nti.externalization.externalization import to_external_object

from nti.externalization.interfaces import LocatedExternalDict
from nti.externalization.interfaces import StandardExternalFields

from nti.orgsync.organizations.interfaces import IOrganization

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.orgsync_rdbms.organizations.interfaces import IStorableOrganization

from nti.ou.orgsync_recommendations import DESCRIPTION

from nti.orgsync_spark import CREATED_AT

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

    SORT_COLS = (ID, CREATED_AT, LONG_NAME, DESCRIPTION)

    @Lazy
    def database(self):
        return component.getUtility(IOrgSyncDatabase)

    @Lazy
    def filters(self):
        filters = dict(self.request.params)
        filters.pop('batchSize', None)
        filters.pop('batchStart', None)
        return filters

    def __call__(self):
        # pylint: disable=no-member
        sort_by = self.filters.pop('sortBy', ID)
        if sort_by not in self.SORT_COLS:
            raise_json_error(self.request,
                             hexc.HTTPUnprocessableEntity,
                             {
                                 'message': _(u"Invalid sort column."),
                                 'code': 'CannotSortOnColumn',
                             },
                             None)
        result = LocatedExternalDict()
        result.__name__ = self.request.view_name
        result.__parent__ = self.request.context
        orgs = get_all_organizations(self.database, self.filters)
        items = result[ITEMS] = orgs
        items.sort(key=lambda x: getattr(x, sort_by))
        self._batch_items_iterable(result, items)
        result[TOTAL] = len(orgs)
        return result
