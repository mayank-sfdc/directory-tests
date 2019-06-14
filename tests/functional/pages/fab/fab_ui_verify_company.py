# -*- coding: utf-8 -*-
"""FAB - Verify Company page"""
import logging

from requests import Response, Session

from tests import URLs
from tests.functional.pages import Services
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.FAB
NAME = "Verify company"
TYPE = "form"
URL = URLs.FAB_CONFIRM_COMPANY_ADDRESS.absolute
EXPECTED_STRINGS = [
    "Verify your company",
    "Enter the 12 digit code from the letter that was sent to",
    "Sign in with Companies House",
    "Alternatively you can sign in to Companies House to verify",
    (
        "You will need your Companies House authentication code and the email and"
        " password you use to sign in"
    ),
]

EXPECTED_STRINGS_VERIFIED = [
    "Your company has been verified",
]


def go_to(session: Session, *, referer: str = None) -> Response:
    referer = referer or URLs.FAB_COMPANY_PROFILE.absolute
    headers = {"Referer": referer}
    return make_request(Method.GET, URL, session=session, headers=headers)


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Supplier is on the Verify Company page")


def submit(
    session: Session,
    token: str,
    verification_code: str,
    *,
    referer: str = None
) -> Response:
    """Submit the form with verification code."""
    if referer is None:
        referer = URLs.FAB_COMPANY_PROFILE.absolute
    headers = {"Referer": referer}
    data = {
        "csrfmiddlewaretoken": token,
        "company_address_verification_view-current_step": "address",
        "address-code": verification_code,
    }
    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )


def should_see_company_is_verified(response: Response):
    """Check is Supplier was told that the company has been verified"""
    check_response(response, 200, body_contains=EXPECTED_STRINGS_VERIFIED)
    logging.debug("Supplier is on the Verify Company page")


def view_or_amend_profile(session: Session) -> Response:
    """Simulate clicking on the 'View or amend your company profile' link."""
    headers = {"Referer": URL}
    url = URLs.FAB_COMPANY_PROFILE.absolute
    return make_request(Method.GET, url, session=session, headers=headers)
