# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from .consumer import Consumer
from ....._models import BaseModel
from .custom_attribute import CustomAttribute
from .validation_messages_dto import ValidationMessagesDto

__all__ = ["ApplicationVersion"]


class ApplicationVersion(BaseModel):
    application_id: str = FieldInfo(alias="applicationId")

    version: str

    id: Optional[str] = None

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    consumers: Optional[List[Consumer]] = None

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    custom_attributes: Optional[List[CustomAttribute]] = FieldInfo(alias="customAttributes", default=None)

    declared_consumed_event_version_ids: Optional[List[str]] = FieldInfo(
        alias="declaredConsumedEventVersionIds", default=None
    )

    declared_event_api_product_version_ids: Optional[List[str]] = FieldInfo(
        alias="declaredEventApiProductVersionIds", default=None
    )

    declared_produced_event_version_ids: Optional[List[str]] = FieldInfo(
        alias="declaredProducedEventVersionIds", default=None
    )

    description: Optional[str] = None

    display_name: Optional[str] = FieldInfo(alias="displayName", default=None)

    end_of_life_date: Optional[str] = FieldInfo(alias="endOfLifeDate", default=None)

    messaging_service_ids: Optional[List[str]] = FieldInfo(alias="messagingServiceIds", default=None)

    state_id: Optional[str] = FieldInfo(alias="stateId", default=None)

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""

    validation_messages: Optional[ValidationMessagesDto] = FieldInfo(alias="validationMessages", default=None)
