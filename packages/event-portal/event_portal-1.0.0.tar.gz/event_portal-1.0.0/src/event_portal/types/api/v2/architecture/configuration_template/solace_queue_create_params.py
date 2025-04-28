# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import TypedDict

__all__ = ["SolaceQueueCreateParams"]


class SolaceQueueCreateParams(TypedDict, total=False):
    description: str

    name: str

    type: str

    value: Dict[str, object]
    """The configuration template in JSON format"""
