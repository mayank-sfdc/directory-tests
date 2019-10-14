# -*- coding: utf-8 -*-
"""Invest in Great Home Page Object."""
import logging
from typing import List

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import Service
from pages import ElementType, common_selectors
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_url,
    find_and_click_on_page_element,
    find_element,
    take_screenshot,
    visit_url,
)

NAME = "landing"
URL = URLs.INVEST_LANDING.absolute
SERVICE = Service.INVEST
TYPE = "landing"
PAGE_TITLE = "Invest in Great Britain - Home"

SELECTORS = {
    "benefits": {
        "self": Selector(By.ID, "benefits"),
        "heading": Selector(By.CSS_SELECTOR, "#benefits h2"),
        "sub-section headings": Selector(By.CSS_SELECTOR, "#benefits h3"),
        "text": Selector(By.CSS_SELECTOR, "#benefits p"),
        "image": Selector(By.CSS_SELECTOR, "#benefits img"),
    },
    "sectors": {
        "self": Selector(By.ID, "industries"),
        "heading": Selector(By.CSS_SELECTOR, "#industries h2"),
        "heading text": Selector(By.CSS_SELECTOR, "#industries h2 ~ div > p"),
        "first": Selector(By.CSS_SELECTOR, "#industries div:nth-child(1) > div > a"),
        "second": Selector(By.CSS_SELECTOR, "#industries div:nth-child(2) > div > a"),
        "third": Selector(By.CSS_SELECTOR, "#industries div:nth-child(3) > div > a"),
        "see more industries": Selector(By.ID, "see-more-industries"),
    },
    "high-potential opportunities": {
        "self": Selector(By.ID, "high-potential-opportunities"),
        "heading": Selector(By.CSS_SELECTOR, "#high-potential-opportunities h2"),
        "text": Selector(By.CSS_SELECTOR, "#high-potential-opportunities h2 ~ div > p"),
        "high productivity food production": Selector(
            By.CSS_SELECTOR, "#high-potential-opportunities div:nth-child(1) > div > a"
        ),
        "lightweight structures": Selector(
            By.CSS_SELECTOR, "#high-potential-opportunities div:nth-child(2) > div > a"
        ),
        "rail infrastructure": Selector(
            By.CSS_SELECTOR, "#high-potential-opportunities div:nth-child(2) > div > a"
        ),
    },
    "how we help": {
        "self": Selector(By.ID, "how-we-help"),
        "build connections - icon": Selector(
            By.CSS_SELECTOR, "#how-we-help ul > li:nth-child(1) > div > img"
        ),
        "build connections - text": Selector(
            By.CSS_SELECTOR, "#how-we-help ul > li:nth-child(1) > div > p"
        ),
        "apply for visas - icon": Selector(
            By.CSS_SELECTOR, "#how-we-help ul > li:nth-child(2) > div > img"
        ),
        "apply for visas - text": Selector(
            By.CSS_SELECTOR, "#how-we-help ul > li:nth-child(2) > div > p"
        ),
        "find grants - icon": Selector(
            By.CSS_SELECTOR, "#how-we-help ul > li:nth-child(3) > div > img"
        ),
        "find grants - text": Selector(
            By.CSS_SELECTOR, "#how-we-help ul > li:nth-child(3) > div > p"
        ),
        "get insights - icon": Selector(
            By.CSS_SELECTOR, "#how-we-help ul > li:nth-child(4) > div > img"
        ),
        "get insights - text": Selector(
            By.CSS_SELECTOR, "#how-we-help ul > li:nth-child(4) > div > p"
        ),
        "grow workforce - icon": Selector(
            By.CSS_SELECTOR, "#how-we-help ul > li:nth-child(5) > div > img"
        ),
        "grow workforce - text": Selector(
            By.CSS_SELECTOR, "#how-we-help ul > li:nth-child(5) > div > p"
        ),
    },
    "contact us": {
        "self": Selector(By.ID, "get-in-touch"),
        "heading": Selector(By.CSS_SELECTOR, "#get-in-touch h2"),
        "text": Selector(By.CSS_SELECTOR, "#get-in-touch p"),
        "speak to us": Selector(
            By.CSS_SELECTOR, "#get-in-touch a", type=ElementType.LINK
        ),
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER)
SELECTORS.update(common_selectors.INVEST_HERO)
SELECTORS.update(common_selectors.BREADCRUMBS)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def visit(driver: WebDriver):
    visit_url(driver, URL)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def clean_name(name: str) -> str:
    return name.split(" - ")[1].strip()


def open_industry(driver: WebDriver, industry_name: str):
    industry_name = clean_name(industry_name)
    selector = Selector(By.PARTIAL_LINK_TEXT, industry_name)
    logging.debug("Looking for: {}".format(industry_name))
    industry_link = find_element(
        driver, selector, element_name="Industry card", wait_for_it=False
    )
    industry_link.click()
    take_screenshot(driver, PAGE_TITLE + " after opening " + industry_name)


def open_guide(driver: WebDriver, guide_name: str):
    guide_name = clean_name(guide_name)
    selector = Selector(By.PARTIAL_LINK_TEXT, guide_name)
    logging.debug("Looking for: {}".format(guide_name))
    guide = find_element(driver, selector, element_name="Guide card", wait_for_it=False)
    guide.click()
    take_screenshot(driver, PAGE_TITLE + " after opening " + guide_name)


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, PAGE_TITLE + " after clicking on " + element_name)
