# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .topic_address_enum import TopicAddressEnum

__all__ = ["TopicAddressEnumResponse"]


class TopicAddressEnumResponse(BaseModel):
    data: Optional[TopicAddressEnum] = None

    meta: Optional[Dict[str, object]] = None
