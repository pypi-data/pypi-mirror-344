# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .event_api import EventAPI
from ....._models import BaseModel

__all__ = ["EventAPIResponse"]


class EventAPIResponse(BaseModel):
    data: Optional[EventAPI] = None

    meta: Optional[Dict[str, object]] = None
