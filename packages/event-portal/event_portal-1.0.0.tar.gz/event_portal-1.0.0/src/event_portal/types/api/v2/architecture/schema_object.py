# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .custom_attribute import CustomAttribute

__all__ = ["SchemaObject"]


class SchemaObject(BaseModel):
    application_domain_id: str = FieldInfo(alias="applicationDomainId")

    name: str

    schema_type: str = FieldInfo(alias="schemaType")

    id: Optional[str] = None

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    custom_attributes: Optional[List[CustomAttribute]] = FieldInfo(alias="customAttributes", default=None)

    event_version_ref_count: Optional[int] = FieldInfo(alias="eventVersionRefCount", default=None)

    number_of_versions: Optional[int] = FieldInfo(alias="numberOfVersions", default=None)

    shared: Optional[bool] = None

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""
