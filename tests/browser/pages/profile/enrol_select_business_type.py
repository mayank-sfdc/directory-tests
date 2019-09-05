# -*- coding: utf-8 -*-
"""Profile - Enrol - Select your business type"""
import logging
from types import ModuleType
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import ElementType, Services, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    choose_one_form_option,
    find_and_click_on_page_element,
    find_element,
    get_selectors,
    go_to_url,
    take_screenshot,
)
from pages.profile import (
    enrol_enter_your_business_email_and_set_password,
    enrol_sole_trader_enter_your_email_and_set_password,
    enrol_uk_taxpayer_enter_your_email_and_set_password,
    enrol_you_cannot_create_account,
)
from settings import DIRECTORY_UI_PROFILE_URL

NAME = "Select your business type"
SERVICE = Services.PROFILE
TYPE = "Enrol"
URL = urljoin(DIRECTORY_UI_PROFILE_URL, "enrol/business-type/")
PAGE_TITLE = ""

SELECTORS = {
    "enrolment progress bar": {"itself": Selector(By.ID, "progress-column")},
    "form": {
        "itself": Selector(By.CSS_SELECTOR, "section form"),
        "ltd, plc or royal charter": Selector(
            By.CSS_SELECTOR,
            "input[value='companies-house-company'] ~ label",
            type=ElementType.RADIO,
            is_visible=False,
        ),
        "sole trader or other type of business": Selector(
            By.CSS_SELECTOR,
            "input[value='non-companies-house-company'] ~ label",
            type=ElementType.RADIO,
            is_visible=False,
        ),
        "uk taxpayer": Selector(
            By.CSS_SELECTOR,
            "input[value='not-company'] ~ label",
            type=ElementType.RADIO,
            is_visible=False,
        ),
        "overseas company": Selector(
            By.CSS_SELECTOR,
            "input[value='overseas-company'] ~ label",
            type=ElementType.RADIO,
            is_visible=False,
        ),
        "submit": Selector(
            By.CSS_SELECTOR, "form button.button", type=ElementType.BUTTON
        ),
    },
}
SELECTORS.update(common_selectors.HEADER)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.FOOTER)

POs = {
    "ltd, plc or royal charter": enrol_enter_your_business_email_and_set_password,
    "sole trader or other type of business": enrol_sole_trader_enter_your_email_and_set_password,
    "uk taxpayer": enrol_uk_taxpayer_enter_your_email_and_set_password,
    "overseas company": enrol_you_cannot_create_account,
}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def should_see_form_choices(driver: WebDriver, names: List[str]):
    radio_selectors = get_selectors(SELECTORS["form"], ElementType.RADIO)
    for name in names:
        radio_selector = radio_selectors[name.lower()]
        find_element(driver, radio_selector, element_name=name, wait_for_it=False)
    logging.debug(
        f"All expected form choices: '{names}' are visible on " f"{driver.current_url}"
    )


def pick_radio_option_and_submit(driver: WebDriver, name: str) -> ModuleType:
    radio_selectors = get_selectors(SELECTORS["form"], ElementType.RADIO)
    choose_one_form_option(driver, radio_selectors, name)
    take_screenshot(driver, "Before submitting the form")
    find_and_click_on_page_element(driver, SELECTORS, "submit", wait_for_it=False)
    take_screenshot(driver, "After submitting the form")
    return POs[name.lower()]
