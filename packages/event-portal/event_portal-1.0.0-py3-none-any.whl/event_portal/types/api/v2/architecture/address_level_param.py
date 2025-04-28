# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["AddressLevelParam"]


class AddressLevelParam(TypedDict, total=False):
    address_level_type: Required[Annotated[Literal["literal", "variable"], PropertyInfo(alias="addressLevelType")]]

    name: Required[str]

    enum_version_id: Annotated[str, PropertyInfo(alias="enumVersionId")]
