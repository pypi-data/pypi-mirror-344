# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["ArchitectureGetStatesResponse", "Data"]


class Data(BaseModel):
    id: Optional[str] = None

    description: Optional[str] = None

    name: Optional[str] = None

    state_order: Optional[int] = FieldInfo(alias="stateOrder", default=None)

    type: Optional[str] = None


class ArchitectureGetStatesResponse(BaseModel):
    data: Optional[List[Data]] = None

    meta: Optional[Dict[str, object]] = None
