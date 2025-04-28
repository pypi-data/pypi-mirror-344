# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .event import Event
from ....._models import BaseModel

__all__ = ["EventResponse"]


class EventResponse(BaseModel):
    data: Optional[Event] = None

    meta: Optional[Dict[str, object]] = None
