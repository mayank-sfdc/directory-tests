import pytest
from rest_framework.status import HTTP_200_OK, HTTP_301_MOVED_PERMANENTLY

from tests import get_absolute_url
from tests.smoke.cms_api_helpers import get_and_assert, status_error


@pytest.mark.session_auth
@pytest.mark.parametrize(
    "url",
    [
        get_absolute_url("sso:landing"),
        get_absolute_url("sso:login"),
        get_absolute_url("sso:signup"),
    ],
)
def test_access_sso_endpoints_as_logged_in_user_w_redirect_to_sud(
    logged_in_session, url, basic_auth
):
    response = logged_in_session.get(
        url, allow_redirects=True, auth=basic_auth
    )
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.prod
@pytest.mark.parametrize(
    "url",
    [
        get_absolute_url("sso:logout"),
        get_absolute_url("sso:password_change"),
        get_absolute_url("sso:password_set"),
        get_absolute_url("sso:password_reset"),
        get_absolute_url("sso:email_confirm"),
        get_absolute_url("sso:inactive"),
    ],
)
def test_access_sso_endpoints_as_anonymous_user_yields_200(url, basic_auth):
    get_and_assert(
        url=url, allow_redirects=True, status_code=HTTP_200_OK, auth=basic_auth
    )


@pytest.mark.session_auth
@pytest.mark.parametrize(
    "url",
    [
        get_absolute_url("sso:logout"),
        get_absolute_url("sso:password_change"),
        get_absolute_url("sso:password_set"),
        get_absolute_url("sso:password_reset"),
        get_absolute_url("sso:email_confirm"),
        get_absolute_url("sso:inactive"),
    ],
)
def test_access_sso_endpoints_as_logged_in_user_wo_redirect_to_sud(
    logged_in_session, url, basic_auth
):
    response = logged_in_session.get(
        url, allow_redirects=True, auth=basic_auth
    )
    assert response.status_code == HTTP_200_OK, status_error(
        HTTP_200_OK, response
    )


@pytest.mark.session_auth
@pytest.mark.parametrize(
    "url, expected_status_code",
    [
        (get_absolute_url("sso:landing"), HTTP_301_MOVED_PERMANENTLY),
        (get_absolute_url("sso:login"), HTTP_301_MOVED_PERMANENTLY),
        (get_absolute_url("sso:signup"), HTTP_301_MOVED_PERMANENTLY),
        (get_absolute_url("sso:logout"), HTTP_301_MOVED_PERMANENTLY),
        (get_absolute_url("sso:password_change"), HTTP_301_MOVED_PERMANENTLY),
        (get_absolute_url("sso:password_set"), HTTP_301_MOVED_PERMANENTLY),
        (get_absolute_url("sso:password_reset"), HTTP_301_MOVED_PERMANENTLY),
        (get_absolute_url("sso:email_confirm"), HTTP_301_MOVED_PERMANENTLY),
        (get_absolute_url("sso:inactive"), HTTP_301_MOVED_PERMANENTLY),
    ],
)
def test_redirects_after_removing_trailing_slash_as_logged_in_user(
    logged_in_session, url, expected_status_code, basic_auth
):
    # get rid of trailing slash
    if url[-1] == "/":
        url = url[:-1]
    response = logged_in_session.get(
        url, allow_redirects=False, auth=basic_auth
    )
    assert response.status_code == expected_status_code, status_error(
        expected_status_code, response
    )
