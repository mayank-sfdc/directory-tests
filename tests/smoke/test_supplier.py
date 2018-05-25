import http.client

import requests

from tests import join_ui_supplier, get_absolute_url


def test_landing_page_200():
    response = requests.get(get_absolute_url('ui-supplier:landing'))

    assert response.status_code == http.client.OK


def test_supplier_list_200():
    response = requests.get(get_absolute_url('ui-supplier:suppliers'))

    assert response.status_code == http.client.OK


def test_industries_list_200():
    response = requests.get(get_absolute_url('ui-supplier:industries'))

    assert response.status_code == http.client.OK


def test_health_industry_200():
    response = requests.get(get_absolute_url('ui-supplier:industries-health'))

    assert response.status_code == http.client.OK


def test_tech_industry_200():
    response = requests.get(get_absolute_url('ui-supplier:industries-tech'))

    assert response.status_code == http.client.OK


def test_creative_industry_200():
    url = get_absolute_url('ui-supplier:industries-creative')
    response = requests.get(url)

    assert response.status_code == http.client.OK


def test_food_industry_200():
    response = requests.get(get_absolute_url('ui-supplier:industries-food'))

    assert response.status_code == http.client.OK


def test_supplier_profile_200():
    # company 09466005 must exist on the environment the tests are ran against.
    url = join_ui_supplier('suppliers/09466005/michboly-ltd')
    response = requests.get(url)

    assert response.status_code == http.client.OK


def test_supplier_contact_200():
    # company 09466005 must exist on the environment the tests are ran against.
    url = join_ui_supplier('suppliers/09466005/contact')
    response = requests.get(url)

    assert response.status_code == http.client.OK


def test_case_study_200():
    # case study 6 must exist on the environment the tests are ran against.
    url = join_ui_supplier('case-study/6/fred')

    response = requests.get(url)

    assert response.status_code == http.client.OK
