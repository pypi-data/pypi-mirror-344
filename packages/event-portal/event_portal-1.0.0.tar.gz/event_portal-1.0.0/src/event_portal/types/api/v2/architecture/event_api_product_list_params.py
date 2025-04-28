# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["EventAPIProductListParams"]


class EventAPIProductListParams(TypedDict, total=False):
    application_domain_id: Annotated[str, PropertyInfo(alias="applicationDomainId")]
    """Match only Event API Products in the given application domain."""

    application_domain_ids: Annotated[List[str], PropertyInfo(alias="applicationDomainIds")]
    """Match only Event API Products in the given application domains."""

    broker_type: Annotated[str, PropertyInfo(alias="brokerType")]
    """Match only Event API Products with the given broken type."""

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

    ids: List[str]
    """Match only Event API Products with the given IDs separated by commas."""

    name: str
    """Name of the Event API Product to match on."""

    page_number: Annotated[int, PropertyInfo(alias="pageNumber")]
    """The page number to get."""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """The number of Event API Products to get per page."""

    shared: bool
    """Match only with shared or unshared Event API Products."""

    sort: str
    """The sorting criteria for the returned results.

    You can sort the results by query parameter in ascending or descending order.
    Define the sort order using the following string: `fieldname:asc/desc` where:

    - `fieldname` — The field name of the query parameter to sort by.
    - `asc` — Sort the selected field name in ascending order.
    - `desc` — Sort the selected field name in descending order.

    If the direction is not specified, the default is ascending.

    You can use multiple query parameters to refine the sorting order.
    """
