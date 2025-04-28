# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .schema_object import SchemaObject

__all__ = ["SchemaResponse"]


class SchemaResponse(BaseModel):
    data: Optional[SchemaObject] = None

    meta: Optional[Dict[str, object]] = None
