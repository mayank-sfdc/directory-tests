# -*- coding: utf-8 -*-
"""SSO - SUD (Profile) Export Opportunities page"""
import logging

from requests import Response, Session

from tests import URLs
from tests.functional.pages import Services
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.PROFILE
NAME = "Export Opportunities"
TYPE = "landing"
URL = URLs.PROFILE_EXOPS_APPLICATIONS.absolute
EXPECTED_STRINGS = [
    "Account",
    "You are signed in as",
    "Export opportunities",
    "Business profile",
    "Selling online overseas",
    "Applications",
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug(
        "Successfully got to the SUD (Profile) Export Opportunities page"
    )
