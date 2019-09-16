# -*- coding: utf-8 -*-
"""Profile - Enter your personal details"""

from requests import Response

from tests import URLs
from tests.functional.pages import Services
from tests.functional.utils.context_utils import Actor
from tests.functional.utils.request import (
    Method,
    check_response,
    check_url,
    make_request,
)

SERVICE = Services.PROFILE
NAME = "Enter your individual details"
TYPE = "form"
URL = URLs.PROFILE_ENROL_INDIVIDUAL_ENTER_YOUR_PERSONAL_DETAILS.absolute
EXPECTED_STRINGS = [
    "Enter your personal details",
    "First name",
    "Last name",
    "Job title",
    "Phone number (optional)",
]


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)


def submit(actor: Actor):
    session = actor.session
    headers = {"Referer": URL}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "individual_user_enrolment_view-current_step": "personal-details",
        "personal-details-given_name": actor.alias,
        "personal-details-family_name": "AUTOMATED TESTS",
        "personal-details-job_title": "DIT AUTOMATED TESTS",
        "personal-details-phone_number": "0987654321",
    }

    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )
