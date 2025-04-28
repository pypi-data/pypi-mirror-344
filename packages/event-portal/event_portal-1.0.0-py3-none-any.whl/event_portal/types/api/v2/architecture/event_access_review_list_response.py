# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from .review import Review
from ....._models import BaseModel

__all__ = ["EventAccessReviewListResponse"]


class EventAccessReviewListResponse(BaseModel):
    data: Optional[List[Review]] = None

    meta: Optional[Meta] = None
