# -*- coding: utf-8 -*-
"""EORI Home Page Object."""
import logging

from selenium.webdriver.remote.webdriver import WebDriver

from pages import Services
from pages.common_actions import check_url, go_to_url, take_screenshot

NAME = "Home"
SERVICE = Services.EORI
TYPE = "home"
URL = "https://www.gov.uk/eori"
SELECTORS = {}


def visit(driver: WebDriver):
    go_to_url(driver, URL, NAME)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL)
    logging.debug("All expected elements are visible on '%s' page", NAME)
