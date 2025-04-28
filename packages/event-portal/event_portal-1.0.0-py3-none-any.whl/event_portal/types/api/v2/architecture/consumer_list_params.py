# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["ConsumerListParams"]


class ConsumerListParams(TypedDict, total=False):
    application_version_ids: Annotated[List[str], PropertyInfo(alias="applicationVersionIds")]
    """
    Match only consumers with the given application version IDs, separated by
    commas.
    """

    ids: List[str]
    """Match only consumers with the given IDs separated by commas."""

    page_number: Annotated[int, PropertyInfo(alias="pageNumber")]
    """The page number to get."""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """The number of consumers to get per page."""
