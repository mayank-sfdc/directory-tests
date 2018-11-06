# -*- coding: utf-8 -*-
"""Events Home Page Object."""
import logging
from urllib.parse import urljoin

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages.common_actions import (
    Selector,
    check_url,
    go_to_url,
    take_screenshot,
    wait_for_visibility,
)
from settings import EVENTS_UI_URL

NAME = "Home"
SERVICE = "Events"
TYPE = "home"
URL = urljoin(EVENTS_UI_URL, "")
GREAT_LOGO = Selector(By.CSS_SELECTOR, "#portal-top > h1 > a > img")
SELECTORS = {"general": {"great.gov.uk logo": GREAT_LOGO}}


def visit(driver: WebDriver, *, first_time: bool = False):
    go_to_url(driver, URL, NAME, first_time=first_time)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    wait_for_visibility(driver, GREAT_LOGO, time_to_wait=15)
    check_url(driver, URL, exact_match=True)
    logging.debug("All expected elements are visible on '%s' page", NAME)
