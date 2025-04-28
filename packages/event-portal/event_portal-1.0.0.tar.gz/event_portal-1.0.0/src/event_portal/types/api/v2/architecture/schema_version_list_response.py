# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .meta import Meta
from ....._models import BaseModel
from .schema_version import SchemaVersion

__all__ = ["SchemaVersionListResponse"]


class SchemaVersionListResponse(BaseModel):
    data: Optional[List[SchemaVersion]] = None

    meta: Optional[Meta] = None
