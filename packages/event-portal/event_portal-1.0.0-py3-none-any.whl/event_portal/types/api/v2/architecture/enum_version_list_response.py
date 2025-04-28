# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from ....._models import BaseModel
from .topic_address_enum_version import TopicAddressEnumVersion

__all__ = ["EnumVersionListResponse"]


class EnumVersionListResponse(BaseModel):
    data: Optional[List[TopicAddressEnumVersion]] = None

    meta: Optional[Meta] = None
