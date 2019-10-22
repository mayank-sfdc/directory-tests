# -*- coding: utf-8 -*-
"""Common PageObject actions."""
import hashlib
import logging
import random
import string
import sys
import time
import traceback
import uuid
from collections import defaultdict, namedtuple
from contextlib import contextmanager
from datetime import datetime
from os import path
from types import ModuleType
from typing import Dict, List, Union
from urllib.parse import urlparse

import requests
from behave.runner import Context
from retrying import retry
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from directory_tests_shared.settings import BARRED_USERS, TAKE_SCREENSHOTS
from pages import ElementType

ScenarioData = namedtuple("ScenarioData", ["actors"])
Actor = namedtuple(
    "Actor",
    [
        "alias",
        "email",
        "password",
        "company_name",
        "article_category",
        "visited_articles",
        "case_study_title",
        "email_confirmation_link",
        "email_confirmation_code",
        "registered",
        "visited_page",
        "last_tag",
        "element_details",
        "forms_data",
    ],
)
Selector = namedtuple(
    "Selector",
    [
        "by",
        "value",
        "in_desktop",
        "in_mobile",
        "in_horizontal",
        "type",
        "is_visible",
        "group_id",
        "autocomplete_callback",
        "wait_after_click",
        "next_page",
    ],
)

# define default values for various named tuples
Actor.__new__.__defaults__ = (None,) * len(Actor._fields)
Selector.__new__.__defaults__ = (
    None,
    None,
    True,
    True,
    True,
    None,
    True,
    None,
    None,
    True,
    None,
)


def go_to_url(driver: WebDriver, url: str, page_name: str):
    """Go to the specified URL and take a screenshot afterwards."""
    driver.get(url)
    take_screenshot(driver, page_name)


def check_url(driver: WebDriver, expected_url: str, *, exact_match: bool = True):
    """Check if current page URL matches the expected one."""
    with assertion_msg(
        f"Expected page URL to be: '{expected_url}' but got '{driver.current_url}'"
    ):
        if exact_match:
            assert driver.current_url == expected_url
        else:
            assert (driver.current_url in expected_url) or (
                expected_url in driver.current_url
            )
    logging.debug(f"Current page URL matches expected '{driver.current_url}'")


def check_title(driver: WebDriver, expected_title: str, *, exact_match: bool = False):
    """Check if current page title matches the expected one."""
    with assertion_msg(
        f"Expected page title to be: '{expected_title}' but got '{driver.title}' on {driver.current_url}"
    ):
        if exact_match:
            assert expected_title.lower() == driver.title.lower()
        else:
            assert expected_title.lower() in driver.title.lower()
    logging.debug(
        f"Page title on '{driver.current_url}' matches expected '{expected_title}'"
    )


def check_for_expected_sections_elements(
    driver: WebDriver, sections: Dict[str, Selector]
):
    """Check if all elements in page sections are visible."""
    for section in sections:
        for element_name, selector in sections[section].items():
            if not isinstance(selector, Selector):
                raise TypeError(
                    f"Expected '{selector}' to be a Selector, got {type(selector)}"
                )
            element = find_element(driver, selector, element_name=element_name)
            if not selector.is_visible:
                logging.debug(f"Skipping '{element_name} as it's marked as invisible'")
                continue
            with assertion_msg(
                f"It looks like '{element_name}' element in '{section}' section is not visible on {driver.current_url}"
            ):
                assert element.is_displayed()
        logging.debug(f"All expected elements are visible on '{driver.current_url}'")


def find_and_click_on_page_element(
    driver: WebDriver, sections: dict, element_name: str, *, wait_for_it: bool = True
):
    """Find page element in any page section selectors and click on it."""
    found_selector = False
    for section_name, selectors in sections.items():
        if element_name.lower() in selectors:
            found_selector = True
            selector = selectors[element_name.lower()]
            logging.debug(
                "Found '%s' in '%s' section with following selector: '%s'",
                element_name,
                section_name,
                selector,
            )
            web_element = find_element(
                driver, selector, element_name=element_name, wait_for_it=wait_for_it
            )
            check_if_element_is_visible(web_element, element_name)
            if web_element.get_attribute("target") == "_blank":
                logging.debug(
                    f"'{web_element.text}' opens in new tab, but will "
                    f"forcefully open it in the same one"
                )
                with wait_for_page_load_after_action(driver):
                    href = web_element.get_attribute("href")
                    driver.get(href)
            else:
                if selector.wait_after_click:
                    with wait_for_page_load_after_action(driver):
                        web_element.click()
                else:
                    web_element.click()
    with assertion_msg(f"Could not find '{element_name}' in any section"):
        assert found_selector


