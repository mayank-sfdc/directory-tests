# -*- coding: utf-8 -*-
"""Domestic Common Advice Page Object."""
import logging
import random
from typing import List
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import Service
from pages import ElementType
from pages.common_actions import (
    Selector,
    check_for_sections,
    check_if_element_is_visible,
    check_url,
    find_elements,
    go_to_url,
    take_screenshot,
    wait_for_page_load_after_action,
)

NAME = "Advice"
TYPE = "article list"
SERVICE = Service.DOMESTIC
URL = URLs.DOMESTIC_ADVICE.absolute
PAGE_TITLE = "Welcome to great.gov.uk"
NAMES = [
    "Create an export plan",
    "Find an export market",
    "Define route to market",
    "Get export finance",
    "Manage payment for export orders",
    "Prepare to do business in a foreign country",
    "Manage legal and ethical compliance",
    "Prepare for export procedures and logistics",
]
SubURLs = {
    "create an export plan": urljoin(URL, "create-an-export-plan/"),
    "find an export market": urljoin(URL, "find-an-export-market/"),
    "define route to market": urljoin(URL, "define-route-to-market/"),
    "get export finance": urljoin(URL, "get-export-finance-and-funding/"),
    "manage payment for export orders": urljoin(
        URL, "manage-payment-for-export-orders/"
    ),
    "prepare to do business in a foreign country": urljoin(
        URL, "prepare-to-do-business-in-a-foreign-country/"
    ),
    "manage legal and ethical compliance": urljoin(
        URL, "manage-legal-and-ethical-compliance/"
    ),
    "prepare for export procedures and logistics": urljoin(
        URL, "prepare-for-export-procedures-and-logistics/"
    ),
}

ARTICLE_LINKS = Selector(
    By.CSS_SELECTOR, "#article-list-page li.article a", type=ElementType.LINK
)
SELECTORS = {
    "hero": {
        "itself": Selector(By.ID, "hero"),
        "heading": Selector(By.ID, "hero-heading"),
    },
    "breadcrumbs": {
        "itself": Selector(By.CSS_SELECTOR, "nav.breadcrumbs"),
        "links": Selector(By.CSS_SELECTOR, "nav.breadcrumbs a"),
    },
    "list of articles": {
        "itself": Selector(By.ID, "article-list-page"),
        "articles": ARTICLE_LINKS,
    },
    "error reporting": {
        "itself": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "link": Selector(By.ID, "error-reporting-section-contact-us"),
    },
}


def clean_name(name: str) -> str:
    return name.split(" - ")[1].strip()


def visit(driver: WebDriver, *, page_name: str = None):
    take_screenshot(driver, page_name or NAME)
    url = SubURLs[page_name.lower()] if page_name else URL
    go_to_url(driver, url, page_name or NAME)


def should_be_here(driver: WebDriver, *, page_name: str):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)


def should_see_sections(driver: WebDriver, names: List[str]):
    check_for_sections(driver, all_sections=SELECTORS, sought_sections=names)


def open_any_article(driver: WebDriver) -> str:
    article_links = find_elements(driver, ARTICLE_LINKS)
    error = f"Expected to see at least 1 article but found none on {driver.current_url}"
    assert article_links, error
    link = random.choice(article_links)
    link_text = link.text
    check_if_element_is_visible(link, element_name=link_text)
    with wait_for_page_load_after_action(driver):
        link.click()
    return link_text
