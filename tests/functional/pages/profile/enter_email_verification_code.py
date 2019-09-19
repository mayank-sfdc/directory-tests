# -*- coding: utf-8 -*-
"""Profile - Enter your email verification code"""

from requests import Response, Session

from directory_tests_shared import URLs
from tests.functional.pages import Services
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.PROFILE
NAME = "Enter email verification code"
TYPE = "form"
URL = URLs.PROFILE_ENROL_EMAIL_VERIFICATION.absolute
EXPECTED_STRINGS = [
    "Enter your confirmation code",
]


def go_to(session: Session) -> Response:
    return make_request(Method.GET, URL, session=session)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def submit(actor: Actor) -> Response:
    session = actor.session
    assert actor.email_confirmation_code
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "companies_house_enrolment_view-current_step": "verification",
        "verification-code": actor.email_confirmation_code,
    }

    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )
