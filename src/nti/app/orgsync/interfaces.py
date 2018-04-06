#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=inherit-non-class,no-value-for-parameter

from zope.security.permission import Permission

from nti.dataserver.authorization import ROLE_PREFIX

from nti.dataserver.authorization import StringRole

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
