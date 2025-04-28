# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from ......_utils import PropertyInfo

__all__ = ["CustomAttributeDefinitionListParams"]


class CustomAttributeDefinitionListParams(TypedDict, total=False):
    page_number: Annotated[int, PropertyInfo(alias="pageNumber")]
    """The page number to get."""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """The number of custom attribute definitions to get per page."""
