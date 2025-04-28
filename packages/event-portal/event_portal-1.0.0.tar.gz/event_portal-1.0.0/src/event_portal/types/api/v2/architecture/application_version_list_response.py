# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from ....._models import BaseModel
from .application_version import ApplicationVersion

__all__ = ["ApplicationVersionListResponse"]


class ApplicationVersionListResponse(BaseModel):
    data: Optional[List[ApplicationVersion]] = None

    meta: Optional[Meta] = None
