# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ......_models import BaseModel
from .custom_attribute_definition import CustomAttributeDefinition

__all__ = ["CustomAttributeDefinitionResponse"]


class CustomAttributeDefinitionResponse(BaseModel):
    data: Optional[CustomAttributeDefinition] = None

    meta: Optional[Dict[str, object]] = None
