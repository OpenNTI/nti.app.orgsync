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

from nti.orgsync.accounts.client import Client as AccountClient

from nti.orgsync.organizations.client import Client as OrgClient

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
    except AlreadyAcquired:  # pragma: no cover
        pass
    return result


def get_organization(org_id, apiKey=None):
    client = OrgClient(apiKey)
    return client.get_organization(org_id)


def get_account(account_id, apiKey=None):
    client = AccountClient(apiKey)
    return client.get_account(account_id)
