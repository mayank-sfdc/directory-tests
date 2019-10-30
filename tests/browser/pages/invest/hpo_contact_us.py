# -*- coding: utf-8 -*-
"""Invest in Great - Contact us Page Object."""
import logging
from typing import List
from uuid import uuid4

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Actor,
    Selector,
    check_for_sections,
    check_if_element_is_not_visible,
    check_url,
    fill_out_input_fields,
    fill_out_textarea_fields,
    find_element,
    find_selector_by_name,
    pick_option_from_autosuggestion,
    take_screenshot,
    tick_captcha_checkbox,
    tick_checkboxes_by_labels,
    visit_url,
)

NAME = "HPO Contact us"
NAMES = [
    "High productivity food production",
    "Lightweight structures",
    "Rail infrastructure",
]
SERVICE = Service.INVEST
TYPE = PageType.CONTACT_US
URL = URLs.INVEST_HPO_CONTACT.absolute
SubURLs = {
    "high productivity food production": URL,
    "lightweight structures": URL,
    "rail infrastructure": URL,
}
PAGE_TITLE = ""

IM_NOT_A_ROBOT = Selector(By.CSS_SELECTOR, ".recaptcha-checkbox-checkmark")
SUBMIT_BUTTON = Selector(By.ID, "submit-button")
SELECTORS = {
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "#content form"),
        "full name": Selector(By.ID, "id_full_name", type=ElementType.INPUT),
        "job title": Selector(By.ID, "id_role_in_company", type=ElementType.INPUT),
        "email": Selector(By.ID, "id_email_address", type=ElementType.INPUT),
        "phone": Selector(By.ID, "id_phone_number", type=ElementType.INPUT),
        "company name": Selector(By.ID, "id_company_name", type=ElementType.INPUT),
        "website url": Selector(By.ID, "id_website_url", type=ElementType.INPUT),
        "country": Selector(
            By.ID, "js-country-select-select", type=ElementType.SELECT, is_visible=False
        ),
        "organisation size": Selector(
            By.ID, "id_company_size", type=ElementType.SELECT
        ),
        "advanced food production": Selector(
            By.ID,
            "checkbox-multiple-advanced-food-production",
            type=ElementType.LABEL,
            is_visible=False,
        ),
        "lightweight structures": Selector(
            By.ID,
            "checkbox-multiple-lightweight-structures",
            type=ElementType.LABEL,
            is_visible=False,
        ),
        "rail infrastructure": Selector(
            By.ID,
            "checkbox-multiple-rail-infrastructure",
            type=ElementType.LABEL,
            is_visible=False,
        ),
        "comment": Selector(By.ID, "id_comment", type=ElementType.TEXTAREA),
        "terms and conditions": Selector(
            By.ID, "id_terms_agreed", type=ElementType.LABEL, is_visible=False
        ),
        "terms and conditions link": Selector(
            By.CSS_SELECTOR, "#id_terms_agreed-label a"
        ),
        "captcha": Selector(
            By.CSS_SELECTOR, "#form-container iframe", type=ElementType.IFRAME
        ),
        "submit": SUBMIT_BUTTON,
    },
    "elements invisible to selenium": {
        "advanced food production checkbox": Selector(
            By.ID, "checkbox-multiple-advanced-food-production", is_visible=False
        ),
        "rail infrastructure checkbox": Selector(
            By.ID, "checkbox-multiple-rail-infrastructure", is_visible=False
        ),
        "lightweight structures checkbox": Selector(
            By.ID, "checkbox-multiple-lightweight-structures", is_visible=False
        ),
        "terms and conditions checkbox": Selector(
            By.ID, "id_terms_agreed", is_visible=False
        ),
    },
}
SELECTORS.update(common_selectors.INVEST_HEADER)
SELECTORS.update(common_selectors.BETA_BAR)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INVEST_FOOTER)

UNEXPECTED_ELEMENTS = {
    "breadcrumbs": {"itself": Selector(By.CSS_SELECTOR, "div.breadcrumbs")}
}


def visit(driver: WebDriver, *, page_name: str = None):
    url = SubURLs[page_name] if page_name else URL
    visit_url(driver, url)


def should_be_here(driver: WebDriver, *, page_name: str):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def check_state_of_form_element(
    driver: WebDriver, element_name: str, expected_state: str
):
    element_selector = find_selector_by_name(SELECTORS, element_name)
    element = find_element(driver, element_selector, wait_for_it=False)
    if expected_state == "selected":
        assert element.get_property("checked")


def generate_form_details(actor: Actor, *, custom_details: dict = None) -> dict:
    details = {
        "full name": str(uuid4()),
        "job title": "QA @ DIT",
        "email": actor.email,
        "phone": "0123456789",
        "company name": actor.company_name or "Automated test - company name",
        "website url": "https://browser.tests.com",
        "country": None,
        "organisation size": None,
        "comment": "This form was submitted by Automated test",
        "advanced food production": True,
        "lightweight structures": True,
        "rail infrastructure": True,
        "terms and conditions": True,
    }
    if custom_details:
        details.update(custom_details)
    logging.debug(f"Form details: {details}")
    return details


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]

    fill_out_input_fields(driver, form_selectors, details)
    fill_out_textarea_fields(driver, form_selectors, details)
    pick_option_from_autosuggestion(driver, form_selectors, details)
    tick_checkboxes_by_labels(driver, form_selectors, details)
    tick_captcha_checkbox(driver)

    take_screenshot(driver, "After filling out the contact us form")


def submit(driver: WebDriver):
    take_screenshot(driver, "Before submitting the contact us form")
    button = find_element(
        driver, SUBMIT_BUTTON, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the contact us form")


def should_not_see_section(driver: WebDriver, name: str):
    section = UNEXPECTED_ELEMENTS[name.lower()]
    for key, selector in section.items():
        check_if_element_is_not_visible(driver, selector, element_name=key)
