#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. $Id$
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from pyramid.view import view_config
from pyramid.view import view_defaults

from nti.app.orgsync.views import OrgSyncPathAdapter

from nti.app.spark.views import SPARK_JOB_ERROR
from nti.app.spark.views import SPARK_JOB_STATUS

from nti.app.spark.views.job_views import SparkJobErrorView
from nti.app.spark.views.job_views import SparkJobStatusView

from nti.dataserver.authorization import ACT_READ

logger = __import__('logging').getLogger(__name__)


@view_config(name=SPARK_JOB_STATUS)
@view_defaults(route_name="objects.generic.traversal",
               renderer="rest",
               request_method="GET",
               permission=ACT_READ,
               context=OrgSyncPathAdapter)
class JobStatusView(SparkJobStatusView):
    pass


@view_config(name=SPARK_JOB_ERROR)
@view_defaults(route_name="objects.generic.traversal",
               renderer="rest",
               request_method="GET",
               permission=ACT_READ,
               context=OrgSyncPathAdapter)
class JobErrorView(SparkJobErrorView):
    pass
