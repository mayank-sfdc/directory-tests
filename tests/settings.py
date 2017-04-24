import os


DIRECTORY_API_URL = os.environ["DIRECTORY_API_URL"]
DIRECTORY_SSO_URL = os.environ['DIRECTORY_SSO_URL']
DIRECTORY_UI_BUYER_URL = os.environ["DIRECTORY_UI_BUYER_URL"]
DIRECTORY_UI_SUPPLIER_URL = os.environ["DIRECTORY_UI_SUPPLIER_URL"]
DIRECTORY_PROFILE_URL = os.environ["DIRECTORY_PROFILE_URL"]
LOCUST_MAX_WAIT = int(os.getenv("LOCUST_MAX_WAIT", 6000))
LOCUST_MIN_WAIT = int(os.getenv("LOCUST_MIN_WAIT", 500))
# run tests for 2.5min by default
LOCUST_TIMEOUT = int(os.getenv("LOCUST_TIMEOUT", 150))
API_CLIENT_KEY = os.getenv("API_CLIENT_KEY")
SSO_USER_ID = int(os.getenv("SSO_USER_ID", 0))
