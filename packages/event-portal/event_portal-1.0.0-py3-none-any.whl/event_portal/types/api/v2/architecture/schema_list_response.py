# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from ....._models import BaseModel
from .schema_object import SchemaObject

__all__ = ["SchemaListResponse"]


class SchemaListResponse(BaseModel):
    data: Optional[List[SchemaObject]] = None

    meta: Optional[Meta] = None
