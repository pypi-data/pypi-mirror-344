# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .custom_attribute_param import CustomAttributeParam
from .delivery_descriptor_param import DeliveryDescriptorParam
from .validation_messages_dto_param import ValidationMessagesDtoParam

__all__ = ["EventVersionParam"]


class EventVersionParam(TypedDict, total=False):
    event_id: Required[Annotated[str, PropertyInfo(alias="eventId")]]

    version: Required[str]

    custom_attributes: Annotated[Iterable[CustomAttributeParam], PropertyInfo(alias="customAttributes")]

    delivery_descriptor: Annotated[DeliveryDescriptorParam, PropertyInfo(alias="deliveryDescriptor")]

    description: str

    display_name: Annotated[str, PropertyInfo(alias="displayName")]

    end_of_life_date: Annotated[str, PropertyInfo(alias="endOfLifeDate")]

    schema_primitive_type: Annotated[
        Literal["BOOLEAN", "BYTES", "DOUBLE", "FLOAT", "INT", "LONG", "NULL", "NUMBER", "STRING"],
        PropertyInfo(alias="schemaPrimitiveType"),
    ]

    schema_version_id: Annotated[str, PropertyInfo(alias="schemaVersionId")]

    type: str

    validation_messages: Annotated[ValidationMessagesDtoParam, PropertyInfo(alias="validationMessages")]