def initialize_scenario_data() -> ScenarioData:
    """Will initialize the Scenario Data."""
    return ScenarioData(actors={})


def unauthenticated_actor(alias: str) -> Actor:
    """Create an instance of an unauthenticated Actor.

    Will:
     * generate a random password for user, which can be used later on during
        registration or signing-in.
    """
    email = (
        "test+{}{}@directory.uktrade.io".format(alias, str(uuid.uuid4()))
        .replace("-", "")
        .replace(" ", "")
        .lower()
    )
    letters = "".join(random.choice(string.ascii_letters) for _ in range(10))
    digits = "".join(random.choice(string.digits) for _ in range(10))
    password = f"{letters}{digits}"
    return Actor(alias=alias, email=email, password=password, visited_articles=[])


def barred_actor(alias: str) -> Actor:
    actor = unauthenticated_actor(alias)
    actor = actor._replace(**{"email": random.choice(BARRED_USERS)})
    return actor


def add_actor(context: Context, actor: Actor):
    """Will add Actor details to Scenario Data."""
    assert isinstance(actor, Actor), (
        f"Expected Actor named tuple but got '{type(actor)}'" " instead"
    )
    context.scenario_data.actors[actor.alias] = actor
    logging.debug("Successfully added actor: %s to Scenario Data", actor.alias)


def get_actor(context: Context, alias: str) -> Actor:
    """Get actor details from context Scenario Data."""
    return context.scenario_data.actors.get(alias)


def get_last_visited_page(context: Context, actor_alias: str) -> ModuleType:
    """Get last visited Page Object context Scenario Data."""
    actor = context.scenario_data.actors.get(actor_alias)
    return actor.visited_page


def update_actor(context: Context, alias: str, **kwargs):
    """Update Actor's details stored in context.scenario_data"""
    actors = context.scenario_data.actors
    for arg in kwargs:
        if arg in Actor._fields:
            logging.debug("Set '%s'='%s' for %s", arg, kwargs[arg], alias)
            actors[alias] = actors[alias]._replace(**{arg: kwargs[arg]})
    logging.debug("Successfully updated %s's details: %s", alias, actors[alias])


def avoid_browser_stack_idle_timeout_exception(driver: WebDriver):
    """BrowserStack will stop browser session after 90s of inactivity.

    In order to avoid it, this helper will generate random events, like scrolling
    """
    actions = {
        "scroll up": "window.scrollBy(0,-1000);",
        "scroll down": "window.scrollBy(0,1000);",
        "click on body": "document.querySelector('body').click();",
        "scroll to random link": "window.scrollTo(0, document.querySelectorAll('a')[Math.floor(Math.random()*document.querySelectorAll('a').length)].offsetTop);",  # noqa
    }
    action = random.choice(list(actions.keys()))
    message = f"Trigger '{action}' event to avoid 'Idle Timeout exception'"
    logging.debug(message)
    driver.execute_script(actions[action])


@retry(stop_max_attempt_number=3)
def take_screenshot(driver: WebDriver, page_name: str):
    """Will take a screenshot of current page."""
    if not isinstance(driver, WebDriver):
        logging.debug("Taking screenshots in non-browser executor is not possible")
        return
    if TAKE_SCREENSHOTS:
        session_id = driver.session_id
        browser = driver.capabilities.get("browserName", "unknown_browser")
        version = driver.capabilities.get("version", "unknown_version")
        platform = driver.capabilities.get("platform", "unknown_platform")
        stamp = datetime.isoformat(datetime.utcnow())
        filename = (
            f"{stamp}-{page_name}-{browser}-{version}-{platform}-{session_id}.png"
        )
        file_path = path.abspath(path.join("screenshots", filename))
        driver.save_screenshot(file_path)
        logging.debug(f"Screenshot of {page_name} page saved in: {filename}")
    else:
        logging.debug(
            "Taking screenshots is disabled. In order to turn it on please set"
            " an environment variable TAKE_SCREENSHOTS=true"
        )


