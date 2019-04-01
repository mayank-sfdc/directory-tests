# -*- coding: utf-8 -*-
"""SSO - SUD (Profile) Find A Buyer page"""
import logging

from requests import Response, Session
from tests import get_absolute_url
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url("profile:fab")
EXPECTED_STRINGS = [
    "Account",
    "You are signed in as",
    "Export opportunities",
    "Business profile",
    "Selling online overseas",
    "Get a business profile",
    "Get a business profile for your company and you can",
    "generate new sales leads",
    "promote your business to thousands of overseas buyers",
    "add case studies of your best work to make your company stand out",
    "have buyers contact your sales team directly to get deals moving",
    "Create a business profile",
]

EXPECTED_STRINGS_AS_LOGGED_IN_USER = [
    "Account",
    "You are signed in as",
    "Export opportunities",
    "Business profile",
    "Selling online overseas",
    "About",
    "Add a case study",
    "Add a logo",
]

MANAGE_USER_ACCOUNTS_STRINGS = [
    "Admin tools", "Admin view"
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response, *, as_logged_in_user: bool = False):
    if as_logged_in_user:
        check_response(
            response, 200, body_contains=EXPECTED_STRINGS_AS_LOGGED_IN_USER
        )
    else:
        check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SUD (Profile) Find A Buyer page")


def should_see_options_to_manage_users(response: Response):
    check_response(response, 200, body_contains=MANAGE_USER_ACCOUNTS_STRINGS)
    logging.debug("User can see options to control FAB profile user accounts")


def should_not_see_options_to_manage_users(response: Response):
    check_response(
        response, 200, unexpected_strings=MANAGE_USER_ACCOUNTS_STRINGS
    )
    logging.debug("User can't see options to manage FAB profile user accounts")
