# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["EventVersionListParams"]


class EventVersionListParams(TypedDict, total=False):
    custom_attributes: Annotated[str, PropertyInfo(alias="customAttributes")]
    """
    Returns the entities that match the custom attribute filter. To filter by custom
    attribute name and value, use the format:
    `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
    by custom attribute name, use the format:
    `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
    operator for multiple custom attribute definitions (not multiple values for a
    given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
    operation. Note: the filter supports custom attribute values containing only the
    characters `[a-zA-Z0-9_\\--\\.. ]`.
    """

    event_ids: Annotated[List[str], PropertyInfo(alias="eventIds")]
    """Match only event versions of these event IDs, separated by commas."""

    ids: List[str]
    """Match only event versions with the given IDs, separated by commas."""

    messaging_service_ids: Annotated[List[str], PropertyInfo(alias="messagingServiceIds")]
    """
    Match only event versions with the given messaging service IDs, separated by
    commas.
    """

    page_number: Annotated[int, PropertyInfo(alias="pageNumber")]
    """The page number to get."""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """The number of event versions to get per page."""

    state_ids: Annotated[List[str], PropertyInfo(alias="stateIds")]
    """Match only event versions with the given state IDs, separated by commas."""
