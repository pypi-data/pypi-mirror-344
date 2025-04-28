# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..meta import Meta
from ......_models import BaseModel
from .solace_client_profile_name import SolaceClientProfileName

__all__ = ["SolaceClientProfileNameConfigurationTemplateResponse"]


class SolaceClientProfileNameConfigurationTemplateResponse(BaseModel):
    data: Optional[SolaceClientProfileName] = None

    meta: Optional[Meta] = None