@contextmanager
def assertion_msg(message: str, *args):
    """This will:
        * print the custom assertion message
        * print the traceback (stack trace)
        * raise the original AssertionError exception
    """
    try:
        yield
    except AssertionError as e:
        if args:
            message = message % args
        logging.error(message)
        e.args += (message,)
        _, _, tb = sys.exc_info()
        if len(sys._current_frames()) == 1:
            print(f"Found 'shallow' Traceback, will inspect outer traceback frames")
            import inspect

            for f in inspect.getouterframes(sys._getframe(0)):
                print(f"{f.filename} +{f.lineno} - in {f.function}")
                if "_def.py" in f.filename:
                    break
        traceback.print_tb(tb)
        raise


@contextmanager
def selenium_action(driver: WebDriver, message: str, *args):
    """This will:
        * print the custom assertion message
        * print the traceback (stack trace)
        * raise the original AssertionError exception

    :raises WebDriverException or NoSuchElementException
    """
    try:
        yield
    except (WebDriverException, NoSuchElementException, TimeoutException) as e:
        browser = driver.capabilities.get("browserName", "unknown browser")
        version = driver.capabilities.get("version", "unknown version")
        platform = driver.capabilities.get("platform", "unknown platform")
        session_id = driver.session_id
        info = "[{} v:{} os:{} session_id:{}]".format(
            browser, version, platform, session_id
        )
        if args:
            message = message % args
        print(f"{info} - {message}")
        logging.debug(f"{info} - {message}")
        e.args += (message,)
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
        raise


def wait_for_visibility(
    driver: WebDriver, selector: Selector, *, time_to_wait: int = 5
):
    """Wait until element is visible."""
    by_locator = (selector.by, selector.value)
    with selenium_action(
        driver,
        "Element identified by '{}' was not visible after waiting "
        "for {} seconds".format(selector.value, time_to_wait),
    ):
        WebDriverWait(driver, time_to_wait).until(
            expected_conditions.visibility_of_element_located(by_locator)
        )


def check_if_element_is_not_present(
    driver: WebDriver, selector: Selector, *, element_name: str = ""
):
    """Find element by CSS selector or it's ID."""
    try:
        driver.find_element(by=selector.by, value=selector.value)
        found = True
    except NoSuchElementException:
        found = False
    with assertion_msg(
        f"Expected not to find '{element_name}' element identified by '{selector.value}' on {driver.current_url}"
    ):
        assert not found


def is_element_present(driver: WebDriver, selector: Selector) -> bool:
    """Check if sought element is present"""
    try:
        elements = driver.find_elements(by=selector.by, value=selector.value)
        if elements:
            logging.debug(f"Found following elements: {elements}")
            found = True
        else:
            found = False
    except NoSuchElementException:
        found = False
    return found


def check_if_element_is_visible(web_element: WebElement, element_name: str):
    """Check if provided web element is visible."""
    with assertion_msg(
        f"Expected to see '{element_name}' element but it's not visible"
    ):
        assert web_element.is_displayed()


def check_if_element_is_not_visible(
    driver: WebDriver,
    selector: Selector,
    *,
    element_name: str = "",
    wait_for_it: bool = True,
):
    """Find element by CSS selector or it's ID."""
    try:
        element = find_element(
            driver, selector, element_name=element_name, wait_for_it=wait_for_it
        )
        with assertion_msg(
            f"Expected not to see '{element_name}' element identified by '{selector.value}' on {driver.current_url}"
        ):
            assert not element.is_displayed()
    except NoSuchElementException:
        logging.debug(f"As expected '{element_name}' is not present")
        pass


