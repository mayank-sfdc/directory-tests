# -*- coding: utf-8 -*-
"""ExRed Footer Page Object."""
import logging

from selenium import webdriver

from utils import assertion_msg, selenium_action, take_screenshot

NAME = "ExRed Footer"
URL = None

SECTIONS = {
    "export readiness": {
        "label": "#footer-links-2",
        "new": "#footer a[href='/new']",
        "occasional": "#footer a[href='/occasional']",
        "regular": "#footer a[href='/regular']",
        "i'm new to exporting": "#footer a[href='/new']",
        "i export occasionally": "#footer a[href='/occasional']",
        "i'm a regular exporter": "#footer a[href='/regular']"
    },
    "guidance": {
        "label": "#footer-links-3",
        "market research": "#footer a[href='/market-research']",
        "customer insight": "#footer a[href='/customer-insight']",
        "finance": "#footer a[href='/finance']",
        "business planning": "#footer a[href='/business-planning']",
        "getting paid": "#footer a[href='/getting-paid']",
        "operations and compliance": "#footer a[href='/operations-and-compliance']"
    },
    "services": {
        "label": "#footer-links-4",
        "find a buyer": "#footer > nav > div:nth-child(4) > ul > li:nth-child(1) > a",
        "selling online overseas": "#footer > nav > div:nth-child(4) > ul > li:nth-child(2) > a",
        "export opportunities": "#footer a[href='/export-opportunities']",
        "get finance": "#footer a[href='/get-finance']",
        "events": "#footer > nav > div:nth-child(4) > ul > li:nth-child(5) > a"
    },
    "general links": {
        "part of great.gov.uk": "#footer > .site-links > ul > li:nth-child(1) > a",
        "about": "#footer > .site-links > ul > li:nth-child(2) > a",
        "contact us": "#footer > .site-links > ul > li:nth-child(3) > a",
        "privacy and cookies": "#footer > .site-links > ul > li:nth-child(4) > a",
        "terms and conditions": "#footer > .site-links > ul > li:nth-child(5) > a",
        "department for international trade": "#footer > .site-links > ul > li:nth-child(6) > a"
    }
}


def should_see_all_menus(driver: webdriver):
    for section in SECTIONS:
        for name, selector in SECTIONS[section].items():
            logging.debug(
                "Looking for '%s' link in '%s' section with '%s' selector",
                name, section, selector)
            with selenium_action(
                    driver, "Could not find '%s link' using '%s'",
                    name, selector):
                element = driver.find_element_by_css_selector(selector)
            with assertion_msg(
                    "It looks like '%s' in '%s' section is not visible",
                    name, section):
                assert element.is_displayed()
        logging.debug("All elements in '%s' section are visible", section)
    logging.debug(
        "All expected sections on %s are visible", NAME)


def should_see_link_to(driver: webdriver, section: str, item_name: str):
    item_selector = SECTIONS[section.lower()][item_name.lower()]
    with selenium_action(
            driver, "Could not find '%s' using '%s'", item_name,
            item_selector):
        menu_item = driver.find_element_by_css_selector(item_selector)
    with assertion_msg(
            "It looks like '%s' in '%s' section is not visible", item_name,
            section):
        assert menu_item.is_displayed()


def open(driver: webdriver, group: str, element: str):
    link = SECTIONS[group.lower()][element.lower()]
    button = driver.find_element_by_css_selector(link)
    assert button.is_displayed()
    button.click()
    take_screenshot(
        driver, NAME + " after clicking on: %s link".format(element))
