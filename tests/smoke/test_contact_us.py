# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import pytest
import requests
from rest_framework.status import HTTP_200_OK

from directory_tests_shared import URLs
from tests.smoke.cms_api_helpers import get_and_assert


@pytest.mark.parametrize(
    "endpoint, expected_redirect",
    [
        ("contact/",                              "/contact/triage/location/"),
        ("directory/",                            "/contact/triage/location/"),
        ("eig/",                                  "/contact/triage/location/"),
        ("export-opportunities/FeedbackForm/",    "/contact/feedback/"),
        ("export_opportunities/",                 "/contact/triage/domestic/"),
        ("export_opportunities/FeedbackForm/",    "/contact/feedback/"),
        ("export_ops/",                           "/contact/triage/domestic/"),
        ("export_readiness/FeedbackForm/",        "/contact/feedback/"),
        ("feedback/",                             "/contact/feedback/"),
        ("feedback/datahub/",                     "/contact/feedback/"),
        ("feedback/directory/",                   "/contact/feedback/"),
        ("feedback/e_navigator/",                 "/contact/feedback/"),
        ("feedback/eig/",                         "/contact/feedback/"),
        ("feedback/export_ops/",                  "/contact/feedback/"),
        ("feedback/exportingisgreat/",            "/contact/feedback/"),
        ("feedback/exportopportunities/",         "/contact/feedback/"),
        ("feedback/invest/",                      "/contact/feedback/"),
        ("feedback/opportunities/",               "/contact/feedback/"),
        ("feedback/selling-online-overseas/",     "/contact/feedback/"),
        ("feedback/selling_online_overseas/",     "/contact/feedback/"),
        ("feedback/single_sign_on/",              "/contact/feedback/"),
        ("feedback/soo/",                         "/contact/feedback/"),
        ("feedback/sso/",                         "/contact/feedback/"),
        ("help/",                                 "/contact/triage/location/"),
        ("help/FeedbackForm/",                    "/contact/feedback/"),
        ("invest/FeedbackForm/",                  "/contact/feedback/"),
        ("opportunities/FeedbackForm/",           "/contact/feedback/"),
        ("selling_online_overseas/",              "/contact/triage/domestic/"),
        ("selling_online_overseas/FeedbackForm/", "/contact/feedback/"),
        ("single_sign_on/",                       "/contact/triage/great-account/"),
        ("single_sign_on/FeedbackForm/",          "/contact/feedback/"),
        ("soo/FeedbackForm/",                     "/contact/feedback/"),
        ("soo/Triage/",                           "/contact/triage/location/"),
        ("soo/feedback/",                         "/contact/feedback/"),
        ("triage/",                               "/contact/triage/location/"),
        ("triage/directory/",                     "/contact/triage/location/"),
        ("triage/sso/",                           "/contact/triage/location/"),
    ]
)
def test_redirects_for_legacy_contact_us_urls(
        endpoint, expected_redirect, basic_auth
):
    url = urljoin(URLs.LEGACY_CONTACT_US_LANDING.absolute, endpoint)
    legacy_contact_us_response = requests.get(url, allow_redirects=False)
    redirect = legacy_contact_us_response.headers["location"]
    response = get_and_assert(
        url=redirect,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )
    if response.history:
        redirects = [h.headers['Location'] for h in response.history]
        last_redirect = redirects[-1]
        error_message = (f"Expected {url} redirect to: '{expected_redirect}' "
                         f"but got {last_redirect}")
        assert expected_redirect == last_redirect, error_message


@pytest.mark.stage
@pytest.mark.parametrize(
    "url, expected_redirect",
    [
        (urljoin(URLs.LEGACY_CONTACT_US_LANDING.absolute, "soo/TriageForm/"), URLs.SSO_LOGIN.absolute),
        (urljoin(URLs.LEGACY_CONTACT_US_LANDING.absolute, "triage/soo/"), URLs.SSO_LOGIN.absolute),
    ]
)
def test_legacy_contact_us_soo_urls_should_redirect_to_sso(
        url, expected_redirect, basic_auth
):
    response = requests.get(url, allow_redirects=True, auth=basic_auth)
    if "Access denied" in response.content.decode("UTF-8"):
        response = requests.get(response.url, allow_redirects=True, auth=basic_auth)

    error = (f"Expected request to {url} to be redirected to "
             f"{expected_redirect}, but got {response.url}")
    assert response.url.startswith(expected_redirect), error
    error = (f"After logging in user should be redirected to "
             f"'contact/selling-online-overseas/organisation/' but ended up on"
             f" {response.url}")
    assert response.url.endswith("contact/selling-online-overseas/organisation/"), error


