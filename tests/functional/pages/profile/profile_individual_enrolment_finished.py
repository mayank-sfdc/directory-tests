# -*- coding: utf-8 -*-
"""Profile - Individual enrolment finished"""

from requests import Response

from tests import URLs
from tests.functional.pages import Services
from tests.functional.utils.request import check_response, check_url

SERVICE = Services.PROFILE
NAME = "Individual enrolment (finished)"
TYPE = "confirmation"
URL = URLs.PROFILE_ENROL_INDIVIDUAL_FINISHED.absolute
EXPECTED_STRINGS = [
    "Your account has been created",
    "You can now",
    "find export opportunities",
    "sell online overseas",
    "find events and visits",
]


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)