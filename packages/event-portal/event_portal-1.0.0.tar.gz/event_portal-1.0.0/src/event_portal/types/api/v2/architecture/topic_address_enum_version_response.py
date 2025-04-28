# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .topic_address_enum_version import TopicAddressEnumVersion

__all__ = ["TopicAddressEnumVersionResponse"]


class TopicAddressEnumVersionResponse(BaseModel):
    data: Optional[TopicAddressEnumVersion] = None

    meta: Optional[Dict[str, object]] = None
