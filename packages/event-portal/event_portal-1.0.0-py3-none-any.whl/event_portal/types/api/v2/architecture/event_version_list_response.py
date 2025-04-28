# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from ....._models import BaseModel
from .event_version import EventVersion

__all__ = ["EventVersionListResponse"]


class EventVersionListResponse(BaseModel):
    data: Optional[List[EventVersion]] = None

    meta: Optional[Meta] = None
