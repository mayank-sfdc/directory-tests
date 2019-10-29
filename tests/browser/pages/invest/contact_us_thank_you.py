# -*- coding: utf-8 -*-
"""Invest in Great - Thank you for your message Page Object."""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import PageType, Service
from pages.common_actions import Selector, check_url, take_screenshot, visit_url

NAME = "Thank you for your message"
SERVICE = Service.INVEST
TYPE = PageType.THANK_YOU
URL = URLs.INVEST_CONTACT_SUCCESS.absolute
PAGE_TITLE = ""
SELECTORS = {
    "hero": {"itself": Selector(By.CSS_SELECTOR, "section.hero")},
    "success message": {"itself": Selector(By.CSS_SELECTOR, "section.contact-success")},
}


def visit(driver: WebDriver):
    visit_url(driver, URL)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)
