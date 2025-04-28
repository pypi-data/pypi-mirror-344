# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ....._models import BaseModel
from .validation_message_dto import ValidationMessageDto

__all__ = ["ValidationMessagesDto"]


class ValidationMessagesDto(BaseModel):
    errors: Optional[List[ValidationMessageDto]] = None

    warnings: Optional[List[ValidationMessageDto]] = None
