#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid import httpexceptions as hexc

from zope import interface

from zope.cachedescriptors.property import Lazy

from zope.location.interfaces import IContained

from zope.traversing.interfaces import IPathAdapter

from nti.app.orgsync import LOGS
from nti.app.orgsync import ORGS
from nti.app.orgsync import ORGSYNC
from nti.app.orgsync import ACCOUNTS

from nti.app.orgsync.interfaces import RID_ORGSYNC

from nti.app.orgsync.common import get_account
from nti.app.orgsync.common import get_organization

from nti.dataserver.authorization import ROLE_ADMIN

from nti.dataserver.authorization_acl import ace_allowing
from nti.dataserver.authorization_acl import acl_from_aces

from nti.dataserver.interfaces import ALL_PERMISSIONS

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IPathAdapter, IContained)
class PathAdapterMixin(object):

    __name__ = None

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context

    @Lazy
    def __acl__(self):
        aces = [
            ace_allowing(ROLE_ADMIN, ALL_PERMISSIONS, type(self)),
            ace_allowing(RID_ORGSYNC, ALL_PERMISSIONS, type(self)),
        ]
        acl = acl_from_aces(aces)
        return acl


class OrgSyncPathAdapter(PathAdapterMixin):
    __name__ = ORGSYNC


class OrgsPathAdapter(PathAdapterMixin):

    __name__ = ORGS

    def __getitem__(self, key):
        if key:
            result = get_organization(key)
            if result is not None:
                return result
        raise KeyError(key) if key else hexc.HTTPNotFound()


class AccountsPathAdapter(PathAdapterMixin):

    __name__ = ACCOUNTS

    def __getitem__(self, key):
        if key:
            result = get_account(key)
            if result is not None:
                return result
        raise KeyError(key) if key else hexc.HTTPNotFound()


class LogsPathAdapter(PathAdapterMixin):
    __name__ = LOGS
