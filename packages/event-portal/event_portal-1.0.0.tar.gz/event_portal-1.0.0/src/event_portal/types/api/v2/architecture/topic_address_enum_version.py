# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .custom_attribute import CustomAttribute

__all__ = ["TopicAddressEnumVersion", "Value"]


class Value(BaseModel):
    value: str

    id: Optional[str] = None

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    enum_version_id: Optional[str] = FieldInfo(alias="enumVersionId", default=None)

    label: Optional[str] = None

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""


class TopicAddressEnumVersion(BaseModel):
    enum_id: str = FieldInfo(alias="enumId")

    values: List[Value]

    version: str

    id: Optional[str] = None

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    custom_attributes: Optional[List[CustomAttribute]] = FieldInfo(alias="customAttributes", default=None)

    description: Optional[str] = None

    display_name: Optional[str] = FieldInfo(alias="displayName", default=None)

    end_of_life_date: Optional[str] = FieldInfo(alias="endOfLifeDate", default=None)

    referenced_by_event_version_ids: Optional[List[str]] = FieldInfo(alias="referencedByEventVersionIds", default=None)

    referenced_by_topic_domain_ids: Optional[List[str]] = FieldInfo(alias="referencedByTopicDomainIds", default=None)

    state_id: Optional[str] = FieldInfo(alias="stateId", default=None)

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""
