#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from requests.structures import CaseInsensitiveDict

from pyramid import httpexceptions as hexc

from pyramid.view import view_config
from pyramid.view import view_defaults

from nti.app.base.abstract_views import AbstractAuthenticatedView

from nti.app.externalization.error import raise_json_error

from nti.app.externalization.view_mixins import ModeledContentUploadRequestUtilsMixin

from nti.app.orgsync import MessageFactory as _

from nti.app.orgsync.sync import synchronize_orgsync

from nti.app.orgsync.views import OrgSyncPathAdapter

from nti.dataserver import authorization as nauth

from nti.orgsync.client import DEFAULT_TIMEOUT

@view_config(name="sync")
@view_defaults(route_name="objects.generic.traversal",
               renderer="rest",
               permission=nauth.ACT_NTI_ADMIN,
               context=OrgSyncPathAdapter,
               request_method="POST")
class OrgSyncSyncView(AbstractAuthenticatedView,
                      ModeledContentUploadRequestUtilsMixin):

    def readInput(self, value=None):  # pragma: no cover
        result = None
        if self.request.body:
            result = super(OrgSyncSyncView, self).readInput(value)
        return CaseInsensitiveDict(result or {})

    def __call__(self):
        data = self.readInput()
        workers = data.get('workers') or 1
        timeout = data.get('timeout') or DEFAULT_TIMEOUT
        if not synchronize_orgsync(workers, timeout):
            raise_json_error(self.request,
                                 hexc.HTTPUnprocessableEntity,
                                 {
                                     'message': _(u"Could not complete OrgSync synchronization."),
                                     'code': 'SynchronizationError',
                                 },
                                 None)
        return hexc.HTTPOk()
