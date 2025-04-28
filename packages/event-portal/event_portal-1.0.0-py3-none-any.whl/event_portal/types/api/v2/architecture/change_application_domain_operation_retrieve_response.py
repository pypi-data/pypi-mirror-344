# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["ChangeApplicationDomainOperationRetrieveResponse", "Data"]


class Data(BaseModel):
    id: Optional[str] = None

    completed_time: Optional[str] = FieldInfo(alias="completedTime", default=None)

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)

    error: Optional[object] = None

    operation_type: Optional[str] = FieldInfo(alias="operationType", default=None)

    results: Optional[object] = None

    status: Optional[Literal["in_progress", "error", "validation_error", "success"]] = None


class ChangeApplicationDomainOperationRetrieveResponse(BaseModel):
    data: Optional[Data] = None

    meta: Optional[Dict[str, object]] = None
