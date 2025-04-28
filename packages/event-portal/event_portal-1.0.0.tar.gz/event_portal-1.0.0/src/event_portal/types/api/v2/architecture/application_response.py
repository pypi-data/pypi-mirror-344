# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .application import Application

__all__ = ["ApplicationResponse"]


class ApplicationResponse(BaseModel):
    data: Optional[Application] = None

    meta: Optional[Dict[str, object]] = None