def find_element(
    driver: WebDriver,
    selector: Selector,
    *,
    element_name: str = "",
    wait_for_it: bool = True,
) -> WebElement:
    """Find element by CSS selector or it's ID."""
    with selenium_action(
        driver,
        f"Couldn't find element called '{element_name}' using selector '{selector.value}' on {driver.current_url}",
    ):
        element = driver.find_element(by=selector.by, value=selector.value)
    if wait_for_it and selector.is_visible:
        wait_for_visibility(driver, selector)
    return element


def find_selector_by_name(selectors: dict, name: str) -> Selector:
    found_selectors = [
        selector
        for section_selectors in selectors.values()
        for selector_name, selector in section_selectors.items()
        if selector_name.lower() == name.lower()
    ]
    assert len(found_selectors) == 1
    return found_selectors[0]


def find_elements(driver: WebDriver, selector: Selector) -> List[WebElement]:
    """Find element by CSS selector or it's ID."""
    with selenium_action(driver, f"Couldn't find elements using '{selector.value}'"):
        elements = driver.find_elements(by=selector.by, value=selector.value)
    return elements


def check_hash_of_remote_file(expected_hash: str, file_url: str):
    """Check if the md5 hash of the file is the same as expected."""
    from directory_tests_shared.settings import BASICAUTH_PASS, BASICAUTH_USER

    logging.debug("Fetching file: %s", file_url)
    parsed = urlparse(file_url)
    with_creds = f"{parsed.scheme}://{BASICAUTH_USER}:{BASICAUTH_PASS}@{parsed.netloc}{parsed.path}"
    response = requests.get(with_creds)
    logging.debug(f"Got {response.status_code} from {file_url}")
    assert response.status_code == 200
    file_hash = hashlib.md5(response.content).hexdigest()
    with assertion_msg(
        f"Expected hash of file downloaded from {file_url} to be {expected_hash} but got {file_hash}"
    ):
        assert expected_hash == file_hash


@contextmanager
def try_js_click_on_element_click_intercepted_exception(
    driver: WebDriver, element: WebElement
):
    """Try to use JS to perform click on an element if regular way didn't work

    This is to handle situations when clicking on element triggers:
        selenium.common.exceptions.ElementClickInterceptedException:
            Message: element click intercepted:
            Element <input id="id_terms" name="terms" type="checkbox">
            is not clickable at point (714, 1235).
            Other element would receive the click:
            <label for="id_terms">...</label>

    See: https://stackoverflow.com/a/44916498
    """
    try:
        yield
    except ElementClickInterceptedException as e:
        logging.warning(
            f"Click was intercepted. Will try JS workaround. Exception msg: " f"{e.msg}"
        )
        driver.execute_script("arguments[0].click();", element)


class wait_for_page_load_after_action(object):
    """Context manager for waiting the page to load.
    Proved to be a more reliable than wait_for_page_load() ^^^
    src:
    http://www.obeythetestinggoat.com/how-to-get-selenium-to-wait-for-page-load-after-a-click.html
    https://www.develves.net/blogs/asd/2017-03-04-selenium-waiting-for-page-load/
    """

    def __init__(self, driver: WebDriver, *, timeout: int = 3):
        self.driver = driver
        self.timeout = timeout

    def __enter__(self):
        self.old_page = self.driver.find_element_by_tag_name("html")

    def page_has_loaded(self):
        new_page = self.driver.find_element_by_tag_name("html")
        return new_page.id != self.old_page.id

    def __exit__(self, *_):
        self.wait_for(self.page_has_loaded)

    def wait_for(self, condition_function):
        import time

        start_time = time.time()
        while time.time() < start_time + self.timeout:
            if condition_function():
                return True
            else:
                time.sleep(0.1)
        raise Exception(
            f"Timed out after {self.timeout}s of waiting for the new page to load"
        )


def scroll_to(driver: WebDriver, element: WebElement):
    if "firefox" in driver.capabilities["browserName"].lower():
        view_port_height = int(driver.execute_script("return window.innerHeight;"))
        vertical_position = int(element.location["y"])
        if vertical_position > view_port_height:
            logging.debug(f"Scrolling to y={vertical_position}")
            driver.execute_script(f"window.scrollTo(0, {vertical_position});")
        else:
            logging.debug(
                f"Element is already positioned ({vertical_position}) within view_port "
                f"({view_port_height})"
            )
    else:
        action_chains = ActionChains(driver)
        action_chains.move_to_element(element)
        action_chains.perform()


