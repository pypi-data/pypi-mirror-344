# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..meta import Meta
from ......_models import BaseModel
from .custom_attribute_definition import CustomAttributeDefinition

__all__ = ["CustomAttributeDefinitionsResponse"]


class CustomAttributeDefinitionsResponse(BaseModel):
    data: Optional[List[CustomAttributeDefinition]] = None

    meta: Optional[Meta] = None
