# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["EventAccessReviewListParams"]


class EventAccessReviewListParams(TypedDict, total=False):
    decision: Literal["approved", "pending", "declined"]
    """Get reviews with the given decision"""

    ids: List[str]
    """The review ids to get"""

    page_number: Annotated[int, PropertyInfo(alias="pageNumber")]
    """The page number to get."""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """The number of events to get per page."""

    request_ids: Annotated[List[str], PropertyInfo(alias="requestIds")]
    """The request ids to get reviews for"""

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

    user_id: Annotated[str, PropertyInfo(alias="userId")]
    """Get reviews created by the given userId"""
