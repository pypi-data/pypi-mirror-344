# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["ConfigurationTypeListParams"]


class ConfigurationTypeListParams(TypedDict, total=False):
    associated_entity_types: Annotated[List[str], PropertyInfo(alias="associatedEntityTypes")]
    """
    Match only configuration types with the given associated entity type values
    separated by commas.
    """

    broker_type: Annotated[str, PropertyInfo(alias="brokerType")]
    """Match only configuration types with the given broker type."""

    ids: List[str]
    """Match only configuration types with the given IDs separated by commas."""

    names: List[str]
    """Match only configuration types with the given names separated by commas."""
