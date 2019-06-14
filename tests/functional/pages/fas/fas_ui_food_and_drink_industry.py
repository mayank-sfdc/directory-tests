# -*- coding: utf-8 -*-
"""FAS - Food and Drink Industry page"""
import logging

from requests import Response, Session

from tests import URLs
from tests.functional.pages import Services
from tests.functional.utils.request import (
    Method,
    check_response,
    check_url,
    make_request,
)

SERVICE = Services.FAS
NAME = "Food and drink"
TYPE = "industry"
URL = URLs.FAS_INDUSTRY_FOOD_AND_DRINK.absolute
EXPECTED_STRINGS = [
    "Why choose UK food and drink",
    "Innovative products",
    "Quality research",
    "Healthy eating",
]


def go_to(session: Session) -> Response:
    headers = {"Referer": URLs.FAS_INDUSTRIES.absolute}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response):
    check_url(response, URL)
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on FAS Food and Drink Industry page")
