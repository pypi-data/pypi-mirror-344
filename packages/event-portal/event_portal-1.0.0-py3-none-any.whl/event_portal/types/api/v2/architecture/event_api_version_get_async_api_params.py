# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["EventAPIVersionGetAsyncAPIParams"]


class EventAPIVersionGetAsyncAPIParams(TypedDict, total=False):
    async_api_version: Annotated[Literal["2.0.0", "2.2.0", "2.5.0"], PropertyInfo(alias="asyncApiVersion")]
    """The version of AsyncAPI to use."""

    event_api_product_version_id: Annotated[str, PropertyInfo(alias="eventApiProductVersionId")]
    """The ID of the event API Product Version to use for generating bindings."""

    format: Literal["json", "yaml"]
    """The format in which to get the AsyncAPI specification.

    Possible values are yaml and json.
    """

    gateway_messaging_service_ids: Annotated[List[str], PropertyInfo(alias="gatewayMessagingServiceIds")]
    """The list IDs of gateway messaging services for generating bindings."""

    included_extensions: Annotated[
        Literal["all", "parent", "version", "none"], PropertyInfo(alias="includedExtensions")
    ]
    """The event portal database keys to include for each AsyncAPI object."""

    plan_id: Annotated[str, PropertyInfo(alias="planId")]
    """The ID of the plan to use for generating bindings."""

    show_versioning: Annotated[bool, PropertyInfo(alias="showVersioning")]
    """
    Include versions in each AsyncAPI object's name when only one version is present
    """
