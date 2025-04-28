# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .custom_attribute_param import CustomAttributeParam

__all__ = ["EventAPIVersionParam"]


class EventAPIVersionParam(TypedDict, total=False):
    event_api_id: Required[Annotated[str, PropertyInfo(alias="eventApiId")]]

    consumed_event_version_ids: Annotated[List[str], PropertyInfo(alias="consumedEventVersionIds")]

    custom_attributes: Annotated[Iterable[CustomAttributeParam], PropertyInfo(alias="customAttributes")]

    declared_event_api_product_version_ids: Annotated[
        List[str], PropertyInfo(alias="declaredEventApiProductVersionIds")
    ]

    description: str

    display_name: Annotated[str, PropertyInfo(alias="displayName")]

    produced_event_version_ids: Annotated[List[str], PropertyInfo(alias="producedEventVersionIds")]

    state_id: Annotated[str, PropertyInfo(alias="stateId")]

    type: str

    version: str
