# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..meta import Meta
from ......_models import BaseModel
from .solace_queue_configuration_template import SolaceQueueConfigurationTemplate

__all__ = ["SolaceQueueListResponse"]


class SolaceQueueListResponse(BaseModel):
    data: Optional[List[SolaceQueueConfigurationTemplate]] = None

    meta: Optional[Meta] = None
