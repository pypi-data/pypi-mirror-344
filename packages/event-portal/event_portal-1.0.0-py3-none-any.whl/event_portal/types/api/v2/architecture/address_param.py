# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .address_level_param import AddressLevelParam

__all__ = ["AddressParam"]


class AddressParam(TypedDict, total=False):
    address_levels: Required[Annotated[Iterable[AddressLevelParam], PropertyInfo(alias="addressLevels")]]

    address_type: Annotated[Literal["topic"], PropertyInfo(alias="addressType")]

    type: str
