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

from zope.container.contained import Contained

from zope.location.interfaces import ILocation

from nti.app.orgsync import LOGS
from nti.app.orgsync import ORGS
from nti.app.orgsync import ORGSYNC
from nti.app.orgsync import ACCOUNTS
from nti.app.orgsync import SNAPSHOT
from nti.app.orgsync import LAST_ENTRY
from nti.app.orgsync import SYNCHRONIZE

from nti.app.orgsync.authorization import is_orsync_admin

from nti.app.orgsync.common import get_ds2

from nti.app.orgsync.interfaces import ACT_SYNC_DB
from nti.app.orgsync.interfaces import ACT_SNAPSHOPT
from nti.app.orgsync.interfaces import ACT_VIEW_LOGS
from nti.app.orgsync.interfaces import ACT_VIEW_ORGS
from nti.app.orgsync.interfaces import ACT_VIEW_ACCOUNTS

from nti.app.orgsync.interfaces import IOrgSyncWorkspace

from nti.appserver.pyramid_authorization import has_permission

from nti.appserver.workspaces.interfaces import IUserService

from nti.dataserver.interfaces import IDataserverFolder

from nti.links.links import Link

from nti.property.property import alias

logger = __import__('logging').getLogger(__name__)


@component.adapter(IDataserverFolder)
@interface.implementer(IOrgSyncWorkspace)
class _OrgSyncWorkspace(Contained):

    __name__ = ORGSYNC
    name = alias('__name__', __name__)

    def __init__(self, user_service):
        self.context = user_service
        self.user = user_service.user

    @property
    def collections(self):
        return ()

    @Lazy
    def root(self):
        return get_ds2()

    def create_link(self, name, elements=(), method='GET', rel=None):
        href = '/%s/%s/%s' % (self.root, ORGSYNC, name)
        link = Link(href, rel=rel or name, elements=elements,
                    method=method)
        link.__name__ = ''
        interface.alsoProvides(link, ILocation)
        return link

    @Lazy
    def is_orgsync_admin(self):
        return is_orsync_admin(self.user)

    @Lazy
    def can_view_logs(self):
        return is_orsync_admin(self.user) or has_permission(ACT_VIEW_LOGS, self)

    @Lazy
    def can_view_orgs(self):
        return is_orsync_admin(self.user) or has_permission(ACT_VIEW_ORGS, self)

    @Lazy
    def can_view_accounts(self):
        return is_orsync_admin(self.user) or has_permission(ACT_VIEW_ACCOUNTS, self)

    @Lazy
    def can_sync_db(self):
        return is_orsync_admin(self.user) or has_permission(ACT_SYNC_DB, self)

    @Lazy
    def can_snapshot_db(self):
        return is_orsync_admin(self.user) or has_permission(ACT_SNAPSHOPT, self)

    @property
    def links(self):
        result = []
        if self.can_view_logs:
            result.append(self.create_link(LOGS))
            result.append(self.create_link(LOGS, rel=LAST_ENTRY,
                                           elements=('@@' + LAST_ENTRY,)))
        if self.can_view_orgs:
            result.append(self.create_link(ORGS))
        if self.can_view_accounts:
            result.append(self.create_link(ACCOUNTS))
        if self.can_sync_db:
            result.append(self.create_link(SYNCHRONIZE, method='POST'))
        if self.can_snapshot_db:
            result.append(self.create_link(SNAPSHOT, method='POST'))
        return result


@component.adapter(IUserService)
@interface.implementer(IOrgSyncWorkspace)
def OrgSyncWorkspace(user_service):
    workspace = _OrgSyncWorkspace(user_service)
    workspace.__parent__ = user_service.__parent__
    return workspace
