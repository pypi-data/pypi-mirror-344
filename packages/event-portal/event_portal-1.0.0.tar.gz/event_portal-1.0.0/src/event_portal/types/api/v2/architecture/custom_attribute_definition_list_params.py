# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["CustomAttributeDefinitionListParams"]


class CustomAttributeDefinitionListParams(TypedDict, total=False):
    associated_entity_types: Annotated[List[str], PropertyInfo(alias="associatedEntityTypes")]
    """
    Match only custom attribute definitions with the given associated entity type
    names separated by commas.
    """

    page_number: Annotated[int, PropertyInfo(alias="pageNumber")]
    """The page number to get."""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """The number of custom attribute definitions to get per page."""
