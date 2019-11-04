# -*- coding: utf-8 -*-
"""ERP - Product Search"""
import logging
from random import choice
from types import BuiltinFunctionType, ModuleType
from typing import List, Tuple

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from directory_tests_shared.utils import evaluate_comparison
from pages import common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_element,
    find_elements,
    find_selector_by_name,
    go_to_url,
    is_element_present,
    take_screenshot,
    wait_for_page_load_after_action,
)
from pages.erp import product_detail

NAME = "Product search"
SERVICE = Service.ERP
TYPE = PageType.FORM
URL = None
PAGE_TITLE = ""
SubURLs = {
    f"{NAME} (Developing country)": URLs.ERP_DEVELOPING_COUNTRY_PRODUCT_SEARCH.absolute,
    f"{NAME} (UK business)": URLs.ERP_BUSINESS_PRODUCT_SEARCH.absolute,
    f"{NAME} (UK consumer)": URLs.ERP_CONSUMER_PRODUCT_SEARCH.absolute,
    f"{NAME} (UK importer)": URLs.ERP_IMPORTER_PRODUCT_SEARCH.absolute,
}
NAMES = list(SubURLs.keys())

PRODUCT_CATEGORIES_SELECTOR = Selector(By.CSS_SELECTOR, "#content form a.govuk-link")
PRODUCT_CODES_SELECTOR = Selector(
    By.CSS_SELECTOR, "button.search-product-select-button"
)
SELECTORS = {}
SELECTORS.update(common_selectors.ERP_HEADER)
SELECTORS.update(common_selectors.ERP_BETA)
SELECTORS.update(common_selectors.ERP_BACK)
SELECTORS.update(common_selectors.ERP_SEARCH_FORM)
SELECTORS.update(common_selectors.ERP_SEARCH_RESULTS)
SELECTORS.update(common_selectors.ERP_HIERARCHY_CODES)
SELECTORS.update(common_selectors.ERP_FOOTER)


def visit(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, page_name or NAME)
    url = SubURLs[page_name]
    go_to_url(driver, url, page_name or NAME)


def should_be_here(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, page_name or NAME)
    url = SubURLs[page_name]
    check_url(driver, url, exact_match=False)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def drill_down_hierarchy_tree(
    driver: WebDriver, *, use_expanded_category: bool = False
) -> ModuleType:
    if use_expanded_category:
        last_expanded_level = Selector(
            By.CSS_SELECTOR, "li.app-hierarchy-tree__parent--open:last-of-type"
        )
        last_opened_levels = find_elements(driver, last_expanded_level)
        opened_first_level = last_opened_levels[-1]
        first_id = opened_first_level.get_property("id")
        logging.debug(f"Commencing from: {first_id} -> {opened_first_level.text}")
    else:
        first_level_selector = Selector(
            By.CSS_SELECTOR, "ul.app-hierarchy-tree li.app-hierarchy-tree__section"
        )
        first_level = find_elements(driver, first_level_selector)
        first = choice(first_level)
        first_id = first.get_property("id")

        with wait_for_page_load_after_action(driver):
            logging.debug(f"First level: {first_id} -> {first.text}")
            first.click()

    select_code_selector = Selector(By.CSS_SELECTOR, "div.app-hierarchy-button")
    select_product_codes_present = is_element_present(driver, select_code_selector)
    logging.debug(
        f"Is Select product code button present: {select_product_codes_present}"
    )

    current_parent_id = first_id
    while not select_product_codes_present:
        child_level_selector = Selector(
            By.CSS_SELECTOR, f"#{current_parent_id} ul li.app-hierarchy-tree__chapter"
        )
        child_level = find_elements(driver, child_level_selector)
        if not child_level:
            logging.debug("No more child level elements")
            break
        logging.debug(f"Child elements of '{current_parent_id}' are: {child_level}")
        child = choice(child_level)
        current_parent_id = child.get_property("id")

        with wait_for_page_load_after_action(driver, timeout=5):
            logging.debug(f"Selected child: {current_parent_id}")
            child.click()

        logging.debug(
            f"Is Select product code button present: {select_product_codes_present}"
        )
        select_product_codes_present = is_element_present(driver, select_code_selector)

    if select_product_codes_present:
        select_codes = find_elements(driver, select_code_selector)
        select = choice(select_codes)
        select_id = select.get_property("id")
        logging.debug(f"Selected product code: {select_id}")
        with wait_for_page_load_after_action(driver, timeout=5):
            select.click()
    else:
        logging.error("Strange! Could not find 'Select' product codes button")

    return product_detail


def search(driver: WebDriver, phrase: str):
    search_input = find_element(driver, find_selector_by_name(SELECTORS, "search"))
    search_button = find_element(
        driver, find_selector_by_name(SELECTORS, "search button")
    )
    search_input.clear()
    search_input.send_keys(phrase)
    search_button.click()


def should_see_number_of_product_codes_to_select(
    driver: WebDriver, comparison_details: Tuple[BuiltinFunctionType, int]
):
    found_elements = find_elements(driver, PRODUCT_CODES_SELECTOR)
    evaluate_comparison(
        "number of product codes to be", len(found_elements), comparison_details
    )


def should_see_number_of_product_categories_to_expand(
    driver: WebDriver, comparison_details: Tuple[BuiltinFunctionType, int]
):
    found_elements = find_elements(driver, PRODUCT_CATEGORIES_SELECTOR)
    evaluate_comparison(
        "number of product categories to be", len(found_elements), comparison_details
    )


def click_on_random_search_result(driver: WebDriver, result_type: str):
    result_type_selectors = {
        "code": PRODUCT_CODES_SELECTOR,
        "category": PRODUCT_CATEGORIES_SELECTOR,
    }
    found_elements = find_elements(driver, result_type_selectors[result_type.lower()])
    search_result = choice(found_elements)
    value = search_result.get_property("value")
    href = search_result.get_attribute("href")
    logging.debug(f"Will click on {result_type}: {value or href}")
    with wait_for_page_load_after_action(driver, timeout=5):
        search_result.click()
