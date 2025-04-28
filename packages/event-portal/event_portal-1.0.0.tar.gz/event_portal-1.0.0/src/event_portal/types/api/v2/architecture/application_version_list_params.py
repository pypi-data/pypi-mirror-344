# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["ApplicationVersionListParams"]


class ApplicationVersionListParams(TypedDict, total=False):
    application_ids: Annotated[List[str], PropertyInfo(alias="applicationIds")]
    """Match only application versions of these application IDs, separated by commas."""

    ids: List[str]
    """Match only application versions with the given IDs, separated by commas."""

    messaging_service_ids: Annotated[List[str], PropertyInfo(alias="messagingServiceIds")]
    """
    Match only application versions with the given messaging service IDs, separated
    by commas.
    """

    page_number: Annotated[int, PropertyInfo(alias="pageNumber")]
    """The page number to get."""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """The number of application versions to get per page."""

    state_ids: Annotated[List[str], PropertyInfo(alias="stateIds")]
    """Match only application versions with the given state IDs, separated by commas."""
