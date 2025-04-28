# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from ....._models import BaseModel
from .application import Application

__all__ = ["ApplicationListResponse"]


class ApplicationListResponse(BaseModel):
    data: Optional[List[Application]] = None

    meta: Optional[Meta] = None
