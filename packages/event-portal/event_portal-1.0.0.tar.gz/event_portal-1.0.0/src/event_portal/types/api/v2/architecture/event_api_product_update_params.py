# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Annotated, TypedDict

from ....._utils import PropertyInfo
from .custom_attribute_param import CustomAttributeParam

__all__ = ["EventAPIProductUpdateParams"]


class EventAPIProductUpdateParams(TypedDict, total=False):
    application_domain_id: Annotated[str, PropertyInfo(alias="applicationDomainId")]

    broker_type: Annotated[Literal["kafka", "solace"], PropertyInfo(alias="brokerType")]
    """The type of the broker used for the event API product"""

    custom_attributes: Annotated[Iterable[CustomAttributeParam], PropertyInfo(alias="customAttributes")]

    name: str
    """The name of the event API product"""

    shared: bool
