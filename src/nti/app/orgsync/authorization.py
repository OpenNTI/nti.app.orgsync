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

from nti.app.orgsync.interfaces import RID_ORGSYNC

from nti.dataserver.interfaces import IUser
from nti.dataserver.interfaces import IGroupMember

logger = __import__('logging').getLogger(__name__)


@component.adapter(IUser)
@interface.implementer(IGroupMember)
class NextthoughtDotComOUOrgSyncAdmin(object):

    def __init__(self, context):
        groups = ()
        if context.username.endswith('@nextthought.com'):
            groups = (RID_ORGSYNC,)
        self.groups = groups


def is_orsync_admin(user):
    """
    Returns whether the user has the `RID_ORGSYNC` role.
    """
    for _, adapter in component.getAdapters((user,), IGroupMember):
        if adapter.groups and RID_ORGSYNC in adapter.groups:
            return True
    return False
