# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .address_level_param import AddressLevelParam

__all__ = ["TopicDomainCreateParams"]


class TopicDomainCreateParams(TypedDict, total=False):
    address_levels: Required[Annotated[Iterable[AddressLevelParam], PropertyInfo(alias="addressLevels")]]

    application_domain_id: Required[Annotated[str, PropertyInfo(alias="applicationDomainId")]]

    broker_type: Required[Annotated[str, PropertyInfo(alias="brokerType")]]
