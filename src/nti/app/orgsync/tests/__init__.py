#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

from zope import component

from nti.app.testing.application_webtest import ApplicationTestLayer


class NoOpCM(object):

    def __enter__(self):
        pass

    def __exit__(self, t, v, tb):
        pass


class OrgSyncApplicationTestLayer(ApplicationTestLayer):
    pass
