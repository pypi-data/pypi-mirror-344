# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .configuration_type import ConfigurationType

__all__ = ["ConfigurationTypeRetrieveResponse"]


class ConfigurationTypeRetrieveResponse(BaseModel):
    data: Optional[ConfigurationType] = None

    meta: Optional[Dict[str, object]] = None
