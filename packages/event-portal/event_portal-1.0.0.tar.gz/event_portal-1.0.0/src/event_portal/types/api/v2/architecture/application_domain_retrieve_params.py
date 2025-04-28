# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import TypedDict

__all__ = ["ApplicationDomainRetrieveParams"]


class ApplicationDomainRetrieveParams(TypedDict, total=False):
    include: List[str]
    """Specify extra data to be included, options are: stats"""
