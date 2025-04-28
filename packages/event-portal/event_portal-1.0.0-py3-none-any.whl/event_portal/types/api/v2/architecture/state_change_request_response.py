# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from ....._models import BaseModel
from .versioned_object_state_change_request import VersionedObjectStateChangeRequest

__all__ = ["StateChangeRequestResponse"]


class StateChangeRequestResponse(BaseModel):
    data: Optional[VersionedObjectStateChangeRequest] = None

    meta: Optional[Dict[str, object]] = None
