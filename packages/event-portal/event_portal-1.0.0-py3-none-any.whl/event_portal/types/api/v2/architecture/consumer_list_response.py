# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from .consumer import Consumer
from ....._models import BaseModel

__all__ = ["ConsumerListResponse"]


class ConsumerListResponse(BaseModel):
    data: Optional[List[Consumer]] = None

    meta: Optional[Meta] = None
