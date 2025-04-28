# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .event_api_product_version import EventAPIProductVersion

__all__ = ["EventAPIProductVersionResponse"]


class EventAPIProductVersionResponse(BaseModel):
    data: Optional[EventAPIProductVersion] = None

    meta: Optional[Dict[str, object]] = None
