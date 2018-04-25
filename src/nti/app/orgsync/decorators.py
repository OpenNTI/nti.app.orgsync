#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import component

from nti.app.orgsync.common import get_account_ounetid

from nti.externalization.singleton import Singleton

from nti.orgsync_rdbms.accounts.interfaces import IStorableAccount

from nti.orgsync_rdbms.organizations import ORGANIZATIONS

from nti.ou.analysis import OUNET_ID

logger = __import__('logging').getLogger(__name__)


@component.adapter(IStorableAccount)
class _AccountDecorator(Singleton):
    """
    Decorate an storable account
    """

    def decorateExternalObject(self, context, result):
        # add organizations
        orgs = result.setdefault(ORGANIZATIONS, [])
        for org in context.organizations or ():
            orgs.append(org.id)
        # add sooner id
        ounetid = get_account_ounetid(context)
        result['SoonerID'] = result[OUNET_ID] = ounetid
        return result
