# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from ......_models import BaseModel

__all__ = ["SolaceClientProfileName"]


class SolaceClientProfileName(BaseModel):
    id: Optional[str] = None

    associated_application_version_ids: Optional[List[str]] = FieldInfo(
        alias="associatedApplicationVersionIds", default=None
    )
    """
    The list of application version IDs associated with this Solace Client Profile
    Name Configuration template
    """

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    configuration_type_id: Optional[str] = FieldInfo(alias="configurationTypeId", default=None)
    """
    See <a href="/cloud/reference/getconfigurationtypes">Get a list of configuration
    types</a> for detail.
    """

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    description: Optional[str] = None

    environment_ids: Optional[List[str]] = FieldInfo(alias="environmentIds", default=None)
    """
    The list of environment IDs associated with this Solace Client Profile Name
    Configuration template
    """

    name: Optional[str] = None

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""

    value: Optional[Dict[str, object]] = None
    """The configuration template in JSON format"""
