# -*- coding: utf-8 -*-
"""ERP - Save for later"""
from types import ModuleType
from typing import List, Union

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Actor,
    Selector,
    check_for_sections,
    check_url,
    fill_out_input_fields,
    find_and_click_on_page_element,
    go_to_url,
    submit_form,
    take_screenshot,
)
from pages.erp import save_for_later_progress_saved

NAME = "Save for later"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = URLs.ERP_SAVE_FOR_LATER.absolute
PAGE_TITLE = ""

SELECTORS = {
    "form": {
        "heading": Selector(By.CSS_SELECTOR, "#content h1"),
        "description": Selector(By.CSS_SELECTOR, "#content h1 ~ p"),
        "form itself": Selector(By.CSS_SELECTOR, "form[method=post]"),
        "email": Selector(By.ID, "id_email", type=ElementType.INPUT),
        "submit": Selector(
            By.CSS_SELECTOR,
            "form[method=post] button[type=submit]",
            type=ElementType.SUBMIT,
            next_page=save_for_later_progress_saved,
        ),
    }
}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_BACK)
SELECTORS.update(common_selectors.ERP_FOOTER)


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)


def generate_form_details(actor: Actor) -> dict:
    result = {"email": actor.email}
    return result


def fill_out(driver: WebDriver, details: dict):
    form_selectors = SELECTORS["form"]
    fill_out_input_fields(driver, form_selectors, details)
    take_screenshot(driver, "After filling out the form")


def submit(driver: WebDriver) -> Union[ModuleType, None]:
    return submit_form(driver, SELECTORS["form"])
