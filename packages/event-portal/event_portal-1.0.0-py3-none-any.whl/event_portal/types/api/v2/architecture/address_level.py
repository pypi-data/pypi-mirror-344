# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["AddressLevel"]


class AddressLevel(BaseModel):
    address_level_type: Literal["literal", "variable"] = FieldInfo(alias="addressLevelType")

    name: str

    enum_version_id: Optional[str] = FieldInfo(alias="enumVersionId", default=None)
