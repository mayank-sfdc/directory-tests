# -*- coding: utf-8 -*-
"""ExRed Common Case Study Page Object."""
import logging

from selenium import webdriver

from utils import assertion_msg, find_element, selenium_action, take_screenshot

NAME = "ExRed Common Case Study"
URL = None


SHARE_WIDGET = "#top > ul.sharing-links"
CASE_STUDIES = {
    1: {
        "breadcrumb": "#content > div > p.breadcrumbs > span.current",
        "title": "#top > h1",
        "type": "#top > p.type",
        "description": "#top > p.description",
    },
    2: {
        "breadcrumb": "#content > div > p.breadcrumbs > span.current",
        "title": "#top > h1",
        "type": "#top > p.type",
        "description": "#top > p.description",
    },
    3: {
        "breadcrumb": "#content > div > p.breadcrumbs > span.current",
        "title": "#top > h1",
        "type": "#top > p.type",
        "description": "#top > p.description",
    }
}


def should_be_here(
        driver: webdriver, case_study_number: int, *, title: str = None):
    take_screenshot(driver, NAME)
    for element_name, element_selector in CASE_STUDIES[case_study_number].items():
        element = find_element(
            driver, by_css=element_selector, element_name=element_name)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
        if title:
            if element_name in ["title", "breadcrumb"]:
                element = find_element(
                    driver, by_css=element_selector, element_name=element_name)
                with assertion_msg(
                        "Expected case study %s to be '%s' but got '%s'",
                        element_name, title, element.text):
                    assert element.text.lower() == title.lower()
    logging.debug("All expected elements are visible on '%s' page", NAME)


def should_see_share_widget(driver: webdriver):
    share_widget = find_element(
        driver, by_css=SHARE_WIDGET, element_name="Share widget")
    with assertion_msg(
            "Share widget is not visible on: %s", driver.current_url):
        assert share_widget.is_displayed()
