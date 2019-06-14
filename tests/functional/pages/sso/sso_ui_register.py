# -*- coding: utf-8 -*-
"""SSO - Registration page"""
import logging
from urllib.parse import quote, urljoin

from requests import Response, Session

from tests import URLs
from tests.functional.pages import Services
from tests.functional.utils.context_utils import Actor, Company
from tests.functional.utils.request import Method, check_response, make_request

SERVICE = Services.SSO
NAME = "Register"
TYPE = "form"
URL = URLs.SSO_SIGNUP.absolute
EXPECTED_STRINGS = [
    "Register",
    "Create a great.gov.uk account and you can",
    "Email",
    "Confirm email",
    "Password",
    "Confirm password",
    "Your password must",
    "be at least 10 characters",
    "contain at least one letter",
    "contain at least one number",
    'not contain the word "password"',
    "Tick this box to accept the",
    "terms and conditions",
    "of the great.gov.uk service.",
]


def should_be_here(response: Response):
    check_response(response, 200, body_contains=EXPECTED_STRINGS)
    logging.debug("Successfully got to the SSO Registration page")


def go_to(
    session: Session, *, next: str = None, referer: str = None
) -> Response:
    referer = referer or URLs.FAB_LANDING.absolute
    if next:
        url = urljoin(URL, f"?next={next}")
    else:
        url = URL
    headers = {"Referer": referer}
    return make_request(Method.GET, url, session=session, headers=headers)


def submit(actor: Actor, company: Company) -> Response:
    """Will submit the SSO Registration form with Supplier & Company details."""
    session = actor.session
    next_url = URLs.FAB_REGISTER_SUBMIT_ACCOUNT_DETAILS.absolute
    next_link_query = f"?company_number={company.number}"
    next_link = quote(urljoin(next_url, next_link_query))
    referer_query = f"?next={next_link}"
    headers = {"Referer": urljoin(URL, referer_query)}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "email": actor.email,
        "email2": actor.email,
        "password1": actor.password,
        "password2": actor.password,
        "terms_agreed": "on",
        "next": next_link,
    }

    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )


def submit_no_company(
    actor: Actor, *, next: str = None, referer: str = URL
) -> Response:
    """Will submit the SSO Registration form without company's details.

    Used when Supplier creates a SSO/great.gov.uk account first.
    """
    session = actor.session
    headers = {"Referer": referer}
    data = {
        "csrfmiddlewaretoken": actor.csrfmiddlewaretoken,
        "email": actor.email,
        "email2": actor.email,
        "password1": actor.password,
        "password2": actor.password,
        "terms_agreed": "on",
    }
    if next:
        data["next"] = next

    return make_request(
        Method.POST, URL, session=session, headers=headers, data=data
    )
