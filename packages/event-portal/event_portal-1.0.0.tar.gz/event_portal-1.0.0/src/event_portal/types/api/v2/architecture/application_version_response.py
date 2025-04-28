# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .application_version import ApplicationVersion

__all__ = ["ApplicationVersionResponse"]


class ApplicationVersionResponse(BaseModel):
    data: Optional[ApplicationVersion] = None

    meta: Optional[Dict[str, object]] = None
