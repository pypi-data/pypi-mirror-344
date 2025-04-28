# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .custom_attribute_param import CustomAttributeParam

__all__ = ["ApplicationCreateParams"]


class ApplicationCreateParams(TypedDict, total=False):
    application_domain_id: Required[Annotated[str, PropertyInfo(alias="applicationDomainId")]]

    application_type: Required[Annotated[str, PropertyInfo(alias="applicationType")]]

    broker_type: Required[Annotated[Literal["kafka", "solace"], PropertyInfo(alias="brokerType")]]

    name: Required[str]

    custom_attributes: Annotated[Iterable[CustomAttributeParam], PropertyInfo(alias="customAttributes")]

    type: str
