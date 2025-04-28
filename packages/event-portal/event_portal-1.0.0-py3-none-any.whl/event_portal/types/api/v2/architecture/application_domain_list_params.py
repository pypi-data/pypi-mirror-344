# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["ApplicationDomainListParams"]


class ApplicationDomainListParams(TypedDict, total=False):
    ids: List[str]
    """Match only application domains with the given IDs separated by commas."""

    include: List[str]
    """Specify extra data to be included, options are: stats"""

    name: str
    """Name to be used to match the application domain."""

    page_number: Annotated[int, PropertyInfo(alias="pageNumber")]
    """The page number to get."""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """The number of application domains to get per page."""
