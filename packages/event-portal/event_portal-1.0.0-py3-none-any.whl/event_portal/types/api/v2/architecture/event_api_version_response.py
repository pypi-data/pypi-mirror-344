# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .event_api_version import EventAPIVersion

__all__ = ["EventAPIVersionResponse"]


class EventAPIVersionResponse(BaseModel):
    data: Optional[EventAPIVersion] = None

    meta: Optional[Dict[str, object]] = None
