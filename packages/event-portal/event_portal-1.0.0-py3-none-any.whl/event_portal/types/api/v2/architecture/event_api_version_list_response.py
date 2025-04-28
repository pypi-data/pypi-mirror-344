# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from ....._models import BaseModel
from .event_api_version import EventAPIVersion

__all__ = ["EventAPIVersionListResponse"]


class EventAPIVersionListResponse(BaseModel):
    data: Optional[List[EventAPIVersion]] = None

    meta: Optional[Meta] = None
