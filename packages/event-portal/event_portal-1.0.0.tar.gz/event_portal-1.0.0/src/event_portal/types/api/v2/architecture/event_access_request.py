# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["EventAccessRequest"]


class EventAccessRequest(BaseModel):
    application_id: str = FieldInfo(alias="applicationId")

    event_id: str = FieldInfo(alias="eventId")

    id: Optional[str] = None

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    comments: Optional[str] = None

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    relationship: Optional[Literal["consuming", "producing"]] = None

    review_status: Optional[Literal["approved", "pending", "declined"]] = FieldInfo(alias="reviewStatus", default=None)

    subscription: Optional[str] = None

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""
