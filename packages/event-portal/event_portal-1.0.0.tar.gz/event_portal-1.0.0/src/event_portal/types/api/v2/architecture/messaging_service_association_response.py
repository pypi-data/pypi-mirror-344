# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .messaging_service_association_dto import MessagingServiceAssociationDto

__all__ = ["MessagingServiceAssociationResponse"]


class MessagingServiceAssociationResponse(BaseModel):
    data: Optional[MessagingServiceAssociationDto] = None

    meta: Optional[Dict[str, object]] = None
