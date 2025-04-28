# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["EventAPIVersionRetrieveParams"]


class EventAPIVersionRetrieveParams(TypedDict, total=False):
    include: str
    """A list of additional entities to include in the response."""
