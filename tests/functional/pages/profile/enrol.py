# -*- coding: utf-8 -*-
"""Profile - Enrol - Create an account"""

from requests import Response, Session

from directory_tests_shared import PageType, Service, URLs
from tests.functional.utils.request import (
    Method,
    check_response,
    check_url,
    make_request,
)

SERVICE = Service.PROFILE
NAME = "Enrol"
TYPE = PageType.LANDING
URL = URLs.PROFILE_ENROL.absolute
EXPECTED_STRINGS = [
    "Create an ",
    "Start now",
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_url(response, URL, startswith=True)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
