# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from ....._models import BaseModel
from .topic_address_enum import TopicAddressEnum

__all__ = ["EnumListResponse"]


class EnumListResponse(BaseModel):
    data: Optional[List[TopicAddressEnum]] = None

    meta: Optional[Meta] = None