def check_for_sections(
    driver: WebDriver,
    all_sections: dict,
    sought_sections: List[str],
    *,
    desktop: bool = True,
    mobile: bool = False,
    horizontal: bool = False,
):
    for name in sought_sections:
        if desktop:
            selectors = get_desktop_selectors(all_sections[name.lower()])
        elif mobile:
            selectors = get_mobile_selectors(all_sections[name.lower()])
        elif horizontal:
            selectors = get_horizontal_selectors(all_sections[name.lower()])
        else:
            raise KeyError(
                "Please choose from desktop, mobile or horizontal (mobile) " "selectors"
            )
        for key, selector in selectors.items():
            with selenium_action(
                driver,
                f"Could not find element: '{key}' identified by '{selector.value}'"
                f" selector on {driver.current_url}",
            ):
                element = driver.find_element(by=selector.by, value=selector.value)
            logging.debug(f"Scrolling/Moving focus to '{name}→{key}' element")
            scroll_to(driver, element)
            if selector.is_visible:
                with assertion_msg(
                    f"It looks like '{key}' element identified by '{selector}' "
                    f"selector is not visible on {driver.current_url}"
                ):
                    assert element.is_displayed()
            else:
                logging.debug(
                    f"Skipping visibility check for '{key} -> {selector}' as "
                    f"its selector is flagged as not visible"
                )


def get_desktop_selectors(section: dict) -> Dict[str, Selector]:
    return {key: selector for key, selector in section.items() if selector.in_desktop}


def get_mobile_selectors(section: dict) -> Dict[str, Selector]:
    return {key: selector for key, selector in section.items() if selector.in_mobile}


def get_horizontal_selectors(section: dict) -> Dict[str, Selector]:
    return {
        key: selector for key, selector in section.items() if selector.in_horizontal
    }


def get_selectors(section: dict, element_type: ElementType) -> Dict[str, Selector]:
    return {
        key: selector
        for key, selector in section.items()
        if selector.type == element_type
    }


def find_elements_of_type(
    driver: WebDriver, section: dict, element_type: ElementType
) -> defaultdict:
    selectors = get_selectors(section, element_type)
    result = defaultdict()
    for key, selector in selectors.items():
        element = find_element(driver, selector, element_name=key)
        result[key] = element
    return result


def selectors_by_group(form_selectors: Dict[str, Selector]) -> Dict[str, Selector]:
    groups = defaultdict(lambda: defaultdict(dict))
    for key, selector in form_selectors.items():
        if selector.group_id:
            groups[selector.group_id][key] = selector
        else:
            groups["default"][key] = selector

    return groups


def visit_url(driver: WebDriver, url: str):
    driver.get(url)


def tick_captcha_checkbox(driver: WebDriver):
    dev_site_key = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
    g_recaptcha = find_element(
        driver,
        Selector(By.CSS_SELECTOR, ".g-recaptcha"),
        element_name="captcha",
        wait_for_it=False,
    )
    current_site_key = g_recaptcha.get_attribute("data-sitekey")
    logging.debug(f"Current site key: {current_site_key}")
    logging.debug(f"Site key for captcha in dev mode: {dev_site_key}")
    is_in_dev_mode = current_site_key == dev_site_key
    if not is_in_dev_mode:
        raise NoSuchElementException(
            f"Captcha is not in Dev Mode on {driver.current_url}"
        )
    im_not_a_robot = Selector(By.CSS_SELECTOR, "#recaptcha-anchor")
    iframe = driver.find_element_by_tag_name("iframe")
    scroll_to(driver, iframe)
    driver.switch_to.frame(iframe)
    captcha = find_element(driver, im_not_a_robot)
    captcha.click()
    # wait 3 s after user clicks on the CAPTCHA checkbox
    # otherwise the test might fail
    time.sleep(3)
    driver.switch_to.parent_frame()


