# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .event_access_request import EventAccessRequest

__all__ = ["EventAccessRequestResponse"]


class EventAccessRequestResponse(BaseModel):
    data: Optional[EventAccessRequest] = None

    meta: Optional[Dict[str, object]] = None
