# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict
from typing_extensions import Literal, Required, Annotated, TypedDict

from ......._utils import PropertyInfo

__all__ = ["SolaceQueueCreateParams"]


class SolaceQueueCreateParams(TypedDict, total=False):
    context_id: Required[Annotated[str, PropertyInfo(alias="contextId")]]
    """The unique identifier of the runtime service the configuration is for."""

    entity_id: Required[Annotated[str, PropertyInfo(alias="entityId")]]
    """The unique identifier of the designer entity the configuration is for."""

    context_type: Annotated[Literal["EVENT_BROKER"], PropertyInfo(alias="contextType")]
    """The type of runtime service the configuration is for."""

    template_id: Annotated[str, PropertyInfo(alias="templateId")]
    """The unique identifier of the configuration template."""

    type: str

    value: Dict[str, object]
    """The configuration value in JSON format."""