def fill_out_input_fields(
    driver: WebDriver, form_selectors: Dict[str, Selector], form_details: dict
):
    input_selectors = get_selectors(form_selectors, ElementType.INPUT)
    for key, selector in input_selectors.items():
        value_to_type = form_details[key]
        if not value_to_type:
            continue
        logging.debug(
            f"Filling out input field '{key}' with '{value_to_type}' on '{driver.current_url}"
        )
        input_field = find_element(
            driver, selector, element_name=key, wait_for_it=False
        )
        if input_field.is_displayed():
            input_field.clear()
        input_field.send_keys(value_to_type)
        if selector.autocomplete_callback:
            logging.debug(f"Calling autocomplete_callback()")
            selector.autocomplete_callback(driver, value=value_to_type)


def fill_out_textarea_fields(
    driver: WebDriver, form_selectors: Dict[str, Selector], form_details: dict
):
    textarea_selectors = get_selectors(form_selectors, ElementType.TEXTAREA)
    for key, selector in textarea_selectors.items():
        value_to_type = form_details[key]
        if not value_to_type:
            continue
        logging.debug(f"Filling out textarea: {key} with '{value_to_type}'")
        textarea = find_element(driver, selector, element_name=key, wait_for_it=False)
        if textarea.is_displayed():
            textarea.clear()
        textarea.send_keys(value_to_type)


def check_form_choices(
    driver: WebDriver, form_selectors: Dict[str, Selector], names: List[str]
):
    radio_selectors = get_selectors(form_selectors, ElementType.RADIO)
    for name in names:
        radio_selector = radio_selectors[name.lower()]
        find_element(driver, radio_selector, element_name=name, wait_for_it=False)
    logging.debug(
        f"All expected form choices: '{names}' are visible on " f"{driver.current_url}"
    )


def pick_option(
    driver: WebDriver, form_selectors: Dict[str, Selector], form_details: dict
):
    select_selectors = get_selectors(form_selectors, ElementType.SELECT)
    for key, selector in select_selectors.items():
        logging.debug(f"Picking option from {key} dropdown list")
        select = find_element(driver, selector, element_name=key, wait_for_it=False)
        if form_details.get(key, None):
            option = form_details[key]
        else:
            options = select.find_elements_by_css_selector("option")
            values = [
                option.get_property("value")
                for option in options
                if option.get_property("value")
            ]
            logging.debug("Available options: {}".format(values))
            option = random.choice(values)
        logging.debug(f"Will select option: {option}")
        option_value_selector = f"option[value='{option}']"
        option_element = select.find_element_by_css_selector(option_value_selector)
        option_element.click()


def pick_option_from_autosuggestion(
    driver: WebDriver, form_selectors: Dict[str, Selector], form_details: dict
):
    select_selectors = get_selectors(form_selectors, ElementType.SELECT)
    for key, selector in select_selectors.items():
        logging.debug(f"Picking option from {key} dropdown list")
        select = find_element(driver, selector, element_name=key, wait_for_it=False)
        logging.debug(f"dealing with {key} {selector}")
        if form_details.get(key, None):
            option = form_details[key]
        else:
            options = select.find_elements_by_css_selector("option")
            values = [
                option.get_attribute("value")
                for option in options
                if option.get_attribute("value")
            ]
            logging.debug(f"Available options: {values}")
            option = random.choice(values)
        logging.debug(f"Selected option: {option}")
        if key == "country":
            js_field_selector = Selector(By.ID, "js-country-select")
            js_field = find_element(driver, js_field_selector)
            js_field.click()
            js_field.clear()
            js_field.send_keys(option)
            first_suggestion_selector = Selector(
                By.CSS_SELECTOR, "#js-country-select__listbox li:nth-child(1)"
            )
            first_suggestion = find_element(
                driver, first_suggestion_selector, wait_for_it=True
            )
            first_suggestion.click()
        else:
            option_value_selector = "option[value='{}']".format(option)
            option_element = select.find_element_by_css_selector(option_value_selector)
            option_element.click()


