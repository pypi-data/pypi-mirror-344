# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from .review import Review
from ....._models import BaseModel

__all__ = ["ReviewResponse"]


class ReviewResponse(BaseModel):
    data: Optional[Review] = None

    meta: Optional[Dict[str, object]] = None
