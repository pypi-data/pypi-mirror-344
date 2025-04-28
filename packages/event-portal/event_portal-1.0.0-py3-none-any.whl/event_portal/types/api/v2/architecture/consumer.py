# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .subscription import Subscription

__all__ = ["Consumer"]


class Consumer(BaseModel):
    application_version_id: str = FieldInfo(alias="applicationVersionId")

    id: Optional[str] = None

    broker_type: Optional[str] = FieldInfo(alias="brokerType", default=None)

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    consumer_type: Optional[str] = FieldInfo(alias="consumerType", default=None)

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    name: Optional[str] = None

    subscriptions: Optional[List[Subscription]] = None

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""
