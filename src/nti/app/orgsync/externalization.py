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

from nti.orgsync.organizations import ORG_MIMETYPE

from nti.orgsync.organizations.interfaces import IOrganization

from nti.orgsync_rdbms.accounts.interfaces import IStorableAccount

from nti.orgsync_rdbms.accounts.alchemy import IGNORE as ACCT_IGNORE

from nti.orgsync_rdbms.organizations.alchemy import IGNORE as ORG_IGNORE

from nti.orgsync_rdbms.organizations.interfaces import IStorableOrganization

ID = StandardInternalFields.ID
MIMETYPE = StandardExternalFields.MIMETYPE

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IExternalObject)
@component.adapter(IStorableOrganization)
class _OrganizationExternal(object):

    def __init__(self, org):
        self.org = org

    def toExternalObject(self, **unused_kwargs):
        result = LocatedExternalDict()
        result[ID] = self.org.id
        result[MIMETYPE] = ORG_MIMETYPE
        for name in IOrganization:
            if name not in ORG_IGNORE:
                result[name] = getattr(self.org, name, None)
        return result


@component.adapter(IStorableAccount)
@interface.implementer(IExternalObject)
class _AccountExternal(object):

    def __init__(self, context):
        self.context = context

    def toExternalObject(self, **unused_kwargs):
        result = LocatedExternalDict()
        result[ID] = self.context.id
        result[MIMETYPE] = ACCOUNT_MIMETYPE
        for name in IAccount:
            if name not in ACCT_IGNORE:
                result[name] = getattr(self.context, name, None)
        return result
