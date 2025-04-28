# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .custom_attribute import CustomAttribute

__all__ = ["EventAPIVersion"]


class EventAPIVersion(BaseModel):
    event_api_id: str = FieldInfo(alias="eventApiId")

    id: Optional[str] = None

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    consumed_event_version_ids: Optional[List[str]] = FieldInfo(alias="consumedEventVersionIds", default=None)

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    custom_attributes: Optional[List[CustomAttribute]] = FieldInfo(alias="customAttributes", default=None)

    declared_event_api_product_version_ids: Optional[List[str]] = FieldInfo(
        alias="declaredEventApiProductVersionIds", default=None
    )

    description: Optional[str] = None

    display_name: Optional[str] = FieldInfo(alias="displayName", default=None)

    end_of_life_date: Optional[str] = FieldInfo(alias="endOfLifeDate", default=None)

    produced_event_version_ids: Optional[List[str]] = FieldInfo(alias="producedEventVersionIds", default=None)

    state_id: Optional[str] = FieldInfo(alias="stateId", default=None)

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""

    version: Optional[str] = None
