# -*- coding: utf-8 -*-
"""Domestic - First page of Long SOO Contact us form"""
import logging
import random
from types import ModuleType

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import Service
from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_random_radio,
    check_url,
    fill_out_input_fields,
    find_element,
    go_to_url,
    take_screenshot,
)
from pages.domestic import contact_us_soo_long_your_experience

NAME = "Long Domestic (Organisation details)"
SERVICE = Service.DOMESTIC
TYPE = "Contact us"
URL = URLs.CONTACT_US_SOO_ORGANISATION_DETAILS.absolute
PAGE_TITLE = "Welcome to great.gov.uk"

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "div.exred-triage-form button", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "under £100,000": Selector(
            By.ID,
            "id_organisation-details-turnover_0",
            type=ElementType.RADIO,
            group_id=1,
        ),
        "£100,000 to £500,000": Selector(
            By.ID,
            "id_organisation-details-turnover_1",
            type=ElementType.RADIO,
            group_id=1,
        ),
        "£500,001 to £2million": Selector(
            By.ID,
            "id_organisation-details-turnover_2",
            type=ElementType.RADIO,
            group_id=1,
        ),
        "more than £2million": Selector(
            By.ID,
            "id_organisation-details-turnover_3",
            type=ElementType.RADIO,
            group_id=1,
        ),
        "sku": Selector(
            By.ID, "id_organisation-details-sku_count", type=ElementType.INPUT
        ),
        "yes": Selector(
            By.ID,
            "id_organisation-details-trademarked_0",
            type=ElementType.RADIO,
            group_id=2,
        ),
        "no": Selector(
            By.ID,
            "id_organisation-details-trademarked_1",
            type=ElementType.RADIO,
            group_id=2,
        ),
    }
}

OTHER_SELECTORS = {
    "postcode": Selector(
        By.ID, "id_organisation-company_postcode", type=ElementType.INPUT
    )
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def generate_form_details(actor: Actor) -> dict:
    result = {"sku": random.randint(0, 10000)}
    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    check_random_radio(driver, form_selectors)
    fill_out_input_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return contact_us_soo_long_your_experience
