#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from zope import interface

from zope.location.interfaces import IContained

from zope.traversing.interfaces import IPathAdapter

from nti.app.orgsync import ORGSYNC

logger = __import__('logging').getLogger(__name__)


@interface.implementer(IPathAdapter, IContained)
class OrgSyncPathAdapter(object):

    __name__ = ORGSYNC

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.__parent__ = context
