# -*- coding: utf-8 -*-
"""Events Event Page Object."""

import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared.enums import Service
from pages.common_actions import (
    Selector,
    check_url,
    take_screenshot,
    wait_for_visibility,
)
from directory_tests_shared.settings import EVENTS_URL

NAME = "Event"
SERVICE = Service.EVENTS
TYPE = "event"
URL = urljoin(EVENTS_URL, "")
GREAT_LOGO = Selector(By.CSS_SELECTOR, "div.event-logo")
SELECTORS = {
    "general": {"great.gov.uk logo": GREAT_LOGO},
    "breadcrumbs": Selector(By.CSS_SELECTOR, ".breadcrumbs div>a"),
}


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    wait_for_visibility(driver, GREAT_LOGO, time_to_wait=15)
    check_url(driver, URL, exact_match=False)
    logging.debug("All expected elements are visible on '%s' page", NAME)
