import pytest
import requests
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_301_MOVED_PERMANENTLY,
    HTTP_302_FOUND,
)

from tests import get_absolute_url, URLs
from tests.smoke.cms_api_helpers import get_and_assert, status_error


@pytest.mark.stage
@pytest.mark.parametrize(
    "url",
    [
        URLs.LEGACY_CONTACT_US_HELP.absolute,
        URLs.LEGACY_CONTACT_US_FEEDBACK_FORM.absolute,
    ],
)
def test_access_as_anon_user(url, basic_auth):
    response = requests.get(url, allow_redirects=False)
    redirect = response.headers["location"]
    get_and_assert(
        url=redirect,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )


@pytest.mark.stage
@pytest.mark.parametrize(
    "url",
    [
        URLs.LEGACY_CONTACT_US_HELP.absolute,
        URLs.LEGACY_CONTACT_US_FEEDBACK_FORM.absolute,
    ],
)
def test_access_contact_us_as_anon_user_after_removing_trailing_slash(
    url, basic_auth
):
    # get rid of trailing slash
    if url[-1] == "/":
        url = url[:-1]
    response = requests.get(url, allow_redirects=False)
    redirect = response.headers["location"]
    get_and_assert(
        url=redirect,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )


@pytest.mark.stage
@pytest.mark.parametrize(
    "url", [get_absolute_url("ui-buyer:confirm-identity")]
)
def test_302_redirects_for_anon_user(url, basic_auth):
    get_and_assert(
        url=url,
        allow_redirects=False,
        status_code=HTTP_302_FOUND,
        auth=basic_auth,
    )


@pytest.mark.parametrize(
    "url", [get_absolute_url("ui-buyer:confirm-identity")]
)
def test_301_redirects_after_removing_trailing_slash_for_anon_user(
    url, basic_auth
):
    # get rid of trailing slash
    if url[-1] == "/":
        url = url[:-1]
    response = get_and_assert(
        url=url,
        allow_redirects=False,
        status_code=HTTP_301_MOVED_PERMANENTLY,
        auth=basic_auth,
    )
    assert response.headers["location"] == "/find-a-buyer/verify/"


@pytest.mark.session_auth
@pytest.mark.stage
@pytest.mark.parametrize(
    "url", [get_absolute_url("ui-buyer:confirm-identity")]
)
def test_access_endpoints_as_logged_in_user(
    logged_in_session, url, basic_auth
):
    response = logged_in_session.get(
        url, allow_redirects=True, auth=basic_auth
    )
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.session_auth
@pytest.mark.stage
@pytest.mark.parametrize(
    "url", [get_absolute_url("ui-buyer:confirm-identity")]
)
def test_check_if_verify_endpoint_redirects_to_correct_page(
    logged_in_session, url, basic_auth
):
    response = logged_in_session.get(
        url, allow_redirects=True, auth=basic_auth
    )
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )
    # depends on the test account status/configuration user should either get
    # to the letter verification page or to their profile page if they already
    # went through verification
    got_to_letter_confirmation = response.url == get_absolute_url(
        "ui-buyer:confirm-company-address"
    )
    got_to_profile = response.url == get_absolute_url("profile:fab")
    assert got_to_letter_confirmation or got_to_profile
