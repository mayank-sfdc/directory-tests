# -*- coding: utf-8 -*-
"""Domestic - SOO Domestic Long Contact us - Thank you for your enquiry."""
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import Selector, check_url, take_screenshot
from directory_tests_shared.enums import Service
from directory_tests_shared.settings import DOMESTIC_URL

NAME = "Long Domestic (Thank you for your enquiry)"
SERVICE = Service.DOMESTIC
TYPE = "Contact us"
URL = urljoin(DOMESTIC_URL, "contact/selling-online-overseas/success/")
PAGE_TITLE = "Welcome to great.gov.uk"

PDF_LINKS = Selector(By.CSS_SELECTOR, "#documents-section a.link")
SELECTORS = {
    "beta bar": {
        "self": Selector(By.ID, "header-beta-bar"),
        "beta bar": Selector(By.CSS_SELECTOR, "#header-beta-bar strong"),
        "feedback": Selector(By.CSS_SELECTOR, "#header-beta-bar a"),
    },
    "confirmation": {
        "itself": Selector(By.ID, "confirmation-section"),
        "heading": Selector(
            By.CSS_SELECTOR, "#confirmation-section div.heading-container"
        ),
    },
    "report this page": {
        "self": Selector(By.CSS_SELECTOR, "section.error-reporting"),
        "report link": Selector(By.CSS_SELECTOR, "section.error-reporting a"),
    },
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, PAGE_TITLE)
    check_url(driver, URL, exact_match=True)
