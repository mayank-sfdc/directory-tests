# -*- coding: utf-8 -*-
import os
import logging
from enum import Enum
from importlib import import_module
from pkgutil import iter_modules
from types import ModuleType
from typing import Dict, List

import pages

REQUIRED_PROPERTIES = ["SERVICE", "NAME", "TYPE", "URL", "SELECTORS"]


class ElementType(Enum):
    INPUT = "input"
    CHECKBOX = "checkbox"
    RADIO = "radio"
    TEXTAREA = "textarea",
    IFRAME = "iframe"
    SELECT = "select"
    LABEL = "label"

    def __str__(self):
        return self.value


class Services(Enum):
    BRITISH_COUNCIL = "British Council"
    EVENTS = "Events"
    EXPORT_OPPORTUNITIES = "Export Opportunities"
    EXPORT_READINESS = "Export Readiness"
    FIND_A_BUYER = "Find a Buyer"
    FIND_A_SUPPLIER = "Find a Supplier"
    INVEST = "Invest"
    LEGAL_SERVICES = "Legal Services"
    SELLING_ONLINE_OVERSEAS = "Selling Online Overseas"
    SINGLE_SIGN_ON = "Single Sign-On"
    VISIT_BRITAIN = "Visit Britain"


def is_page_object(module: ModuleType):
    return all([hasattr(module, prop) for prop in REQUIRED_PROPERTIES])


class PageObjects(Enum):
    """Page Objects enumeration.

    Values can only be modules with properties required for a Page Object.
    """

    def __new__(cls, value):
        if not is_page_object(value):
            raise TypeError(
                "Expected to get a Page Object module but got: {}".format(
                    value
                )
            )
        member = object.__new__(cls)
        member._value_ = value
        return member

    def __str__(self):
        return "{}-{} [{} - {}]".format(
            self.value.SERVICE,
            self.value.NAME,
            self.value.TYPE,
            self.value.URL,
        )

    @property
    def name(self) -> str:
        return self.value.NAME

    @property
    def service(self) -> str:
        return self.value.SERVICE

    @property
    def type(self) -> str:
        return self.value.TYPE

    @property
    def url(self) -> str:
        return self.value.URL

    @property
    def selectors(self) -> Dict:
        return self.value.SELECTORS


def get_enum_key(module: ModuleType) -> str:
    return (
        f"{module.SERVICE}_{module.NAME}".upper()
        .replace(" ", "_")
        .replace("-", "_")
    )


def get_subpackages_names(package: ModuleType) -> List[str]:
    path = package.__path__
    return [name for _, name, is_pkg in iter_modules(path) if is_pkg]


def get_page_objects(package: ModuleType) -> Dict[str, ModuleType]:
    subpackages_names = get_subpackages_names(package)
    result = {}
    root_prefix = f"{package.__name__}."
    root_path = package.__path__[0]
    for subpackage_name in subpackages_names:
        subpackage_path = os.path.join(root_path, subpackage_name)
        for _, module_name, is_pkg in iter_modules([subpackage_path]):
            module_path = f"{root_prefix}{subpackage_name}.{module_name}"
            if not is_pkg:
                module = import_module(module_path)
                if is_page_object(module):
                    enum_key = get_enum_key(module)
                    result[enum_key] = module
    return result


PAGES = PageObjects("PageObjects", names=get_page_objects(pages))


def get_page_object(service_and_page: str) -> ModuleType:
    assert (
        " - " in service_and_page
    ), f"Invalid Service & Page name: {service_and_page}"
    parts = service_and_page.split(" - ")
    sought_service = parts[0]
    sought_page = parts[1]
    result = None
    for page_object in PAGES.__members__.values():
        if sought_service.lower() == page_object.service.lower():
            if hasattr(page_object.value, "NAMES"):
                names = page_object.value.NAMES
                if sought_page.lower() in [name.lower() for name in names]:
                    result = page_object.value
                    break
            else:
                if sought_page.lower() == page_object.name.lower():
                    result = page_object.value
                    break

    if not result:
        service_key = sought_service.replace(" ", "_").upper()
        keys = [
            key
            for key in PAGES.__members__.keys()
            if key.startswith(service_key)
        ]
        raise KeyError(
            f"Could not find Page Object for '{sought_page}' in "
            f"'{sought_service}' package. Here's a list of available Page "
            f"Objects: {keys}"
        )
    logging.debug(f"Found PO for: {service_and_page} → {result}")
    return result
