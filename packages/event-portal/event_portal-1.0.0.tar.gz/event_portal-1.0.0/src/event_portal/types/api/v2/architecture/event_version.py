# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .custom_attribute import CustomAttribute
from .delivery_descriptor import DeliveryDescriptor
from .validation_messages_dto import ValidationMessagesDto

__all__ = ["EventVersion", "AttractingApplicationVersionID"]


class AttractingApplicationVersionID(BaseModel):
    application_version_id: Optional[str] = FieldInfo(alias="applicationVersionId", default=None)

    event_mesh_ids: Optional[List[str]] = FieldInfo(alias="eventMeshIds", default=None)


class EventVersion(BaseModel):
    event_id: str = FieldInfo(alias="eventId")

    version: str

    id: Optional[str] = None

    attracting_application_version_ids: Optional[List[AttractingApplicationVersionID]] = FieldInfo(
        alias="attractingApplicationVersionIds", default=None
    )

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    consuming_event_api_version_ids: Optional[List[str]] = FieldInfo(alias="consumingEventApiVersionIds", default=None)

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    custom_attributes: Optional[List[CustomAttribute]] = FieldInfo(alias="customAttributes", default=None)

    declared_consuming_application_version_ids: Optional[List[str]] = FieldInfo(
        alias="declaredConsumingApplicationVersionIds", default=None
    )

    declared_producing_application_version_ids: Optional[List[str]] = FieldInfo(
        alias="declaredProducingApplicationVersionIds", default=None
    )

    delivery_descriptor: Optional[DeliveryDescriptor] = FieldInfo(alias="deliveryDescriptor", default=None)

    description: Optional[str] = None

    display_name: Optional[str] = FieldInfo(alias="displayName", default=None)

    end_of_life_date: Optional[str] = FieldInfo(alias="endOfLifeDate", default=None)

    messaging_service_ids: Optional[List[str]] = FieldInfo(alias="messagingServiceIds", default=None)

    producing_event_api_version_ids: Optional[List[str]] = FieldInfo(alias="producingEventApiVersionIds", default=None)

    schema_primitive_type: Optional[
        Literal["BOOLEAN", "BYTES", "DOUBLE", "FLOAT", "INT", "LONG", "NULL", "NUMBER", "STRING"]
    ] = FieldInfo(alias="schemaPrimitiveType", default=None)

    schema_version_id: Optional[str] = FieldInfo(alias="schemaVersionId", default=None)

    state_id: Optional[str] = FieldInfo(alias="stateId", default=None)

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""

    validation_messages: Optional[ValidationMessagesDto] = FieldInfo(alias="validationMessages", default=None)
