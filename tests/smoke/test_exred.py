import http.client

import pytest
import requests

from tests import get_absolute_url
from tests.settings import DIRECTORY_API_HEALTH_CHECK_TOKEN as TOKEN


@pytest.mark.parametrize("absolute_url", [
    get_absolute_url('ui-exred:healthcheck-api'),
    get_absolute_url('ui-exred:healthcheck-sso-proxy'),
])
def test_health_check_endpoints(absolute_url, hawk_cookie):
    params = {'token': TOKEN}
    response = requests.get(
        absolute_url, params=params, cookies=hawk_cookie
    )
    assert response.status_code == http.client.OK


def test_terms_200(hawk_cookie):
    response = requests.get(
        get_absolute_url('ui-exred:terms'), cookies=hawk_cookie
    )
    assert response.status_code == http.client.OK


def test_privacy_200(hawk_cookie):
    response = requests.get(
        get_absolute_url('ui-exred:privacy'), cookies=hawk_cookie
    )
    assert response.status_code == http.client.OK


