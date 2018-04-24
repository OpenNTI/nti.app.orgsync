#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component
from zope import interface

from zope.cachedescriptors.property import Lazy

from nti.app.orgsync.interfaces import RID_ORGSYNC

from nti.dataserver.authorization import ROLE_ADMIN

from nti.dataserver.authorization_acl import ace_allowing
from nti.dataserver.authorization_acl import acl_from_aces

from nti.dataserver.interfaces import ACE_DENY_ALL
from nti.dataserver.interfaces import ALL_PERMISSIONS

from nti.dataserver.interfaces import IACLProvider

from nti.orgsync.accounts.interfaces import IAccount

from nti.orgsync.entries.interfaces import IMembershipLog

from nti.orgsync.organizations.interfaces import IOrganization

from nti.orgsync_rdbms.accounts.interfaces import IStorableAccount

from nti.orgsync_rdbms.entries.interfaces import IStorableMembershipLog

from nti.orgsync_rdbms.organizations.interfaces import IStorableOrganization

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IACLProvider)
class _ACLProviderMixin(object):

    def __init__(self, context):
        self.context = context

    @Lazy
    def __acl__(self):
        aces = [
            ace_allowing(ROLE_ADMIN, ALL_PERMISSIONS, type(self)),
            ace_allowing(RID_ORGSYNC, ALL_PERMISSIONS, type(self)),
        ]
        aces.append(ACE_DENY_ALL)
        acl = acl_from_aces(aces)
        return acl


@component.adapter(IOrganization)
class _OrgACLProvider(_ACLProviderMixin):
    pass


@component.adapter(IStorableOrganization)
class _StorableOrgACLProvider(_ACLProviderMixin):
    pass


@component.adapter(IAccount)
class _AccountACLProvider(_ACLProviderMixin):
    pass


@component.adapter(IStorableAccount)
class _StorableAccountACLProvider(_ACLProviderMixin):
    pass


@component.adapter(IMembershipLog)
class _MembershipLogACLProvider(_ACLProviderMixin):
    pass


@component.adapter(IStorableMembershipLog)
class _StorableMembershipLogACLProvider(_ACLProviderMixin):
    pass
