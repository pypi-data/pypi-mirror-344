# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..meta import Meta
from ......_models import BaseModel
from .solace_client_profile_name import SolaceClientProfileName

__all__ = ["SolaceClientProfileNameListResponse"]


class SolaceClientProfileNameListResponse(BaseModel):
    data: Optional[List[SolaceClientProfileName]] = None

    meta: Optional[Meta] = None
