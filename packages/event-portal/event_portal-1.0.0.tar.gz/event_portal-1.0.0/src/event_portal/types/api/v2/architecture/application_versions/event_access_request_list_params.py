# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ......_utils import PropertyInfo

__all__ = ["EventAccessRequestListParams"]


class EventAccessRequestListParams(TypedDict, total=False):
    review_statuses: Annotated[List[str], PropertyInfo(alias="reviewStatuses")]
    """Get requests with the given review statuses"""
