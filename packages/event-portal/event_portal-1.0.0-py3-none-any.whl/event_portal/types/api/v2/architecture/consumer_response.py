# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .consumer import Consumer
from ....._models import BaseModel

__all__ = ["ConsumerResponse"]


class ConsumerResponse(BaseModel):
    data: Optional[Consumer] = None

    meta: Optional[Dict[str, object]] = None
