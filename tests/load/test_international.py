# -*- coding: utf-8 -*-
from random import choice

from directory_tests_shared import URLs, settings
from directory_tests_shared.utils import basic_auth
from locust import HttpLocust, TaskSet, task
from tests.load.utils import USER_AGENT


class InternationalTasks(TaskSet):

    @task
    def home_page(self):
        url = URLs.INTERNATIONAL_LANDING.relative
        self.client.get(
            url,
            headers=USER_AGENT,
            name="/",
            auth=basic_auth(),
        )

    @task
    def uk_setup_guides_pages(self):
        endpoints = [
            URLs.INVEST_UK_SETUP_GUIDE.relative,
            URLs.INVEST_UK_SETUP_GUIDE_OPEN_BANK_ACCOUNT.relative,
            URLs.INVEST_UK_SETUP_GUIDE_ACCESS_FINANCE.relative,
            URLs.INVEST_UK_SETUP_GUIDE_UK_TAX.relative,
        ]
        self.client.get(
            choice(endpoints),
            headers=USER_AGENT,
            name=URLs.INVEST_UK_SETUP_GUIDE.template,
            auth=basic_auth(),
        )

    @task
    def industry_pages(self):
        urls = [
            URLs.INTERNATIONAL_INDUSTRIES.relative,
            URLs.INTERNATIONAL_INDUSTRY_CREATIVE_INDUSTRIES.relative,
            URLs.INTERNATIONAL_INDUSTRY_ENGINEERING_AND_MANUFACTURING.relative,
            URLs.INTERNATIONAL_INDUSTRY_FINANCIAL_SERVICES.relative,
            URLs.INTERNATIONAL_INDUSTRY_TECHNOLOGY.relative,
        ]
        self.client.get(
            choice(urls),
            headers=USER_AGENT,
            name=URLs.INTERNATIONAL_INDUSTRIES.template,
            auth=basic_auth(),
        )


class International(HttpLocust):
    host = settings.INTERNATIONAL_URL
    task_set = InternationalTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
