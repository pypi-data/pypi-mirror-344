# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from ....._models import BaseModel
from .event_api_product import EventAPIProduct

__all__ = ["EventAPIProductListResponse"]


class EventAPIProductListResponse(BaseModel):
    data: Optional[List[EventAPIProduct]] = None

    meta: Optional[Meta] = None
