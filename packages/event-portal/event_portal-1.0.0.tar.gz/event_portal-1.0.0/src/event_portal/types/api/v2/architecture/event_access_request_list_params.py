# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["EventAccessRequestListParams"]


class EventAccessRequestListParams(TypedDict, total=False):
    application_ids: Annotated[List[str], PropertyInfo(alias="applicationIds")]
    """Get requests with given applicationIds"""

    can_review: Annotated[bool, PropertyInfo(alias="canReview")]
    """If set to true, return requests that the user can review"""

    created_bys: Annotated[List[str], PropertyInfo(alias="createdBys")]
    """Get requests with the given createdBy user IDs"""

    event_ids: Annotated[List[str], PropertyInfo(alias="eventIds")]
    """Get requests with given eventIds"""

    exclude_auto_approved_events: Annotated[bool, PropertyInfo(alias="excludeAutoApprovedEvents")]
    """If set to true, exclude requests for auto-approved events"""

    ids: List[str]
    """The request ids to get"""

    page_number: Annotated[int, PropertyInfo(alias="pageNumber")]
    """The page number to get."""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """The number of requests to get per page."""

    relationships: List[Literal["consuming", "producing"]]
    """Get requests with the given relationships"""

    review_statuses: Annotated[List[Literal["approved", "pending", "declined"]], PropertyInfo(alias="reviewStatuses")]
    """Get requests with the given review statuses"""

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

    subscriptions: List[str]
    """Get requests with the given subscriptions"""
