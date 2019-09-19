# -*- coding: utf-8 -*-
"""Profile - Enrolment finished"""

from requests import Response, Session

from directory_tests_shared import URLs
from tests.functional.pages import Services
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.PROFILE
NAME = "Enrolment (finished)"
TYPE = "confirmation"
URL = URLs.PROFILE_ENROL_FINISHED.absolute
EXPECTED_STRINGS = [
    "Your account has been created",
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
