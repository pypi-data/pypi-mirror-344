# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from ....._models import BaseModel
from .event_api_product_version import EventAPIProductVersion

__all__ = ["EventAPIProductVersionListResponse"]


class EventAPIProductVersionListResponse(BaseModel):
    data: Optional[List[EventAPIProductVersion]] = None

    meta: Optional[Meta] = None