@pytest.mark.parametrize("endpoint, expected_redirect", [
    ("directory/FeedbackForm/", "/contact/feedback/"),
])
def test_redirects_for_legacy_contact_us_urls_direct(
        endpoint, expected_redirect, basic_auth
):
    url = urljoin(URLs.LEGACY_CONTACT_US_LANDING.absolute, endpoint)
    legacy_contact_us_response = requests.get(url, allow_redirects=False)
    redirect = legacy_contact_us_response.headers["location"]
    response = get_and_assert(
        url=redirect,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )
    assert response.url.endswith("/contact/feedback/")


@pytest.mark.dev
@pytest.mark.parametrize(
    "market",
    [
        "1688com",
        "amazon-canada",
        "amazon-china",
        "amazon-france",
        "amazon-germany",
        "amazon-italy",
        "amazon-japan",
        "amazon-spain",
        "amazon-usa",
        "cdiscount",
        "ebay",
        "etsy",
        "flipkart",
        "jd-worldwide",
        "kaola",
        "newegg-inc",
        "privalia",
        "rakuten",
        "royal-mail-t-mall",
        "sfbest",
        "shangpin",
        "spartoo",
        "trademe",
    ]
)
def test_access_contact_us_organisation_endpoints_dev(market, basic_auth):
    params = {"market": market}
    get_and_assert(
        url=URLs.CONTACT_US_SOO_ORGANISATION.absolute,
        params=params,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )


@pytest.mark.stage
@pytest.mark.parametrize(
    "market",
    [
        "1688com",
        "amazon-canada",
        "amazon-china",
        "amazon-france",
        "amazon-germany",
        "amazon-italy",
        "amazon-japan",
        "amazon-mexico",
        "amazon-spain",
        "amazon-usa",
        "cdiscount",
        "ebay",
        "flipkart",
        "fruugo",
        "goxip",
        "jd-worldwide",
        "kaola",
        "la-redoute",
        "linio",
        "newegg-business",
        "newegg-canada",
        "newegg-inc",
        "privalia",
        "rakuten",
        "royal-mail-t-mall",
        "sfbest",
        "shangpin",
        "spartoo",
        "trademe",
        "tthigo",
    ]
)
def test_access_contact_us_organisation_endpoints_stage(market, basic_auth):
    params = {"market": market}
    get_and_assert(
        url=URLs.CONTACT_US_SOO_ORGANISATION.absolute,
        params=params,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )


@pytest.mark.prod
@pytest.mark.parametrize(
    "market",
    [
        "1688com",
        "amazon-canada",
        "amazon-china",
        "amazon-france",
        "amazon-germany",
        "amazon-italy",
        "amazon-japan",
        "amazon-mexico",
        "amazon-spain",
        "amazon-usa",
        "bol",
        "catch",
        "cdiscount",
        "darty",
        "ebay",
        "eprice",
        "flipkart",
        "fnac",
        "fruugo",
        "goxip",
        "jd-worldwide",
        "kaola",
        "la-redoute",
        "linio",
        "mano-mano",
        "newegg-business",
        "newegg-canada",
        "newegg-inc",
        "onbuy",
        "privalia",
        "rakuten",
        "royal-mail-t-mall",
        "sfbest",
        "shangpin",
        "spartoo",
        "trademe",
        "tthigo",
    ]
)
def test_access_contact_us_organisation_endpoints_prod(market):
    params = {"market": market}
    get_and_assert(
        url=URLs.CONTACT_US_SOO_ORGANISATION.absolute,
        params=params,
        allow_redirects=True,
        status_code=HTTP_200_OK,
    )


@pytest.mark.parametrize("url", [
    URLs.CONTACT_US_SOO_ORGANISATION_DETAILS.absolute,
    URLs.CONTACT_US_SOO_ORGANISATION_YOUR_EXPERIENCE.absolute,
    URLs.CONTACT_US_SOO_ORGANISATION_CONTACT_DETAILS.absolute,
    URLs.CONTACT_US_SOO_ORGANISATION_SUCCESS.absolute,
])
def test_access_contact_us_endpoints(url, basic_auth):
    get_and_assert(
        url=url,
        allow_redirects=True,
        status_code=HTTP_200_OK,
        auth=basic_auth,
    )
