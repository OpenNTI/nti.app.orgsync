#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from redis_lock import Lock as RedisLock

from zope import component

from nti.coremetadata.interfaces import IRedisClient

#: Lock expire time 1.5(hr)
DEFAULT_LOCK_EXPIRY_TIME = 5400

logger = __import__('logging').getLogger(__name__)


def redis_client():
    return component.queryUtility(IRedisClient)


def get_redis_lock(name, expire=DEFAULT_LOCK_EXPIRY_TIME, strict=False):
    return RedisLock(redis_client(), name, expire, strict=strict)
