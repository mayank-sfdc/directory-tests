# -*- coding: utf-8 -*-
"""Profile - Enrol - Sole Trader Enter your details"""
import logging
from types import ModuleType
from typing import List
from uuid import uuid4

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType
from pages.common_actions import (
    Actor,
    Selector,
    check_for_sections,
    check_url,
    fill_out_input_fields,
    find_and_click_on_page_element,
    go_to_url,
    take_screenshot,
    tick_checkboxes,
)
from pages.profile import enrol_account_created

NAME = "Enter your details (Sole trader or other type of business)"
SERVICE = Service.PROFILE
TYPE = PageType.FORM
URL = URLs.PROFILE_ENROL_NON_CH_COMPANY_ENTER_PERSONAL_DETAILS.absolute
PAGE_TITLE = ""

SELECTORS = {
    "enrolment progress bar": {"itself": Selector(By.ID, "progress-column")},
    "your business details": {
        "itself": Selector(By.ID, "business-details-information-box"),
        "company name": Selector(By.ID, "company-name"),
        "company address": Selector(By.ID, "company-address"),
        "change business details": Selector(
            By.ID, "change-business-details", type=ElementType.LINK
        ),
    },
    "enter your details form": {
        "itself": Selector(By.CSS_SELECTOR, "section form"),
        "heading": Selector(By.CSS_SELECTOR, "h1"),
        "first name": Selector(
            By.ID, "id_personal-details-given_name", type=ElementType.INPUT
        ),
        "last name": Selector(
            By.ID, "id_personal-details-family_name", type=ElementType.INPUT
        ),
        "job title": Selector(
            By.ID, "id_personal-details-job_title", type=ElementType.INPUT
        ),
        "phone number": Selector(
            By.ID, "id_personal-details-phone_number", type=ElementType.INPUT
        ),
        "background checks": Selector(
            By.ID,
            "id_personal-details-confirmed_is_company_representative-label",
            type=ElementType.CHECKBOX,
            is_visible=False,
        ),
        "submit": Selector(
            By.CSS_SELECTOR, "form button.button", type=ElementType.BUTTON
        ),
    },
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)
    msg = f"Got 404 on {driver.current_url}"
    assert "This page cannot be found" not in driver.page_source, msg


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def generate_form_details(actor: Actor) -> dict:
    result = {
        "first name": actor.alias,
        "last name": str(uuid4()),
        "job title": "DIT AUTOMATED TESTS",
        "phone number": "07123456789",
        "background checks": True,
    }
    logging.debug(f"Generated form details: {result}")
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["enter your details form"]
    fill_out_input_fields(driver, form_selectors, details)
    tick_checkboxes(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> ModuleType:
    take_screenshot(driver, "Before submitting the form")
    find_and_click_on_page_element(driver, SELECTORS, "submit", wait_for_it=False)
    take_screenshot(driver, "After submitting the form")
    return enrol_account_created
