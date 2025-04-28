# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["SubscriptionParam"]


class SubscriptionParam(TypedDict, total=False):
    subscription_type: Annotated[str, PropertyInfo(alias="subscriptionType")]

    value: str
