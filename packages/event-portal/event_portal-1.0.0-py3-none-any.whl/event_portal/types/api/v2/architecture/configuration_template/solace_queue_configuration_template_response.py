# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..meta import Meta
from ......_models import BaseModel
from .solace_queue_configuration_template import SolaceQueueConfigurationTemplate

__all__ = ["SolaceQueueConfigurationTemplateResponse"]


class SolaceQueueConfigurationTemplateResponse(BaseModel):
    data: Optional[SolaceQueueConfigurationTemplate] = None

    meta: Optional[Meta] = None
