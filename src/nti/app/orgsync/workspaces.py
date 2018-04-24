#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid.threadlocal import get_current_registry

from zope import component
from zope import interface

from zope.cachedescriptors.property import Lazy

from zope.container.contained import Contained

from zope.location.interfaces import ILocation

from nti.app.orgsync import LOGS
from nti.app.orgsync import ORGS
from nti.app.orgsync import ORGSYNC
from nti.app.orgsync import ACCOUNTS

from nti.app.orgsync.authorization import is_orsync_admin

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
        request = get_current_registry()
        try:
            result = request.path_info_peek() if request else None
        except AttributeError:  # in unit test we may see this
            result = None
        root = result or "dataserver2"
        return root

    def create_link(self, name):
        href = '/%s/%s/%s' % (self.root, ORGSYNC, name)
        link = Link(href, rel=name, elements=())
        link.__name__ = ''
        interface.alsoProvides(link, ILocation)
        return link

    @Lazy
    def is_orgsync_admin(self):
        return is_orsync_admin(self.user)

    @property
    def links(self):
        result = []
        if self.is_orgsync_admin or has_permission(ACT_VIEW_LOGS, self):
            result.append(self.create_link(LOGS))
        if self.is_orgsync_admin or has_permission(ACT_VIEW_ORGS, self):
            result.append(self.create_link(ORGS))
        if self.is_orgsync_admin or has_permission(ACT_VIEW_ACCOUNTS, self):
            result.append(self.create_link(ACCOUNTS))
        return result


@component.adapter(IUserService)
@interface.implementer(IOrgSyncWorkspace)
def OrgSyncWorkspace(user_service):
    workspace = _OrgSyncWorkspace(user_service)
    workspace.__parent__ = workspace.user
    return workspace
