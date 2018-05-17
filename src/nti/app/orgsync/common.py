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

from pyramid.threadlocal import get_current_request

from sqlalchemy.orm import aliased

from zope import component

from nti.coremetadata.interfaces import IRedisClient

from nti.orgsync_rdbms.accounts.alchemy import Account
from nti.orgsync_rdbms.accounts.alchemy import load_account
from nti.orgsync_rdbms.accounts.alchemy import get_account_profile_response
from nti.orgsync_rdbms.accounts.alchemy import get_account_profile_responses

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.orgsync_rdbms.organizations.alchemy import Organization
from nti.orgsync_rdbms.organizations.alchemy import load_organization

from nti.ou.orgsync_analysis import OUID

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


def query_filter_table(session, table, filters=None):
    query_obj = session.query(table).order_by(table.id)
    if filters:
        # Filter out any nonsense filter keywords
        org_cols = [col.key for col in table.__table__.columns]
        valid_filters = {k: v for k, v in filters.iteritems() if k in org_cols}
        # Chain filter commands on the query object for each filter
        for k, v in valid_filters.items():
            value = "%" + v + "%" 
            query_obj = query_obj.filter(getattr(table, k).like(value))
    return query_obj


def get_organization(org_id, db=None):
    db = component.getUtility(IOrgSyncDatabase) if db is None else db
    return load_organization(db, org_id)


def get_all_organizations(db=None, filters=None):
    result = []
    db = component.getUtility(IOrgSyncDatabase) if db is None else db
    session = getattr(db, 'session', db)
    organization = aliased(Organization)
    query_obj = query_filter_table(session, organization, filters)
    for row in query_obj.all():
        result.append(row)
    return result


def get_account(account_id, db=None):
    db = component.getUtility(IOrgSyncDatabase) if db is None else db
    return load_account(db, account_id)


def get_all_accounts(db=None, filters=None):
    result = []
    db = component.getUtility(IOrgSyncDatabase) if db is None else db
    session = getattr(db, 'session', db)
    account = aliased(Account)
    query_obj = query_filter_table(session, account, filters)
    for row in query_obj.all():
        result.append(row)
    return result


def get_account_ounetid(account, db=None):
    db = component.getUtility(IOrgSyncDatabase) if db is None else db
    return get_account_profile_response(db, account, OUID)


def get_account_profile(account, db=None):
    result = {}
    db = component.getUtility(IOrgSyncDatabase) if db is None else db
    responses = get_account_profile_responses(db, account)
    for resp in responses or ():
        name = resp.element.name
        if name:
            result[name] = resp.data
    return result


def get_ds2(request=None):
    request = request if request else get_current_request()
    try:
        result = request.path_info_peek() if request else None
    except AttributeError:  # in unit test we may see this
        result = None
    return result or "dataserver2"
