# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["Subscription", "AttractedEventVersionID"]


class AttractedEventVersionID(BaseModel):
    event_mesh_ids: Optional[List[str]] = FieldInfo(alias="eventMeshIds", default=None)

    event_version_id: Optional[str] = FieldInfo(alias="eventVersionId", default=None)


class Subscription(BaseModel):
    id: Optional[str] = None

    attracted_event_version_ids: Optional[List[AttractedEventVersionID]] = FieldInfo(
        alias="attractedEventVersionIds", default=None
    )

    subscription_type: Optional[str] = FieldInfo(alias="subscriptionType", default=None)

    value: Optional[str] = None
