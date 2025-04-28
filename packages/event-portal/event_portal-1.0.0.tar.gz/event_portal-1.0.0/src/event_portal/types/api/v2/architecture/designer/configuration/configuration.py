# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ......._models import BaseModel

__all__ = ["Configuration"]


class Configuration(BaseModel):
    context_id: str = FieldInfo(alias="contextId")
    """The unique identifier of the runtime service the configuration is for."""

    entity_id: str = FieldInfo(alias="entityId")
    """The unique identifier of the designer entity the configuration is for."""

    id: Optional[str] = None
    """The unique identifier of the configuration."""

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    configuration_type_id: Optional[str] = FieldInfo(alias="configurationTypeId", default=None)
    """
    See <a href="/cloud/reference/getconfigurationtypes">Get a list of configuration
    types</a> for detail.
    """

    context_type: Optional[Literal["EVENT_BROKER"]] = FieldInfo(alias="contextType", default=None)
    """The type of runtime service the configuration is for."""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    entity_type: Optional[
        Literal[
            "address",
            "application",
            "applicationVersion",
            "audit",
            "consumer",
            "eventVersion",
            "schema",
            "schemaVersion",
            "subscription",
        ]
    ] = FieldInfo(alias="entityType", default=None)
    """The type of the designer entity the configuration is for."""

    identifier: Optional[str] = None
    """The audit identifier of the designer entity the configuration is for."""

    resolved_value: Optional[Dict[str, object]] = FieldInfo(alias="resolvedValue", default=None)
    """The resolved configuration value from user and configuration template."""

    template_id: Optional[str] = FieldInfo(alias="templateId", default=None)
    """The unique identifier of the configuration template."""

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""

    value: Optional[Dict[str, object]] = None
    """The configuration value in JSON format."""
