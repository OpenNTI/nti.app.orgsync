#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component

from nti.orgsync.client import DEFAULT_TIMEOUT

from nti.orgsync.interfaces import IOrgSyncKey

from nti.orgsync_rdbms.database.interfaces import IOrgSyncDatabase

from nti.orgsync_rdbms.synchronize.synchronize import synchronize

def get_api_key():
    key = component.getUtility(IOrgSyncKey)
    return key.APIKey

def synchronize_orgsync(workers=1, timeout=DEFAULT_TIMEOUT):
    db = component.getUtility(IOrgSyncDatabase)
    key = get_api_key()
    successful_sync = True
    try:
        synchronize(key, db, workers=workers, timeout=timeout)
    except:
        successful_sync = False
    return successful_sync
