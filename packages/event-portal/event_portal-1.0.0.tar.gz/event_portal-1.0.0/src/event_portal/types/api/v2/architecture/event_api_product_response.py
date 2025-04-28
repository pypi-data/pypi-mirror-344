# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .event_api_product import EventAPIProduct

__all__ = ["EventAPIProductResponse"]


class EventAPIProductResponse(BaseModel):
    data: Optional[EventAPIProduct] = None

    meta: Optional[Dict[str, object]] = None
