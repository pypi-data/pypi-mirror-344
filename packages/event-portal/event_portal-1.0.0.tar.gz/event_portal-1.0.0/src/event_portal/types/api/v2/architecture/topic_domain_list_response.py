# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from ....._models import BaseModel
from .topic_domain import TopicDomain

__all__ = ["TopicDomainListResponse"]


class TopicDomainListResponse(BaseModel):
    data: Optional[List[TopicDomain]] = None

    meta: Optional[Meta] = None
