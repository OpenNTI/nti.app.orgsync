#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import zope.i18nmessageid
MessageFactory = zope.i18nmessageid.MessageFactory(__name__)

#: OrgSync Path adapter
ORGSYNC = "orgsync"

#: Organizations Path adapter
ORGS = "orgs"

#: Accounts Path adapter
ACCOUNTS = "accounts"

#: Logs Path adapter
LOGS = "logs"

#: Sync view
SYNCHRONIZE = 'synchronize'

#: Last entry view
LAST_ENTRY = 'last_entry'

#: Snapshot view
SNAPSHOT = 'snapshot'

#: Snapshot view
SOONER_ID = 'SoonerID'

#: ID
ID = "id"

#: Account first_name
FIRST_NAME = "first_name"

#: Account last_name
LAST_NAME = "last_name"

#: Account Major
MAJOR = "Major"

#: Account 4x4
OUFBYF = "OU 4x4"

#: Organization keywords
KEYWORDS = "keywords"

#: Organization long name
LONG_NAME = "long_name"