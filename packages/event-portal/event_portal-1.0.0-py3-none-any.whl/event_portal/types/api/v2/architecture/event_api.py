# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .custom_attribute import CustomAttribute

__all__ = ["EventAPI"]


class EventAPI(BaseModel):
    id: Optional[str] = None
    """Primary key set by the server."""

    application_domain_id: Optional[str] = FieldInfo(alias="applicationDomainId", default=None)

    broker_type: Optional[Literal["kafka", "solace"]] = FieldInfo(alias="brokerType", default=None)
    """The type of the broker used for the event API"""

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    custom_attributes: Optional[List[CustomAttribute]] = FieldInfo(alias="customAttributes", default=None)

    name: Optional[str] = None
    """The name of the event api."""

    number_of_versions: Optional[int] = FieldInfo(alias="numberOfVersions", default=None)

    shared: Optional[bool] = None

    type: Optional[str] = None
    """The type of this payload, eventApi."""

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""
