# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .custom_attribute import CustomAttribute

__all__ = ["ApplicationDomain", "Stats"]


class Stats(BaseModel):
    application_count: Optional[int] = FieldInfo(alias="applicationCount", default=None)

    enum_count: Optional[int] = FieldInfo(alias="enumCount", default=None)

    event_api_count: Optional[int] = FieldInfo(alias="eventApiCount", default=None)

    event_api_product_count: Optional[int] = FieldInfo(alias="eventApiProductCount", default=None)

    event_count: Optional[int] = FieldInfo(alias="eventCount", default=None)

    schema_count: Optional[int] = FieldInfo(alias="schemaCount", default=None)


class ApplicationDomain(BaseModel):
    name: str

    id: Optional[str] = None

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    custom_attributes: Optional[List[CustomAttribute]] = FieldInfo(alias="customAttributes", default=None)

    deletion_protected: Optional[bool] = FieldInfo(alias="deletionProtected", default=None)
    """
    If set to true, application domain cannot be deleted until deletion protected is
    disabled.
    """

    description: Optional[str] = None

    non_draft_descriptions_editable: Optional[bool] = FieldInfo(alias="nonDraftDescriptionsEditable", default=None)
    """If set to true, descriptions of entities in a non-draft state can be edited."""

    stats: Optional[Stats] = None

    topic_domain_enforcement_enabled: Optional[bool] = FieldInfo(alias="topicDomainEnforcementEnabled", default=None)
    """
    Forces all topic addresses within the application domain to be prefixed with one
    of the application domain’s configured topic domains.
    """

    type: Optional[str] = None

    unique_topic_address_enforcement_enabled: Optional[bool] = FieldInfo(
        alias="uniqueTopicAddressEnforcementEnabled", default=None
    )
    """Forces all topic addresses within the application domain to be unique."""

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""
