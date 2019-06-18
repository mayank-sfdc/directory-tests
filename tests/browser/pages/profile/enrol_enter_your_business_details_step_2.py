# -*- coding: utf-8 -*-
"""Profile - Enrol - Enter your business details"""
import logging
from collections import defaultdict
from types import ModuleType
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType, Services
from pages.common_actions import (
    Actor,
    Selector,
    check_for_sections,
    check_url,
    fill_out_input_fields,
    find_and_click_on_page_element,
    find_elements_of_type,
    go_to_url,
    pick_option,
    take_screenshot,
)
from pages.profile import enrol_enter_your_details
from settings import DIRECTORY_UI_PROFILE_URL

NAME = "Enter your business details [step 2]"
NAMES = ["Enter your business details [step 2] (LTD, PLC or Royal Charter)"]
SERVICE = Services.PROFILE
TYPE = "Enrol"
URL = urljoin(
    DIRECTORY_UI_PROFILE_URL, "enrol/business-type/companies-house/business-details/"
)
URLs = {"enter your business details [step 2] (ltd, plc or royal charter)": URL}
PAGE_TITLE = ""

INDUSTRY = Selector(
    By.ID, "id_business-details-sectors", is_visible=False, type=ElementType.SELECT
)
WEBSITE = Selector(
    By.ID, "id_business-details-website", is_visible=False, type=ElementType.INPUT
)
SELECTORS = {
    "enrolment progress bar": {"itself": Selector(By.ID, "progress-column")},
    "enter your business details": {
        "itself": Selector(By.CSS_SELECTOR, "section form"),
        "heading": Selector(By.CSS_SELECTOR, "h2"),
        "text": Selector(By.ID, "form-step-body-text"),
        "company name": Selector(By.ID, "id_business-details-company_name"),
        "industry": INDUSTRY,
        "website": WEBSITE,
        "submit": Selector(
            By.CSS_SELECTOR, "form button.button", type=ElementType.BUTTON
        ),
    },
}
FORM_FIELDS_WITH_USEFUL_DATA = {
    "company name": Selector(
        By.ID, "id_business-details-company_name", type=ElementType.INPUT
    ),
    "company number": Selector(
        By.ID,
        "id_business-details-company_number",
        type=ElementType.INPUT,
        is_visible=False,
    ),
    "industry": INDUSTRY,
    "company website": WEBSITE,
    "sic": Selector(By.ID, "id_business-details-sic", type=ElementType.INPUT),
    "date_of_creation": Selector(
        By.ID, "id_business-details-date_of_creation", type=ElementType.INPUT
    ),
    "address": Selector(By.ID, "id_business-details-address", type=ElementType.INPUT),
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, NAME)
    url = URLs[page_name.lower()] if page_name else URL
    check_url(driver, url, exact_match=False)
    msg = f"Got 404 on {driver.current_url}"
    assert "This page cannot be found" not in driver.page_source, msg


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor) -> dict:
    result = {"industry": None, "website": "https://automated.test.com"}
    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["enter your business details"]
    pick_option(driver, form_selectors, details)
    fill_out_input_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    find_and_click_on_page_element(driver, SELECTORS, "submit", wait_for_it=False)
    take_screenshot(driver, "After submitting the form")
    return enrol_enter_your_details


def get_form_details(driver: WebDriver) -> dict:
    elements = find_elements_of_type(
        driver, FORM_FIELDS_WITH_USEFUL_DATA, ElementType.INPUT
    )
    result = defaultdict()
    for key, element in elements.items():
        value = element.get_attribute("value")
        result[key] = value

    return dict(result)
