# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ...meta import Meta
from ......._models import BaseModel
from .configuration import Configuration

__all__ = ["ConfigurationsResponse"]


class ConfigurationsResponse(BaseModel):
    data: Optional[List[Configuration]] = None

    meta: Optional[Meta] = None
