# -*- coding: utf-8 -*-
"""Contact Us - Feedback Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.remote.webdriver import WebDriver

from pages import Services
from pages.common_actions import check_url, take_screenshot, visit_url
from directory_tests_shared.settings import CONTACT_US_URL

NAME = "Feedback"
SERVICE = Services.INVEST
TYPE = "contact"
URL = urljoin(CONTACT_US_URL, "feedback/")
PAGE_TITLE = "Contact us - great.gov.uk"
SELECTORS = {}


def visit(driver: WebDriver):
    visit_url(driver, URL)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)
