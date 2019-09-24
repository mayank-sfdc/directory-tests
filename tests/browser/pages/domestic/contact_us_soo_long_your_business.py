# -*- coding: utf-8 -*-
"""Domestic - First page of Long SOO Contact us form"""
import logging
import random
from types import ModuleType
from urllib.parse import urljoin

from directory_tests_shared.enums import Service
from directory_tests_shared.settings import DOMESTIC_URL
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    assertion_msg,
    check_url,
    fill_out_input_fields,
    find_element,
    go_to_url,
    take_screenshot,
    tick_checkboxes,
)
from pages.domestic import contact_us_soo_long_organisation_details
from pages.domestic.autocomplete_callbacks import autocomplete_company_name

NAME = "Long Domestic (Your Business)"
SERVICE = Service.DOMESTIC
TYPE = "Contact us"
URL = urljoin(DOMESTIC_URL, "contact/selling-online-overseas/organisation/")
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "div.exred-triage-form button", type=ElementType.BUTTON
)
WEBSITE = Selector(By.ID, "id_organisation-website_address", type=ElementType.INPUT)
COMPANY_NAME = Selector(By.ID, "id_organisation-company_name", type=ElementType.INPUT)
COMPANY_POSTCODE = Selector(
    By.ID, "id_organisation-company_postcode", type=ElementType.INPUT
)
COMPANY_NUMBER = Selector(
    By.ID, "id_organisation-company_number", type=ElementType.INPUT
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "i don't have a company number": Selector(
            By.ID, "id_organisation-soletrader", type=ElementType.CHECKBOX
        ),
        "company website": WEBSITE,
        "company name": COMPANY_NAME,
    }
}

HAS_COMPANY_NUMBER = {
    "company name": Selector(
        By.ID,
        "id_organisation-company_name",
        type=ElementType.INPUT,
        is_visible=False,
        autocomplete_callback=autocomplete_company_name,
    ),
    "company number": COMPANY_NUMBER,
}

DOESNT_HAVE_COMPANY_NUMBER = {"company postcode": COMPANY_POSTCODE}
PREPOPULATED_FORM_FIELDS = {
    "company name": COMPANY_NAME,
    "company number": COMPANY_NUMBER,
    "company postcode": COMPANY_POSTCODE,
    "company website": WEBSITE,
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    does_not_have_company_number = custom_details.get(
        "i don't have a company number", random.choice([True, False])
    )
    result = {
        "i don't have a company number": does_not_have_company_number,
        "company website": f"http://{actor.email}.automated.tests.com".replace(
            "@", "."
        ),
    }

    if does_not_have_company_number:
        result.update(
            {"company postcode": "SW1H 0TL", "company name": "Automated Test"}
        )
        SELECTORS["form"].update(DOESNT_HAVE_COMPANY_NUMBER)
        SELECTORS["form"] = dict(
            set(SELECTORS["form"].items()) - set(HAS_COMPANY_NUMBER.items())
        )
    else:
        result.update(
            {
                "company name": "COLDSPACE COLD ROOMS (UK) LLP",
                "company number": "OC399213",
                "company postcode": "GL2 2AQ",
            }
        )
        SELECTORS["form"].update(HAS_COMPANY_NUMBER)

    if custom_details:
        result.update(custom_details)

    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    tick_checkboxes(driver, form_selectors, details)
    fill_out_input_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return contact_us_soo_long_organisation_details


def check_if_populated(driver: WebDriver, expected_form_details: dict):
    for key, expected_value in expected_form_details.items():
        existing_field_selector = PREPOPULATED_FORM_FIELDS.get(key, None)
        if not existing_field_selector:
            continue
        existing_field = find_element(driver, existing_field_selector, element_name=key)
        existing_field_value = existing_field.get_attribute("value")
        if expected_value:
            error = (
                f"Expected '{key}' value to be '{expected_value}' but got "
                f"'{existing_field_value}'"
            )
            with assertion_msg(error):
                assert existing_field_value.lower() == expected_value.lower()
                logging.debug(
                    f"'{key}' field was prepopulated with expected value: "
                    f"'{expected_value}'"
                )
