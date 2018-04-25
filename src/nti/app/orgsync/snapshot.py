#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import time

from zope import component

from nti.app.spark.common import get_redis_lock
from nti.app.spark.common import is_locked_held

from nti.app.spark.runner import queue_job

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.orgsync_spark.snapshot import snapshot as db_snapshot

#: snapshot lock name
SNAPSHOT_LOCK = '++etc++orgsync++snapshot++lock'

logger = __import__('logging').getLogger(__name__)


def get_snapshot_lock():
    return get_redis_lock(SNAPSHOT_LOCK)


def is_snapshot_lock_held():
    return is_locked_held(SNAPSHOT_LOCK)


def orgsync_source_snapshot(timestamp, start_date=None, end_date=None,
                            logs=False, archive=True):
    with get_snapshot_lock():
        timestamp = time.mktime(timestamp.timetuple())
        database = component.getUtility(IOrgSyncDatabase)
        db_snapshot(database, timestamp, start_date, end_date, logs, archive)


def create_orgsync_source_snapshot_job(creator, timestamp, start_date=None,
                                       end_date=None, logs=False, archive=True):
    return queue_job(creator,
                     orgsync_source_snapshot,
                     args=(timestamp, start_date, end_date, logs, archive))
