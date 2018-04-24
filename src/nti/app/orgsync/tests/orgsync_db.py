#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

# pylint: disable=protected-access,too-many-public-methods,arguments-differ

import os
import codecs

import simplejson

from nti.orgsync.accounts.utils import parse_account_source

from nti.orgsync.classifications.utils import parse_classification_source

from nti.orgsync.entries.utils import membershiplog_object_hook
from nti.orgsync.entries.utils import parse_membership_log_from_external

from nti.orgsync.organizations.utils import parse_organization_source

from nti.orgsync_rdbms.accounts.alchemy import Account
from nti.orgsync_rdbms.accounts.alchemy import load_accounts

from nti.orgsync_rdbms.classifications.alchemy import Classification
from nti.orgsync_rdbms.classifications.alchemy import load_classifications

from nti.orgsync_rdbms.entries.alchemy import load_membership_logs

from nti.orgsync_rdbms.groups.alchemy import Group
from nti.orgsync_rdbms.groups.alchemy import load_groups
from nti.orgsync_rdbms.groups.alchemy import load_group_accounts

from nti.orgsync_rdbms.organizations.alchemy import Organization
from nti.orgsync_rdbms.organizations.alchemy import load_organization_groups
from nti.orgsync_rdbms.organizations.alchemy import load_organizations_and_profile_responses

from nti.orgsync_rdbms.synchronize.synchronize import do_organizations_load
from nti.orgsync_rdbms.synchronize.synchronize import do_postprocess_accounts


def get_organizations():
    path = os.path.join(os.path.dirname(__file__),
                        'data', 'organization.json')
    with codecs.open(path, "r", "UTF-8") as fp:
        return [parse_organization_source(fp)]


def get_accounts():
    path = os.path.join(os.path.dirname(__file__),
                        'data', 'account.json')
    with codecs.open(path, "r", "UTF-8") as fp:
        return [parse_account_source(fp)]


def get_classifications():
    path = os.path.join(os.path.dirname(__file__),
                        'data', 'classification.json')
    with codecs.open(path, "r", "UTF-8") as fp:
        return [parse_classification_source(fp)]


def get_membership_logs():
    path = os.path.join(os.path.dirname(__file__), 'data',
                        "membership_log.json")
    with codecs.open(path, "r", "UTF-8") as fp:
        data = membershiplog_object_hook(simplejson.load(fp))
        return [parse_membership_log_from_external(data)]


def postprocess_organizations(db, organizations=()):
    profile_responses = {}
    for org in organizations or ():
        load_groups(db, org.groups)
        for group in org.groups or ():
            load_group_accounts(db, group, group.account_ids)
        load_organization_groups(db, org, org.groups)
        profile_responses[org.id] = org.profile_responses
    load_organizations_and_profile_responses(db, profile_responses)


def postprocess_accounts(db, accounts=()):
    do_postprocess_accounts(db, accounts)


def synchronize(db):
    accounts = get_accounts()
    organizations = get_organizations()
    classifications = get_classifications()
    membership_logs = get_membership_logs()
    # create classifications
    load_classifications(db, classifications)
    # create organizations
    do_organizations_load(db, organizations)
    # create accounts
    load_accounts(db, accounts)
    # post process organizations
    postprocess_organizations(db, organizations)
    # post process accounts
    postprocess_accounts(db, accounts)
    # load logs
    load_membership_logs(db, membership_logs)


def drop(db):
    session = getattr(db, "session", db)
    session.query(Account).delete()
    session.query(Organization).delete()
    session.query(Classification).delete()
    session.query(Group).delete()
