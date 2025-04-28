# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Annotated, TypedDict

from ....._utils import PropertyInfo
from .address_param import AddressParam

__all__ = ["DeliveryDescriptorParam"]


class DeliveryDescriptorParam(TypedDict, total=False):
    id: str

    address: AddressParam

    broker_type: Annotated[str, PropertyInfo(alias="brokerType")]

    key_schema_primitive_type: Annotated[
        Literal["BOOLEAN", "BYTES", "DOUBLE", "FLOAT", "INT", "LONG", "NULL", "NUMBER", "STRING"],
        PropertyInfo(alias="keySchemaPrimitiveType"),
    ]

    key_schema_version_id: Annotated[str, PropertyInfo(alias="keySchemaVersionId")]

    type: str
