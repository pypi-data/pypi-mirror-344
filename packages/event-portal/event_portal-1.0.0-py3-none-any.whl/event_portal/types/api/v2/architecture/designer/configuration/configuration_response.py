# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ......._models import BaseModel
from .configuration import Configuration

__all__ = ["ConfigurationResponse"]


class ConfigurationResponse(BaseModel):
    data: Optional[Configuration] = None

    meta: Optional[Dict[str, object]] = None
