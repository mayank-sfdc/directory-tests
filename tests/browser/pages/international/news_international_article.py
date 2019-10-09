# -*- coding: utf-8 -*-
"""great.gov.uk International EU Exit News Article page"""
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from directory_tests_shared import URLs
from directory_tests_shared.enums import Service
from pages import common_selectors
from pages.common_actions import (
    Selector,
    check_url,
    find_and_click_on_page_element,
    find_elements,
    take_screenshot,
)

NAME = "International EU Exit news"
SERVICE = Service.INTERNATIONAL
TYPE = "article"
URL = URLs.INTERNATIONAL_BREXIT_NEWS.absolute
PAGE_TITLE = ""


TAGS = Selector(By.CSS_SELECTOR, "ul.tag-list a")
RELATED_ARTICLES = Selector(
    By.CSS_SELECTOR, "#article > article > div > div > div.column-quarter ul a"
)
SELECTORS = {
    "share menu": {
        "itself": Selector(By.CSS_SELECTOR, "ul.sharing-links"),
        "twitter": Selector(By.ID, "share-twitter"),
        "facebook": Selector(By.ID, "share-facebook"),
        "linkedin": Selector(By.ID, "share-linkedin"),
        "email": Selector(By.ID, "share-email"),
    },
    "article": {
        "itself": Selector(By.ID, "article"),
        "breadcrumbs": Selector(By.CSS_SELECTOR, ".breadcrumbs"),
        "great.gov.uk": Selector(
            By.CSS_SELECTOR, ".breadcrumbs a[href='/international/']"
        ),
        "updates for non-uk companies on eu exit": Selector(
            By.CSS_SELECTOR, ".breadcrumbs a[href='/international/eu-exit-news/']"
        ),
        "header": Selector(By.CSS_SELECTOR, "#article h1"),
        "lede": Selector(By.CSS_SELECTOR, "#article p.lede"),
        "updates for companies on eu exit": Selector(
            By.CSS_SELECTOR, "article footer nav > div:nth-child(1) a"
        ),
        "back to top": Selector(
            By.CSS_SELECTOR, "article footer nav > div:nth-child(2) a"
        ),
    },
    "tag list": {"itself": Selector(By.CSS_SELECTOR, "ul.tag-list"), "tags": TAGS},
    "related content": {
        "itself": Selector(
            By.CSS_SELECTOR, "#article > article > div > div > div.column-quarter"
        ),
        "related articles": RELATED_ARTICLES,
    },
}
SELECTORS.update(common_selectors.INTERNATIONAL_HEADER)
SELECTORS.update(common_selectors.BETA_BAR)
SELECTORS.update(common_selectors.ERROR_REPORTING)
SELECTORS.update(common_selectors.INTERNATIONAL_FOOTER)


def should_be_here(driver: WebDriver):
    take_screenshot(driver, NAME)
    check_url(driver, URL, exact_match=False)


def open_any_tag(driver: WebDriver) -> str:
    links = find_elements(driver, TAGS)
    assert len(links) > 0
    link = links[random.randint(1, len(links)) - 1]
    tag = link.text.lower()
    link.click()
    return tag


def open_any_related_article(driver: WebDriver):
    links = find_elements(driver, RELATED_ARTICLES)
    assert len(links) > 0
    links[random.randint(1, len(links)) - 1].click()


def click_on_page_element(driver: WebDriver, element_name: str):
    find_and_click_on_page_element(driver, SELECTORS, element_name)
    take_screenshot(driver, NAME + " after clicking on " + element_name)
