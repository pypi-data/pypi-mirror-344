# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .event_version import EventVersion

__all__ = ["EventVersionResponse"]


class EventVersionResponse(BaseModel):
    data: Optional[EventVersion] = None

    meta: Optional[Dict[str, object]] = None
