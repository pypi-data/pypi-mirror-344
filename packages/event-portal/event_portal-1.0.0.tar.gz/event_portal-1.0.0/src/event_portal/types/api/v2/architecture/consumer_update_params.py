# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .subscription_param import SubscriptionParam

__all__ = ["ConsumerUpdateParams"]


class ConsumerUpdateParams(TypedDict, total=False):
    application_version_id: Required[Annotated[str, PropertyInfo(alias="applicationVersionId")]]

    broker_type: Annotated[str, PropertyInfo(alias="brokerType")]

    consumer_type: Annotated[str, PropertyInfo(alias="consumerType")]

    name: str

    subscriptions: Iterable[SubscriptionParam]

    type: str
