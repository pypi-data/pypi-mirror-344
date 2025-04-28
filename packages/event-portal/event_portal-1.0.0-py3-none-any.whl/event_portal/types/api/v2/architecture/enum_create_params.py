# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .custom_attribute_param import CustomAttributeParam

__all__ = ["EnumCreateParams"]


class EnumCreateParams(TypedDict, total=False):
    application_domain_id: Required[Annotated[str, PropertyInfo(alias="applicationDomainId")]]

    name: Required[str]

    custom_attributes: Annotated[Iterable[CustomAttributeParam], PropertyInfo(alias="customAttributes")]

    shared: bool
