# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .application_domain import ApplicationDomain

__all__ = ["ApplicationDomainResponse"]


class ApplicationDomainResponse(BaseModel):
    data: Optional[ApplicationDomain] = None

    meta: Optional[Dict[str, object]] = None
