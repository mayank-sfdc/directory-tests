# -*- coding: utf-8 -*-
"""Behave configuration file."""
import logging
from pprint import pformat

from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry

from directory_tests_shared.pdf import NoPDFMinerLogEntriesFilter
from directory_tests_shared.settings import AUTO_RETRY, AUTO_RETRY_MAX_ATTEMPTS
from directory_tests_shared.utils import blue, green, red
from tests.functional.utils.context_utils import (
    get_company,
    initialize_scenario_data,
    update_company,
)
from tests.functional.utils.generic import (
    delete_supplier_data_from_dir,
    delete_supplier_data_from_sso,
    extract_form_errors,
    extract_main_error,
    extract_section_error,
    print_response,
)
from tests.functional.utils.request import REQUEST_EXCEPTIONS


def before_all(context):
    context.config.setup_logging(configfile=".behave_logging")
    logger = logging.getLogger()
    logger.addFilter(NoPDFMinerLogEntriesFilter())


def before_feature(context, feature):
    """Use autoretry feature which automatically retries failing scenarios."""
    if AUTO_RETRY:
        for scenario in feature.scenarios:
            patch_scenario_with_autoretry(
                scenario, max_attempts=AUTO_RETRY_MAX_ATTEMPTS
            )


def before_scenario(context, scenario):
    logging.debug(f"Starting scenario: {scenario.name}")
    # re-initialize the scenario data
    context.scenario_data = initialize_scenario_data()


def before_step(context, step):
    logging.debug(f"Started step: {step.step_type.capitalize()} {step.name}")


def after_step(context, step):
    logging.debug(
        f"Finished step: {round(step.duration, 3)} {step.step_type.capitalize()} "
        f"{step.name}"
    )
    if step.status == "failed":
        logging.debug(
            f"Step: {step.step_type.capitalize()} {step.name} failed. Reason: "
            f"{step.exception}"
        )
        logging.debug(context.scenario_data)
        red("\nScenario data:")
        print(pformat(context.scenario_data))
        has_content = hasattr(context, "response")
        is_request_exception = isinstance(step.exception, REQUEST_EXCEPTIONS)
        if not is_request_exception and has_content:
            res = context.response
            content = res.content.decode("utf-8")
            main_errors = extract_main_error(content)
            section_errors = extract_section_error(content)
            form_errors = extract_form_errors(content)
            if main_errors:
                red(
                    "Found words in the `main` part of the response that might"
                    " suggest the root cause of the error"
                )
                print(main_errors)
            if section_errors:
                red(
                    "Found words in the `section` part of the response that "
                    "might suggest the root cause of the error"
                )
                print(section_errors)
            if form_errors:
                red(
                    "Found words in the `form` part of the response that might"
                    " suggest the root cause of the error"
                )
                print(form_errors)
            green("Last recorded request & response")
            print_response(res, trim=True, content_only=True)
        else:
            blue("There's no response content to log")


def after_scenario(context, scenario):
    actors = context.scenario_data.actors
    for actor in actors.values():
        if actor.session:
            actor.session.close()
            logging.debug(f"Closed Requests session for {actor.alias}")
        if actor.type == "supplier":
            delete_supplier_data_from_sso(actor.email, context=context)
            if actor.company_alias:
                company = get_company(context, actor.company_alias)
                if not company:
                    logging.warning(
                        f"Could not find company '{actor.company_alias}' details in "
                        f"context.scenario_data.companies. Possibly details were not "
                        f"stored in it after its alias was added to actor's details"
                    )
                    continue
                if company.deleted:
                    logging.debug(f"Company '{company.alias}' is already deleted")
                    continue
                if company.number:
                    logging.debug(f"Delete company by number: {company.number}")
                    delete_supplier_data_from_dir(company.number, context=context)
                else:
                    logging.debug(f"Delete company by title: {company.title}")
                    delete_supplier_data_from_dir(company.title, context=context)
                update_company(context, alias=company.alias, deleted=True)
        else:
            logging.debug(
                f"'{actor.alias}' is not a supplier. No need to delete anything"
            )
    # clear the scenario data after every scenario
    context.scenario_data = None
    logging.debug(f"Finished scenario: {round(scenario.duration, 3)} → {scenario.name}")
