# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["EventAPIProductVersionRetrieveParams"]


class EventAPIProductVersionRetrieveParams(TypedDict, total=False):
    client_app_id: Annotated[str, PropertyInfo(alias="clientAppId")]
    """Match Event API Product versions with the given clientAppId."""

    include: str
    """A list of additional entities to include in the response."""
