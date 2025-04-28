# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["CustomAttribute"]


class CustomAttribute(BaseModel):
    custom_attribute_definition_id: Optional[str] = FieldInfo(alias="customAttributeDefinitionId", default=None)

    custom_attribute_definition_name: Optional[str] = FieldInfo(alias="customAttributeDefinitionName", default=None)

    string_values: Optional[str] = FieldInfo(alias="stringValues", default=None)

    value: Optional[str] = None
