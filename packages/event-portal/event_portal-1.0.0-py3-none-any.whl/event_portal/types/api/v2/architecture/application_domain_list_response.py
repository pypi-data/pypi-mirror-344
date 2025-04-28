# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from ....._models import BaseModel
from .application_domain import ApplicationDomain

__all__ = ["ApplicationDomainListResponse"]


class ApplicationDomainListResponse(BaseModel):
    data: Optional[List[ApplicationDomain]] = None

    meta: Optional[Meta] = None
