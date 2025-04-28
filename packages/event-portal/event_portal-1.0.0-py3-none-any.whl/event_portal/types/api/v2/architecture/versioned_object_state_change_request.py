# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["VersionedObjectStateChangeRequest"]


class VersionedObjectStateChangeRequest(BaseModel):
    state_id: Optional[str] = FieldInfo(alias="stateId", default=None)
