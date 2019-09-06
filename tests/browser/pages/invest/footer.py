# -*- coding: utf-8 -*-
"""Invest - Page Footer."""
import logging

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from pages import Services
from pages.common_actions import (
    Selector,
    check_hash_of_remote_file,
    find_and_click_on_page_element,
    find_element,
    scroll_to,
    take_screenshot,
)
from settings import MD5_CHECKSUM_GREAT_LOGO

NAME = "Footer"
URL = None
SERVICE = Services.INVEST
TYPE = "footer"

UK_GOV_LOGO = Selector(By.ID, "great-footer-great-logo")
SELECTORS = {
    "logos": {
        "uk gov": UK_GOV_LOGO,
        "invest in great": Selector(By.CSS_SELECTOR, "#invest-footer img:nth-child(2)"),
    },
    "links": {
        "home": Selector(By.CSS_SELECTOR, "#invest-footer a[href='/']"),
        "industries": Selector(
            By.CSS_SELECTOR, "#invest-footer a[href='/industries/']"
        ),
        "uk setup guide": Selector(
            By.CSS_SELECTOR, "#invest-footer a[href='/uk-setup-guide/']"
        ),
        "contact us": Selector(By.CSS_SELECTOR, "#invest-footer a[href='/contact/']"),
        "part of great.gov.uk": Selector(
            By.CSS_SELECTOR,
            "#invest-footer div.footer-sub-links-list li:nth-child(1) a",
        ),
        "terms and conditions": Selector(
            By.CSS_SELECTOR,
            "#invest-footer div.footer-sub-links-list li:nth-child(2) a",
        ),
        "privacy and cookies": Selector(
            By.CSS_SELECTOR,
            "#invest-footer div.footer-sub-links-list li:nth-child(3) a",
        ),
        "department for international trade": Selector(
            By.CSS_SELECTOR,
            "#invest-footer div.footer-sub-links-list li:nth-child(4) a",
        ),
    },
}


def click_on_page_element(driver: WebDriver, element: str):
    """Open specific element that belongs to the group."""
    find_and_click_on_page_element(driver, SELECTORS, element)
    take_screenshot(driver, NAME + " after clicking on: {} link".format(element))


def check_logo(driver: WebDriver):
    logo = find_element(driver, UK_GOV_LOGO)
    scroll_to(driver, logo)
    src = logo.get_attribute("src")
    check_hash_of_remote_file(MD5_CHECKSUM_GREAT_LOGO, src)
    logging.debug("%s has correct MD5sum %s", src, MD5_CHECKSUM_GREAT_LOGO)
