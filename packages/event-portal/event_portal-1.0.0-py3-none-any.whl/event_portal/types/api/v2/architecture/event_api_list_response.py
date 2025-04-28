# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from .event_api import EventAPI
from ....._models import BaseModel

__all__ = ["EventAPIListResponse"]


class EventAPIListResponse(BaseModel):
    data: Optional[List[EventAPI]] = None

    meta: Optional[Meta] = None
