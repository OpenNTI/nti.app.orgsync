#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid.view import view_config

from nti.app.base.abstract_views import AbstractAuthenticatedView

from nti.app.orgsync.interfaces import ACT_VIEW_ACCOUNTS

from nti.externalization.externalization import to_external_object

from nti.orgsync.accounts.interfaces import IAccount

logger = __import__('logging').getLogger(__name__)


@view_config(route_name="objects.generic.traversal",
             renderer="rest",
             permission=ACT_VIEW_ACCOUNTS,
             context=IAccount,
             request_method="GET")
class AccountView(AbstractAuthenticatedView):

    def __call__(self):
        result = to_external_object(self.context)
        result.__name__ = self.request.view_name
        result.__parent__ = self.request.context
        return result
