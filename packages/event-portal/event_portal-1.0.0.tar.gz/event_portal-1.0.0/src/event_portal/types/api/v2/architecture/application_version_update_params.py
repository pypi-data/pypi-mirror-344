# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .custom_attribute_param import CustomAttributeParam
from .validation_messages_dto_param import ValidationMessagesDtoParam

__all__ = ["ApplicationVersionUpdateParams"]


class ApplicationVersionUpdateParams(TypedDict, total=False):
    application_id: Required[Annotated[str, PropertyInfo(alias="applicationId")]]

    version: Required[str]

    include: List[str]

    relations_broker_type: Annotated[str, PropertyInfo(alias="relationsBrokerType")]

    custom_attributes: Annotated[Iterable[CustomAttributeParam], PropertyInfo(alias="customAttributes")]

    declared_consumed_event_version_ids: Annotated[List[str], PropertyInfo(alias="declaredConsumedEventVersionIds")]

    declared_event_api_product_version_ids: Annotated[
        List[str], PropertyInfo(alias="declaredEventApiProductVersionIds")
    ]

    declared_produced_event_version_ids: Annotated[List[str], PropertyInfo(alias="declaredProducedEventVersionIds")]

    description: str

    display_name: Annotated[str, PropertyInfo(alias="displayName")]

    end_of_life_date: Annotated[str, PropertyInfo(alias="endOfLifeDate")]

    type: str

    validation_messages: Annotated[ValidationMessagesDtoParam, PropertyInfo(alias="validationMessages")]
