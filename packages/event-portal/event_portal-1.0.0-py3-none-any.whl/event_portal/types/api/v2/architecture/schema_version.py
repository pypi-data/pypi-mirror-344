# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .custom_attribute import CustomAttribute

__all__ = ["SchemaVersion", "SchemaVersionReference"]


class SchemaVersionReference(BaseModel):
    schema_version_id: Optional[str] = FieldInfo(alias="schemaVersionId", default=None)


class SchemaVersion(BaseModel):
    schema_id: str = FieldInfo(alias="schemaId")

    version: str

    id: Optional[str] = None

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    content: Optional[str] = None

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    custom_attributes: Optional[List[CustomAttribute]] = FieldInfo(alias="customAttributes", default=None)

    description: Optional[str] = None

    display_name: Optional[str] = FieldInfo(alias="displayName", default=None)

    end_of_life_date: Optional[str] = FieldInfo(alias="endOfLifeDate", default=None)

    referenced_by_event_version_ids: Optional[List[str]] = FieldInfo(alias="referencedByEventVersionIds", default=None)

    referenced_by_schema_version_ids: Optional[List[str]] = FieldInfo(
        alias="referencedBySchemaVersionIds", default=None
    )

    schema_version_references: Optional[List[SchemaVersionReference]] = FieldInfo(
        alias="schemaVersionReferences", default=None
    )

    state_id: Optional[str] = FieldInfo(alias="stateId", default=None)

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""
