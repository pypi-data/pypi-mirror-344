# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from ....._models import BaseModel
from .configuration_type import ConfigurationType

__all__ = ["ConfigurationTypeListResponse"]


class ConfigurationTypeListResponse(BaseModel):
    data: Optional[List[ConfigurationType]] = None

    meta: Optional[Meta] = None
