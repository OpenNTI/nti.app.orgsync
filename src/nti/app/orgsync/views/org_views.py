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

from nti.app.orgsync.interfaces import ACT_VIEW_ORGS

from nti.externalization.externalization import to_external_object

from nti.orgsync.organizations.interfaces import IOrganization

from nti.orgsync_rdbms.organizations.interfaces import IStorableOrganization

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
