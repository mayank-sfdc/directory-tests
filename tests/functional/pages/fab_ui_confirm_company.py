# -*- coding: utf-8 -*-
"""FAB - Confirm Company page"""
import logging
from urllib.parse import urljoin

from requests import Response, Session

from tests import get_absolute_url
from tests.functional.utils.context_utils import Company
from tests.functional.utils.generic import escape_html
from tests.functional.utils.request import Method, check_response, make_request

URL = get_absolute_url('ui-buyer:landing')
EXPECTED_STRINGS = [
    "Create your company’s profile", "Confirm company", "Trading status",
    "Company number",
    ("To confirm that this is your company you must create a great.gov.uk "
     "account."), "An account will let you:",
    "create a trade profile that will be promoted to international buyers",
    ("apply for export opportunities from foreign companies sourced by UK "
     "government"), "Create account", "Cancel"
]


def go_to(session: Session, company: Company) -> Response:
    """Go to "Confirm Company" page. This requires Company

    :param session: Supplier session object
    :param company: a namedtuple with Company details
    :return: response object
    """
    data = {"company_name": company.title, "company_number": company.number}
    headers = {"Referer": URL}

    response = make_request(
        Method.POST, URL, session=session, headers=headers, data=data)

    return response


def should_be_here(response: Response, company: Company):
    """Check if Supplier is on Confirm Export Status page.

    :param response: response with Confirm Export Status page
    :param company: a namedtuple with Company details
    """
    escaped_company_title = escape_html(company.title, upper=True)
    expected = EXPECTED_STRINGS + [escaped_company_title, company.number]
    check_response(response, 200, body_contains=expected)
    logging.debug("Successfully got to the Confirm your Company page")


def confirm_company_selection(
        session: Session, company: Company, token: str) -> Response:
    """Confirm that the selected company is the right one.

    :param session: Supplier session object
    :param company: a named tuple with Company details
    :param token: a CSRF token required to submit the form
    """
    query = "?company_number={}".format(company.number)
    url = urljoin(get_absolute_url('ui-buyer:register-confirm-company'), query)
    headers = {"Referer": url}
    data = {
        "csrfmiddlewaretoken": token,
        "enrolment_view-current_step": "company",
        "company-company_name": company.title,
        "company-company_number": company.number,
        "company-company_address": company.companies_house_details["address_snippet"]
    }

    return make_request(
        Method.POST, url, session=session, headers=headers, data=data)
