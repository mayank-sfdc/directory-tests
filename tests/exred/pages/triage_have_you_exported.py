# -*- coding: utf-8 -*-
"""ExRed Triage 2nd Question Page Object."""
import logging

from selenium import webdriver

from utils import assertion_msg, get_absolute_url, take_screenshot

NAME = "ExRed Triage - have you exported before"
URL = get_absolute_url(NAME)

YES_CHECKBOX = "#id_EXPORTED_BEFORE-exported_before > li:nth-child(1) > label"
NO_CHECKBOX = "#id_EXPORTED_BEFORE-exported_before > li:nth-child(2) > label"
CONTINUE_BUTTON = ".exred-triage-form button.button"
PREVIOUS_STEP_BUTTON = ".exred-triage-form button.previous-step"
BACK_TO_HOME_LINK = ".home-link a"
EXPECTED_ELEMENTS = {
    "question": "#id_triage_wizard_form_view-current_step ~ li > label",
    "yes checkbox": YES_CHECKBOX,
    "no checkbox": NO_CHECKBOX,
    "continue button": CONTINUE_BUTTON,
    "previous step button": PREVIOUS_STEP_BUTTON,
    "back to home link": BACK_TO_HOME_LINK
}


def should_be_here(driver: webdriver):
    for element_name, element_selector in EXPECTED_ELEMENTS.items():
        element = driver.find_element_by_css_selector(element_selector)
        with assertion_msg(
                "It looks like '%s' element is not visible on %s",
                element_name, NAME):
            assert element.is_displayed()
    take_screenshot(driver, NAME)
    logging.debug("All expected elements are visible on '%s' page", NAME)


def select_yes(driver: webdriver):
    yes = driver.find_element_by_css_selector(YES_CHECKBOX)
    yes.click()
    take_screenshot(driver, NAME)


def select_no(driver: webdriver):
    no = driver.find_element_by_css_selector(NO_CHECKBOX)
    no.click()
    take_screenshot(driver, NAME)


def submit(driver: webdriver):
    button = driver.find_element_by_css_selector(CONTINUE_BUTTON)
    button.click()
    take_screenshot(driver, NAME + " after submitting")
