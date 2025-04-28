# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .event_access_request import EventAccessRequest

__all__ = ["ApplicationVersionEventAccessRequestsResponse", "Data"]


class Data(BaseModel):
    id: Optional[str] = None

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    event_access_requests: Optional[List[EventAccessRequest]] = FieldInfo(alias="eventAccessRequests", default=None)

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""


class ApplicationVersionEventAccessRequestsResponse(BaseModel):
    data: Optional[Data] = None

    meta: Optional[Dict[str, object]] = None
