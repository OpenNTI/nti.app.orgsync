#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid.threadlocal import get_current_request

from redis_lock import AlreadyAcquired
from redis_lock import Lock as RedisLock

from sqlalchemy import sql

from sqlalchemy.orm import aliased

from zope import component

from nti.app.orgsync import ORGS
from nti.app.orgsync import ORGSYNC
from nti.app.orgsync import ACCOUNTS
from nti.app.orgsync import SOONER_ID

from nti.coremetadata.interfaces import IRedisClient

from nti.externalization.interfaces import LocatedExternalDict

from nti.orgsync_rdbms.accounts.alchemy import Account
from nti.orgsync_rdbms.accounts.alchemy import load_account
from nti.orgsync_rdbms.accounts.alchemy import get_account_profile_response
from nti.orgsync_rdbms.accounts.alchemy import get_account_profile_responses
from nti.orgsync_rdbms.accounts.alchemy import get_accounts_like_profile_response

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.orgsync_rdbms.organizations.alchemy import Organization
from nti.orgsync_rdbms.organizations.alchemy import load_organization

from nti.ou.analysis import OUNET_ID

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
        org_cols = {col.key for col in table.__table__.columns}
        valid_filters = {k: v for k, v in filters.items() if k in org_cols}
        # Chain filter commands on the query object for each filter
        for k, v in valid_filters.items():
            value = "%" + "%s" % v + "%"
            query_obj = query_obj.filter(getattr(table, k).like(value))
        # if no valid filters
        if not valid_filters:
            query_obj = session.query(table).filter(sql.false())
    return query_obj


def get_organization(org_id, db=None):
    db = component.getUtility(IOrgSyncDatabase) if db is None else db
    return load_organization(db, org_id)


def get_all_organizations(db=None, filters=None):
    db = component.getUtility(IOrgSyncDatabase) if db is None else db
    session = getattr(db, 'session', db)
    organization = aliased(Organization)
    query_obj = query_filter_table(session, organization, filters)
    result = query_obj.all()
    return result


def get_account(account_id, db=None):
    db = component.getUtility(IOrgSyncDatabase) if db is None else db
    return load_account(db, account_id)


def get_all_accounts(db=None, filters=None):
    db = component.getUtility(IOrgSyncDatabase) if db is None else db
    session = getattr(db, 'session', db)
    account = aliased(Account)
    # query table
    if filters:
        query_obj = query_filter_table(session, account, filters)
        result = {row for row in query_obj.all()}
        # check for sooner id
        if SOONER_ID in filters or OUNET_ID in filters:
            v = filters.get(SOONER_ID) or filters.get(OUNET_ID)
            value = "%" + "%s" % v + "%"
            result.update(get_accounts_like_profile_response(db, OUID, value))
        result = sorted(result)
    else:
        query_obj = session.query(account).order_by(account.id)
        result = query_obj.all()
    return result


def get_account_ounetid(account, db=None):
    db = component.getUtility(IOrgSyncDatabase) if db is None else db
    return get_account_profile_response(db, account, OUID)


def get_account_profile(account, db=None):
    result = LocatedExternalDict()
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


def get_accounts_href(request=None):
    root = get_ds2(request)
    return '/%s/%s/%s' % (root, ORGSYNC, ACCOUNTS)


def get_account_ref(account, request=None):
    aid = getattr(account, "id", account)
    href = get_accounts_href(request)
    return "%s/%s" % (href, aid)


def get_orgs_href(request=None):
    root = get_ds2(request)
    return '/%s/%s/%s' % (root, ORGSYNC, ORGS)


def get_org_href(org, request=None):
    oid = getattr(org, "id", org)
    href = get_orgs_href(request)
    return "%s/%s" % (href, oid)
