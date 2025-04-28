# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["ValidationMessageDtoParam", "Context"]


class Context(TypedDict, total=False):
    entity_names: Annotated[List[str], PropertyInfo(alias="entityNames")]

    entity_type: Annotated[str, PropertyInfo(alias="entityType")]

    ids: List[str]


class ValidationMessageDtoParam(TypedDict, total=False):
    context: Context

    message: str

    message_key: Annotated[str, PropertyInfo(alias="messageKey")]
