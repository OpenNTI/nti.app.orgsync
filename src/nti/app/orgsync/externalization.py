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

from nti.externalization.interfaces import IExternalObject
from nti.externalization.interfaces import LocatedExternalDict
from nti.externalization.interfaces import StandardExternalFields
from nti.externalization.interfaces import StandardInternalFields

from nti.orgsync.accounts import ACCOUNT_MIMETYPE

from nti.orgsync.accounts.interfaces import IAccount

from nti.orgsync.entries import MEMBERSHIP_LOG_MIMETYPE

from nti.orgsync.entries.interfaces import IMembershipLog

from nti.orgsync.organizations import ORG_MIMETYPE

from nti.orgsync.organizations.interfaces import IOrganization

from nti.orgsync_rdbms.accounts.interfaces import IStorableAccount

from nti.orgsync_rdbms.accounts.alchemy import IGNORE as ACCT_IGNORE

from nti.orgsync_rdbms.entries.interfaces import IStorableMembershipLog

from nti.orgsync_rdbms.organizations.alchemy import IGNORE as ORG_IGNORE

from nti.orgsync_rdbms.organizations.interfaces import IStorableOrganization

ID = StandardInternalFields.ID
MIMETYPE = StandardExternalFields.MIMETYPE

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IExternalObject)
class _StorableExternal(object):
    
    IGNORE = ()
    interface = ()
    mimeType = None

    def __init__(self, context):
        self.context = context

    def toExternalObject(self, **unused_kwargs):
        result = LocatedExternalDict()
        result[ID] = self.context.id
        result[MIMETYPE] = self.mimeType
        for name in self.interface:
            if name not in self.IGNORE:
                result[name] = getattr(self.context, name, None)
        return result


@component.adapter(IStorableOrganization)
class _OrganizationExternal(_StorableExternal):
    IGNORE = ORG_IGNORE
    mimeType = ORG_MIMETYPE
    interface = IOrganization


@component.adapter(IStorableAccount)
class _AccountExternal(_StorableExternal):
    IGNORE = ACCT_IGNORE
    interface = IAccount
    mimeType = ACCOUNT_MIMETYPE


@component.adapter(IStorableMembershipLog)
class _MembershipLogExternal(_StorableExternal):
    interface = IMembershipLog
    mimeType = MEMBERSHIP_LOG_MIMETYPE
