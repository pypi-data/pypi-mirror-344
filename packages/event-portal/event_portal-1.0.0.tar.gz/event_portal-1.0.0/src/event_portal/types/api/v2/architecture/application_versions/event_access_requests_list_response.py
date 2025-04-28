# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..meta import Meta
from ......_models import BaseModel
from ..event_access_request import EventAccessRequest

__all__ = ["EventAccessRequestsListResponse"]


class EventAccessRequestsListResponse(BaseModel):
    data: Optional[List[EventAccessRequest]] = None

    meta: Optional[Meta] = None
