# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .address_level import AddressLevel

__all__ = ["Address"]


class Address(BaseModel):
    address_levels: List[AddressLevel] = FieldInfo(alias="addressLevels")

    id: Optional[str] = None

    address_type: Optional[Literal["topic"]] = FieldInfo(alias="addressType", default=None)

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""
