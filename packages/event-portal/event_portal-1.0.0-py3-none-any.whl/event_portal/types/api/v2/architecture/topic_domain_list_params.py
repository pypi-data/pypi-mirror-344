# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["TopicDomainListParams"]


class TopicDomainListParams(TypedDict, total=False):
    application_domain_id: Annotated[str, PropertyInfo(alias="applicationDomainId")]

    application_domain_ids: Annotated[List[str], PropertyInfo(alias="applicationDomainIds")]
    """
    Match only topic domains with the given application domain ids separated by
    commas.
    """

    broker_type: Annotated[str, PropertyInfo(alias="brokerType")]
    """Match only topic domains with the given brokerType."""

    ids: List[str]
    """Match only topic domains with the given IDs separated by commas."""

    page_number: Annotated[int, PropertyInfo(alias="pageNumber")]
    """The page number to get."""

    page_size: Annotated[int, PropertyInfo(alias="pageSize")]
    """The number of topic domains to get per page."""
