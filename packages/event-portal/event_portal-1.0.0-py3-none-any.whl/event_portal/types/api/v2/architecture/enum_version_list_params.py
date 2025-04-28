# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["EnumVersionListParams"]


class EnumVersionListParams(TypedDict, total=False):
    enum_ids: Annotated[List[str], PropertyInfo(alias="enumIds")]
    """Match only enumeration versions of these enumeration IDs, separated by commas."""

    ids: List[str]
    """Match only enumeration versions with the given IDs, separated by commas."""

    page_number: Annotated[int, PropertyInfo(alias="pageNumber")]
    """The page number to get."""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """The number of enumeration versions to get per page."""
