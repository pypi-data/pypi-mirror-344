# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["CustomAttributeParam"]


class CustomAttributeParam(TypedDict, total=False):
    custom_attribute_definition_id: Annotated[str, PropertyInfo(alias="customAttributeDefinitionId")]

    custom_attribute_definition_name: Annotated[str, PropertyInfo(alias="customAttributeDefinitionName")]

    string_values: Annotated[str, PropertyInfo(alias="stringValues")]

    value: str
