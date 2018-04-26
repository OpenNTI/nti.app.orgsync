#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class,no-value-for-parameter

from zope import interface

from zope.interface.interfaces import ObjectEvent
from zope.interface.interfaces import IObjectEvent

from zope.security.permission import Permission

from nti.appserver.workspaces.interfaces import IWorkspace

from nti.dataserver.authorization import ROLE_PREFIX

from nti.dataserver.authorization import StringRole

from nti.schema.field import ValidDatetime

#: The ID of a role for ourecomm
RID_ORGSYNC_PREFIX = ROLE_PREFIX + 'nti.dataserver.orgsync'
RID_ORGSYNC = StringRole(RID_ORGSYNC_PREFIX)

#: View orgs permission
ACT_VIEW_ORGS = Permission('nti.actions.orgsync.view_orgs')

#: View accounts permission
ACT_VIEW_ACCOUNTS = Permission('nti.actions.orgsync.view_accounts')

#: View logs permission
ACT_VIEW_LOGS = Permission('nti.actions.orgsync.view_logs')

#: Sync db permission
ACT_SYNC_DB = Permission('nti.actions.orgsync.sync_db')

#: Snapshot permission
ACT_SNAPSHOPT = Permission('nti.actions.orgsync.snapshot')


class IOrgSyncWorkspace(IWorkspace):
    """
    A workspace containing data for orgsync.
    """


class IOrgSyncSyncEvent(IObjectEvent):
    """
    An event that is sent, when the orgsync db is synchronized 
    """

    timestamp = ValidDatetime(title=u"The timestamp", 
                              required=True)

    start_date = ValidDatetime(title=u"Start date", 
                               required=False)

    end_date = ValidDatetime(title=u"Start date", 
                             required=False)


@interface.implementer(IOrgSyncSyncEvent)
class OrgSyncSyncEvent(ObjectEvent):

    def __init__(self, db, timestamp, start_date=None, end_date=None):
        super(OrgSyncSyncEvent, self).__init__(db)
        self.timestamp = timestamp
        self.start_date = start_date
        self.end_date = end_date