def check_radio(
    driver: WebDriver, form_selectors: Dict[str, Selector], form_details: dict
):
    radio_selectors = get_selectors(form_selectors, ElementType.RADIO)
    for key, selector in radio_selectors.items():
        assert key in form_details, f"Can't find form detail for '{key}'"
        if form_details[key]:
            radio = find_element(driver, selector, element_name=key, wait_for_it=False)
            if not radio.get_property("checked"):
                logging.debug(f"Checking '{key}' radio")
                radio.click()


def check_random_radio(driver: WebDriver, form_selectors: Dict[str, Selector]):
    radio_selectors = get_selectors(form_selectors, ElementType.RADIO)
    grouped_selectors = selectors_by_group(radio_selectors)
    for group, selectors in grouped_selectors.items():
        logging.debug(f"Selecting random radio option from group: {group}")
        key = random.choice(list(selectors.keys()))
        selector = radio_selectors[key]
        radio = find_element(driver, selector, element_name=key, wait_for_it=False)
        if not radio.get_property("checked"):
            logging.debug(f"Checking '{key}' radio")
            radio.click()


def choose_one_form_option(
    driver: WebDriver, radio_selectors: Dict[str, Selector], name: str
):
    form_details = defaultdict(bool)
    for key in radio_selectors.keys():
        form_details[key] = key == name.lower()
    logging.debug(f"Form details: {form_details}")
    check_radio(driver, radio_selectors, form_details)


def choose_one_form_option_except(
    driver: WebDriver, radio_selectors: Dict[str, Selector], ignored: List[str]
) -> str:
    all_keys = list(radio_selectors.keys())
    without_ignored = list(set(all_keys) - set(ignored))
    selected = random.choice(without_ignored)
    form_details = defaultdict(bool)
    for key in radio_selectors.keys():
        form_details[key.lower()] = key.lower() == selected
    logging.debug(f"Form details (with ignored: {ignored}): {form_details}")
    check_radio(driver, radio_selectors, form_details)
    return selected


def pick_one_option_and_submit(
    driver: WebDriver,
    form_selectors: Dict[str, Selector],
    name: str,
    *,
    submit_button_name: str = "submit",
) -> Union[ModuleType, None]:
    radio_selectors = get_selectors(form_selectors, ElementType.RADIO)
    selector = radio_selectors[name.lower()]
    choose_one_form_option(driver, radio_selectors, name)
    take_screenshot(driver, "Before submitting the form")
    submit_button_selector = form_selectors[submit_button_name]
    button = find_element(
        driver, submit_button_selector, element_name="Submit button", wait_for_it=False
    )
    button.click()
    take_screenshot(driver, "After submitting the form")
    return selector.next_page


def tick_checkboxes(
    driver: WebDriver, form_selectors: Dict[str, Selector], form_details: dict
):
    checkbox_selectors = get_selectors(form_selectors, ElementType.CHECKBOX)
    for key, selector in checkbox_selectors.items():
        logging.debug(f"Ticking {key} checkbox (if necessary)")
        if form_details[key]:
            checkbox = find_element(
                driver, selector, element_name=key, wait_for_it=False
            )
            if not checkbox.get_property("checked"):
                with try_js_click_on_element_click_intercepted_exception(
                    driver, checkbox
                ):
                    checkbox.click()


def tick_checkboxes_by_labels(
    driver: WebDriver, form_selectors: Dict[str, Selector], form_details: dict
):
    checkbox_selectors = get_selectors(form_selectors, ElementType.LABEL)
    for key, selector in checkbox_selectors.items():
        if form_details[key]:
            logging.debug(f"'{key}' checkbox should be ticked")
            checkbox = find_element(
                driver, selector, element_name=key, wait_for_it=False
            )
            if not checkbox.get_property("checked"):
                logging.debug(f"'{key}' checkbox is not ticked, checking it")
                with try_js_click_on_element_click_intercepted_exception(
                    driver, checkbox
                ):
                    checkbox.click()
        else:
            logging.debug(f"'{key}' checkbox should be left unchanged")
            checkbox = find_element(
                driver, selector, element_name=key, wait_for_it=False
            )
            if checkbox.get_property("checked"):
                logging.debug(f"'{key}' checkbox is ticked, unchecking it")
                with try_js_click_on_element_click_intercepted_exception(
                    driver, checkbox
                ):
                    checkbox.click()
