# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["ValidationMessageDto", "Context"]


class Context(BaseModel):
    entity_names: Optional[List[str]] = FieldInfo(alias="entityNames", default=None)

    entity_type: Optional[str] = FieldInfo(alias="entityType", default=None)

    ids: Optional[List[str]] = None


class ValidationMessageDto(BaseModel):
    context: Optional[Context] = None

    message: Optional[str] = None

    message_key: Optional[str] = FieldInfo(alias="messageKey", default=None)
