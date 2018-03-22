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

from nti.app.orgsync.views import OrgSyncPathAdapter

from nti.dataserver import authorization as nauth

@view_config(name="sync")
@view_defaults(route_name="objects.generic.traversal",
               renderer="rest",
               permission=nauth.ACT_NTI_ADMIN,
               context=OrgSyncPathAdapter,
               request_method="POST")
class OrgSyncSyncView(AbstractAuthenticatedView):

    def __call__(self):
        return self.request.response
