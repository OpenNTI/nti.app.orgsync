#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from datetime import datetime

from zope.component import getUtility

from zope.event import notify

from nti.app.orgsync.common import get_redis_lock
from nti.app.orgsync.common import is_locked_held

from nti.app.orgsync.interfaces import OrgSyncSyncEvent

from nti.app.spark.runner import queue_job

from nti.orgsync.client import DEFAULT_TIMEOUT
from nti.orgsync.client import DEFAULT_MAX_WORKERS

from nti.orgsync.interfaces import IOrgSyncKey

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.orgsync_rdbms.synchronize.synchronize import process_classifications
from nti.orgsync_rdbms.synchronize.synchronize import process_membership_logs

#: Orgsync sync lock name
SYNC_ORGSYNC_LOCK = '++etc++orgsync++sync++lock'

logger = __import__('logging').getLogger(__name__)


def is_sync_lock_held():
    return is_locked_held(SYNC_ORGSYNC_LOCK)


def synchronize_orgsync(start_date=None, end_date=None,
                        workers=DEFAULT_MAX_WORKERS,
                        timeout=DEFAULT_TIMEOUT):
    with get_redis_lock(SYNC_ORGSYNC_LOCK):
        key = getUtility(IOrgSyncKey)
        db = getUtility(IOrgSyncDatabase)
        # always process classifications
        process_classifications(key, db, timeout=timeout)
        # membership logs sync orgs and accounts
        result = process_membership_logs(key, db,
                                         end_date=end_date,
                                         start_date=start_date,
                                         workers=workers, timeout=timeout)
        if result:  # notify if there are logs
            notify(OrgSyncSyncEvent(db, datetime.now(), start_date, end_date))
        return result


def create_orgsync_sync_job(creator, start_date=None, end_date=None,
                            workers=DEFAULT_MAX_WORKERS):
    return queue_job(creator,
                     synchronize_orgsync,
                     args=(start_date, end_date, workers))
