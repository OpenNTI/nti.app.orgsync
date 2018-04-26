#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component

from nti.app.orgsync.interfaces import IOrgSyncSyncEvent

from nti.app.orgsync.snapshot import orgsync_source_snapshot

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

logger = __import__('logging').getLogger(__name__)


@component.adapter(IOrgSyncDatabase, IOrgSyncSyncEvent)
def on_orgsync_syncned(_, event):
    orgsync_source_snapshot(event.timestamp,
                            event.start_date,
                            event.end_date)
