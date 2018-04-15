#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from redis_lock import AlreadyAcquired
from redis_lock import Lock as RedisLock

from zope import component

from nti.coremetadata.interfaces import IRedisClient

from nti.orgsync_rdbms.accounts.alchemy import load_account

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.orgsync_rdbms.organizations.alchemy import load_organization

#: Lock expire time 1.5(hr)
DEFAULT_LOCK_EXPIRY_TIME = 5400

logger = __import__('logging').getLogger(__name__)


def redis_client():
    return component.queryUtility(IRedisClient)


def get_redis_lock(name, expire=DEFAULT_LOCK_EXPIRY_TIME, strict=False):
    return RedisLock(redis_client(), name, expire, strict=strict)


def is_locked_held(name):
    result = True
    lock = get_redis_lock(name)
    try:
        if lock.acquire(False):
            lock.release()
            result = False
    except AlreadyAcquired:
        pass
    return result


def get_organization(org_id, db=None):
    db = component.getUtility(IOrgSyncDatabase) if db is None else db
    return load_organization(db, org_id)


def get_account(account_id, db=None):
    db = component.getUtility(IOrgSyncDatabase) if db is None else db
    return load_account(db, account_id)
