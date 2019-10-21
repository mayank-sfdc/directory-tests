# -*- coding: utf-8 -*-
"""ERP - User type"""
from types import ModuleType
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_form_choices,
    check_url,
    go_to_url,
    pick_one_option_and_submit,
    take_screenshot,
)
from pages.erp import (
    consumer_product_search,
    developing_country_select,
    triage_import_from_overseas,
)

NAME = "User type"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = URLs.ERP_TRIAGE_USER_TYPE.absolute
PAGE_TITLE = ""

SUBMIT_BUTTON = Selector(
    By.CSS_SELECTOR, "#content > form button.govuk-button", type=ElementType.BUTTON
)
SELECTORS = {
    "form": {
        "form itself": Selector(By.CSS_SELECTOR, "#content form[method='post']"),
        "uk business": Selector(
            By.CSS_SELECTOR,
            "input[value='UK_BUSINESS']",
            type=ElementType.RADIO,
            is_visible=False,
            next_page=triage_import_from_overseas,
        ),
        "uk consumer": Selector(
            By.CSS_SELECTOR,
            "input[value='UK_CONSUMER']",
            type=ElementType.RADIO,
            is_visible=False,
            next_page=consumer_product_search,
        ),
        "exporter from developing country": Selector(
            By.CSS_SELECTOR,
            "input[value='DEVELOPING_COUNTRY_COMPANY']",
            type=ElementType.RADIO,
            is_visible=False,
            next_page=developing_country_select,
        ),
        "submit": SUBMIT_BUTTON,
    }
}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_BACK)
SELECTORS.update(common_selectors.ERP_BREADCRUMBS)
SELECTORS.update(common_selectors.ERP_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def should_see_form_choices(driver: WebDriver, names: List[str]):
    check_form_choices(driver, SELECTORS["form"], names)


def pick_radio_option_and_submit(driver: WebDriver, name: str) -> ModuleType:
    return pick_one_option_and_submit(driver, SELECTORS["form"], name)
