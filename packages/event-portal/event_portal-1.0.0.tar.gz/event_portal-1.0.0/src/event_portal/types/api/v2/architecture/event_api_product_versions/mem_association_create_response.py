# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ......_models import BaseModel
from .gateway_messaging_service import GatewayMessagingService

__all__ = ["MemAssociationCreateResponse"]


class MemAssociationCreateResponse(BaseModel):
    data: Optional[GatewayMessagingService] = None

    meta: Optional[Dict[str, object]] = None
