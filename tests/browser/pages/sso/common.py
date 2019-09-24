# -*- coding: utf-8 -*-
"""SSO Common operations."""
import logging

from directory_sso_api_client.testapiclient import DirectorySSOTestAPIClient
from directory_tests_shared.settings import SSO_API_KEY, SSO_API_URL


def verify_account(email: str):
    client = DirectorySSOTestAPIClient(
        base_url=SSO_API_URL, api_key=SSO_API_KEY, sender_id="directory", timeout=5
    )
    response = client.flag_user_email_as_verified_or_not(email, verified=True)
    if response.status_code == 204:
        logging.debug("Flagged '%s' account as verified", email)
    else:
        logging.warning(
            "Something went wrong when trying to flag %s email as verified", email
        )


def delete_supplier_data_from_sso(email: str):
    client = DirectorySSOTestAPIClient(
        base_url=SSO_API_URL, api_key=SSO_API_KEY, sender_id="directory", timeout=5
    )
    response = client.delete_user_by_email(email)
    if response.status_code == 204:
        logging.debug("Deleted %s data from SSO", email)
    else:
        logging.warning(
            "Something went wrong when trying to delete %s data from SSO", email
        )
