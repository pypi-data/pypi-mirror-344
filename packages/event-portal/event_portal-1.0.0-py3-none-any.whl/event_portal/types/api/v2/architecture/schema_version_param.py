# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .custom_attribute_param import CustomAttributeParam

__all__ = ["SchemaVersionParam", "SchemaVersionReference"]


class SchemaVersionReference(TypedDict, total=False):
    schema_version_id: Annotated[str, PropertyInfo(alias="schemaVersionId")]


class SchemaVersionParam(TypedDict, total=False):
    schema_id: Required[Annotated[str, PropertyInfo(alias="schemaId")]]

    version: Required[str]

    content: str

    custom_attributes: Annotated[Iterable[CustomAttributeParam], PropertyInfo(alias="customAttributes")]

    description: str

    display_name: Annotated[str, PropertyInfo(alias="displayName")]

    end_of_life_date: Annotated[str, PropertyInfo(alias="endOfLifeDate")]

    schema_version_references: Annotated[
        Iterable[SchemaVersionReference], PropertyInfo(alias="schemaVersionReferences")
    ]
