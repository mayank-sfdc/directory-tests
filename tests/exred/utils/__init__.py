# -*- coding: utf-8 -*-
"""ExRed utils."""
import logging
import os
import sys
import traceback
from contextlib import contextmanager
from datetime import datetime
from os.path import abspath, join

import requests
from behave.runner import Context
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from settings import (
    EXRED_UI_URL,
    BROWSER_STACK_SESSIONS_URL,
    BROWSER_STACK_USERNAME,
    BROWSER_STACK_ACCESS_KEY
)

ScenarioData = namedtuple(
    "ScenarioData",
    [
        "actors"
    ]
)
Actor = namedtuple(
    "Actor",
    [
        "alias", "email", "password", "self_classification",
        "triage_classification"
    ]
)

# Set all fields to None by default.
Actor.__new__.__defaults__ = (None,) * len(Actor._fields)


def initialize_scenario_data() -> ScenarioData:
    """Will initialize the Scenario Data.

    :return an empty ScenarioData named tuple
    """
    actors = {}
    scenario_data = ScenarioData(actors)
    return scenario_data


def take_screenshot(driver: webdriver, page_name: str):
    """Will take a screenshot of current page.

    :param driver: Any of the WebDrivers
    :param page_name: page name which will be used in the screenshot filename
    """
    session_id = driver.session_id
    stamp = datetime.isoformat(datetime.utcnow())
    filename = "{}-{}-{}.png".format(stamp, page_name, session_id)
    file_path = abspath(join("screenshots", filename))
    driver.save_screenshot(file_path)
    logging.debug("Screenshot of %s page saved in: %s", page_name, filename)


@contextmanager
def assertion_msg(message: str, *args):
    """This will:
        * print the custom assertion message
        * print the traceback (stack trace)
        * raise the original AssertionError exception

    :param message: a message that will be printed & logged when assertion fails
    :param args: values that will replace % conversion specifications in message
                 like: %s, %d
    """
    try:
        yield
    except AssertionError as e:
        if args:
            message = message % args
        logging.error(message)
        e.args += (message,)
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
        raise


@contextmanager
def selenium_action(driver: webdriver, message: str, *args):
    """This will:
        * print the custom assertion message
        * print the traceback (stack trace)
        * raise the original AssertionError exception

    :param driver: Selenium WebDriver required to extract browser information
    :param message: a message that will be printed & logged when assertion fails
    :param args: values that will replace % conversion specifications in message
                 like: %s, %d
    """
    try:
        yield
    except WebDriverException as e:
        browser = driver.capabilities.get("browserName", "unknown browser")
        version = driver.capabilities.get("version", "unknown version")
        platform = driver.capabilities.get("platform", "unknown platform")
        session_id = driver.session_id
        info = ("[{} v:{} os:{} session_id:{}] "
                .format(browser, version, platform, session_id))
        if args:
            message = message % args
        logging.error(info, message)
        e.args += (message,)
        _, _, tb = sys.exc_info()
        traceback.print_tb(tb)
        raise


def get_file_log_handler(
        log_formatter, *, log_level=logging.DEBUG, task_id: str = None) \
        -> logging.FileHandler:
    """Configure the console logger.

    Will use DEBUG logging level by default.

    :param log_formatter: specifies how the log entries will look like
    :param log_level: specifies logging level, e.g.: logging.ERROR
    :param task_id: (optional) ID of the parallel task
    :return: configured console log handler
    """
    if task_id:
        log_file = os.path.join("reports", ("behave-%s.log" % task_id))
    else:
        log_file = os.path.join("reports", "behave.log")
    print("Behave log file: {}".format(log_file))
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(log_formatter)
    return file_handler


def init_loggers(context: Context, *, task_id: str = None):
    """Will initialize console and file loggers."""
    # configure the formatter
    fmt = ('%(asctime)s-%(filename)s[line:%(lineno)d]-%(name)s-%(levelname)s: '
           '%(message)s')
    log_formatter = logging.Formatter(fmt)
    log_file_handler = get_file_log_handler(log_formatter, task_id=task_id)
    # Add log file handler to Behave's logging
    logging.getLogger("selenium").setLevel(logging.WARNING)
    context.config.setup_logging(handlers=[log_file_handler])


def flag_browserstack_session_as_failed(session_id: str, reason: str):
    url = BROWSER_STACK_SESSIONS_URL.format(session_id)
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "status": "failed",
        "reason": reason
    }
    auth = (BROWSER_STACK_USERNAME, BROWSER_STACK_ACCESS_KEY)
    response = requests.put(url=url, headers=headers, data=data, auth=auth)
    assert response.ok
    logging.error("Flagged BrowserStack session: %s as failed", session_id)
