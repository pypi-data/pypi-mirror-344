# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .topic_domain import TopicDomain

__all__ = ["TopicDomainResponse"]


class TopicDomainResponse(BaseModel):
    data: Optional[TopicDomain] = None

    meta: Optional[Dict[str, object]] = None
