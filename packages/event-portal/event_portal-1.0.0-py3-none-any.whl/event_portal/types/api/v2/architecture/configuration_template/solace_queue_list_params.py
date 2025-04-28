# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ......_utils import PropertyInfo

__all__ = ["SolaceQueueListParams"]


class SolaceQueueListParams(TypedDict, total=False):
    ids: List[str]
    """
    The unique identifiers of the Solace queue configuration templates to retrieve,
    separated by commas.
    """

    name: str
    """The name of the Solace queue configuration template to match."""

    page_number: Annotated[int, PropertyInfo(alias="pageNumber")]
    """The page number to retrieve."""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """The number of Solace queue configuration templates to return per page."""

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
