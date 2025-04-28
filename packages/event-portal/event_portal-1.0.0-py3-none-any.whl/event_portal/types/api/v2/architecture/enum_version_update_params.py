# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .custom_attribute_param import CustomAttributeParam

__all__ = ["EnumVersionUpdateParams", "Value"]


class EnumVersionUpdateParams(TypedDict, total=False):
    enum_id: Required[Annotated[str, PropertyInfo(alias="enumId")]]

    values: Required[Iterable[Value]]

    version: Required[str]

    custom_attributes: Annotated[Iterable[CustomAttributeParam], PropertyInfo(alias="customAttributes")]

    description: str

    display_name: Annotated[str, PropertyInfo(alias="displayName")]

    end_of_life_date: Annotated[str, PropertyInfo(alias="endOfLifeDate")]


class Value(TypedDict, total=False):
    value: Required[str]

    enum_version_id: Annotated[str, PropertyInfo(alias="enumVersionId")]

    label: str
