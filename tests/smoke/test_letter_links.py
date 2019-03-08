import pytest
import requests
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_301_MOVED_PERMANENTLY,
    HTTP_302_FOUND,
)

from tests import get_absolute_url
from tests.smoke.cms_api_helpers import status_error


@pytest.mark.stage
@pytest.mark.parametrize(
    "absolute_url,redirect",
    [
        (
            get_absolute_url("legacy-ui-contact-us:help"),
            get_absolute_url("ui-contact-us-legacy-redirects:help"),
        ),
        (
            get_absolute_url("legacy-ui-contact-us:feedback-form"),
            get_absolute_url("ui-contact-us-legacy-redirects:feedback"),
        ),
    ],
)
def test_access_as_anon_user(absolute_url, redirect):
    response = requests.get(absolute_url, allow_redirects=False)
    assert response.status_code == HTTP_302_FOUND, status_error(
        HTTP_302_FOUND, response
    )
    assert response.headers["location"] == redirect


@pytest.mark.stage
@pytest.mark.parametrize(
    "absolute_url,redirect",
    [
        (
            get_absolute_url("legacy-ui-contact-us:help"),
            get_absolute_url("ui-contact-us-legacy-redirects:help"),
        ),
        (
            get_absolute_url("legacy-ui-contact-us:feedback-form"),
            get_absolute_url("ui-contact-us-legacy-redirects:feedback"),
        ),
    ],
)
def test_access_contact_us_as_anon_user_after_removing_trailing_slash(
    absolute_url, redirect
):
    # get rid of trailing slash
    absolute_url = absolute_url[:-1]
    response = requests.get(absolute_url, allow_redirects=False)
    assert response.status_code == HTTP_302_FOUND, status_error(
        HTTP_302_FOUND, response
    )
    assert response.headers["location"] == redirect[:-1]


@pytest.mark.stage
@pytest.mark.parametrize(
    "absolute_url", [get_absolute_url("ui-buyer:confirm-identity")]
)
def test_302_redirects_for_anon_user(absolute_url, basic_auth):
    response = requests.get(
        absolute_url, allow_redirects=False, auth=basic_auth
    )
    assert response.status_code == HTTP_302_FOUND


@pytest.mark.parametrize(
    "absolute_url", [get_absolute_url("ui-buyer:confirm-identity")]
)
def test_301_redirects_after_removing_trailing_slash_for_anon_user(
    absolute_url, basic_auth
):
    # get rid of trailing slash
    absolute_url = absolute_url[:-1]
    response = requests.get(
        absolute_url, allow_redirects=False, auth=basic_auth
    )
    assert response.status_code == HTTP_301_MOVED_PERMANENTLY
    assert response.headers["location"] == "/find-a-buyer/verify/"


@pytest.mark.session_auth
@pytest.mark.stage
@pytest.mark.parametrize(
    "absolute_url", [get_absolute_url("ui-buyer:confirm-identity")]
)
def test_access_endpoints_as_logged_in_user(
    logged_in_session, absolute_url, basic_auth
):
    response = logged_in_session.get(
        absolute_url, allow_redirects=True, auth=basic_auth
    )
    assert response.status_code == HTTP_200_OK


@pytest.mark.session_auth
@pytest.mark.stage
@pytest.mark.parametrize(
    "absolute_url", [get_absolute_url("ui-buyer:confirm-identity")]
)
def test_check_if_verify_endpoint_redirects_to_correct_page(
    logged_in_session, absolute_url, basic_auth
):
    response = logged_in_session.get(
        absolute_url, allow_redirects=True, auth=basic_auth
    )
    assert response.status_code == HTTP_200_OK
    # depends on the test account status/configuration user should either get
    # to the letter verification page or to their profile page if they already
    # went through verification
    got_to_letter_confirmation = response.url == get_absolute_url(
        "ui-buyer:confirm-company-address"
    )
    got_to_profile = response.url == get_absolute_url(
        "ui-buyer:company-profile"
    )
    assert got_to_letter_confirmation or got_to_profile
