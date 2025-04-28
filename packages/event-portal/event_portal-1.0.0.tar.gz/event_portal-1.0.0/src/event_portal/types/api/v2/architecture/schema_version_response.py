# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .schema_version import SchemaVersion

__all__ = ["SchemaVersionResponse"]


class SchemaVersionResponse(BaseModel):
    data: Optional[SchemaVersion] = None

    meta: Optional[Dict[str, object]] = None
