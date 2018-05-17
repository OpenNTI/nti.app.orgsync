#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid.interfaces import IRequest

from zope import component
from zope import interface

from nti.app.orgsync import ORGSYNC
from nti.app.orgsync import ACCOUNTS
from nti.app.orgsync import SOONER_ID

from nti.app.orgsync.common import get_ds2
from nti.app.orgsync.common import get_account_ounetid

from nti.app.renderers.decorators import AbstractAuthenticatedRequestAwareDecorator

from nti.appserver.pyramid_authorization import has_permission

from nti.dataserver.authorization import ACT_READ

from nti.externalization.interfaces import StandardExternalFields
from nti.externalization.interfaces import IExternalObjectDecorator

from nti.externalization.singleton import Singleton

from nti.links.links import Link

from nti.orgsync_rdbms.accounts.interfaces import IStorableAccount

from nti.orgsync_rdbms.organizations import ORGANIZATIONS

from nti.ou.analysis import OUNET_ID

LINKS = StandardExternalFields.LINKS

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
        result[SOONER_ID] = result[OUNET_ID] = ounetid
        return result


@component.adapter(IStorableAccount, IRequest)
@interface.implementer(IExternalObjectDecorator)
class _AccountsLinkDecorator(AbstractAuthenticatedRequestAwareDecorator):
    """
    Decorate an account
    """

    def _predicate(self, context, unused_result):
        # pylint: disable=too-many-function-args
        return bool(self.authenticated_userid) \
           and has_permission(ACT_READ, context, self.request)

    def _do_decorate_external(self, context, result):
        account_id = str(context.id)
        links = result.setdefault(LINKS, [])
        href = '/%s/%s/%s' % (get_ds2(self.request), ORGSYNC, ACCOUNTS)
        for name in ('profile',):
            link = Link(href, rel=name, elements=(account_id, name),
                        method='GET')
            links.append(link)
