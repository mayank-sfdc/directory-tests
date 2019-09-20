# -*- coding: utf-8 -*-
import random

from directory_tests_shared import URLs, settings
from directory_tests_shared.utils import basic_auth
from locust import HttpLocust, TaskSet, task
from tests.load.utils import USER_AGENT, random_sector, rare_word


class FASTasks(TaskSet):
    @task
    def home_page(self):
        url = URLs.FAS_LANDING.relative
        self.client.get(
            url,
            headers=USER_AGENT,
            name="/",
            auth=basic_auth(),
        )

    @task
    def search(self):
        url = URLs.FAS_SEARCH.relative
        params = {
            "q": rare_word(),
            "industries": random_sector(),
        }
        self.client.get(
            url,
            params=params,
            headers=USER_AGENT,
            name="/search/?q=[term]&industries=[sectors]",
            auth=basic_auth(),
        )

    @task
    def profile(self):
        ch_ids = [
            "00832429", "02152566", "04092016", "04716401", "06362216", "06712674",
            "07006709", "07282974", "07543721", "07710219", "07719599", "07906462",
            "07944809", "08037389", "08240787", "08291104", "08597472", "08634730",
            "08646741", "08795085", "08818272", "08956237", "09009697", "09642236",
            "10668509", "11102696", "11136874", "NI608411", "SC443301", "SC465051",
        ]
        self.client.get(
            URLs.FAS_SUPPLIER.template.format(ch_number=random.choice(ch_ids)),
            headers=USER_AGENT,
            name="/suppliers/[id]/[slug]/",
            auth=basic_auth(),
        )


class FAS(HttpLocust):
    host = settings.FIND_A_SUPPLIER_URL
    task_set = FASTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
