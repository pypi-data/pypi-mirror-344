# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from .address import Address
from ....._models import BaseModel

__all__ = ["DeliveryDescriptor"]


class DeliveryDescriptor(BaseModel):
    id: Optional[str] = None

    address: Optional[Address] = None

    broker_type: Optional[str] = FieldInfo(alias="brokerType", default=None)

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    key_schema_primitive_type: Optional[
        Literal["BOOLEAN", "BYTES", "DOUBLE", "FLOAT", "INT", "LONG", "NULL", "NUMBER", "STRING"]
    ] = FieldInfo(alias="keySchemaPrimitiveType", default=None)

    key_schema_version_id: Optional[str] = FieldInfo(alias="keySchemaVersionId", default=None)

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""
