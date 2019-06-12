from locust import HttpLocust, TaskSet, task
from tests import settings, URLs
from tests.load import USER_AGENT, basic_auth
from tests.load.utils import rare_word


class SearchTasks(TaskSet):
    @task
    def search(self):
        url = URLs.DOMESTIC_SEARCH.relative
        params = {"q": rare_word()}

        self.client.get(
            url,
            params=params,
            headers=USER_AGENT,
            name="search/?q=[...]",
            auth=basic_auth(),
        )


class Search(HttpLocust):
    host = settings.EXRED_UI_URL
    task_set = SearchTasks
    stop_timeout = settings.LOCUST_TIMEOUT
    min_wait = settings.LOCUST_MIN_WAIT
    max_wait = settings.LOCUST_MAX_WAIT
