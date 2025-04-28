# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["EventAPIVersionListParams"]


class EventAPIVersionListParams(TypedDict, total=False):
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

    event_api_ids: Annotated[List[str], PropertyInfo(alias="eventApiIds")]
    """Match only event API versions of these event API IDs, separated by commas."""

    ids: List[str]
    """Match event API versions with the given IDs, separated by commas."""

    include: str
    """A list of additional entities to include in the response."""

    page_number: Annotated[int, PropertyInfo(alias="pageNumber")]
    """The page number to get results from based on the page size."""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """The number of results to return in one page of results."""

    state_id: Annotated[str, PropertyInfo(alias="stateId")]
    """Match event API versions with the given state ID."""
