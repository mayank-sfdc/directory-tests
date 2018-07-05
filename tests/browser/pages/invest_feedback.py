# -*- coding: utf-8 -*-
"""Contact Us - Feedback Page Object."""
import logging
from urllib.parse import urljoin

from utils import take_screenshot

from pages import Executor, visit_url
from pages.common_actions import check_title, check_url
from settings import DIRECTORY_CONTACT_US_UI_URL

URL = urljoin(DIRECTORY_CONTACT_US_UI_URL, "directory/")
PAGE_TITLE = "Contact us - great.gov.uk"


def visit(executor: Executor, *, first_time: bool = False):
    visit_url(executor, URL)


def should_be_here(executor: Executor):
    check_title(executor, PAGE_TITLE, exact_match=True)
    check_url(executor, URL, exact_match=True)
    take_screenshot(executor, PAGE_TITLE)
    logging.debug("All expected elements are visible on '%s' page", PAGE_TITLE)
