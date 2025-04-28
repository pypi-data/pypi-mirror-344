# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .custom_attribute import CustomAttribute

__all__ = ["Application"]


class Application(BaseModel):
    application_domain_id: str = FieldInfo(alias="applicationDomainId")

    application_type: str = FieldInfo(alias="applicationType")

    broker_type: Literal["kafka", "solace"] = FieldInfo(alias="brokerType")

    name: str

    id: Optional[str] = None

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    custom_attributes: Optional[List[CustomAttribute]] = FieldInfo(alias="customAttributes", default=None)

    number_of_versions: Optional[int] = FieldInfo(alias="numberOfVersions", default=None)

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""
