# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .custom_attribute_param import CustomAttributeParam

__all__ = ["ApplicationDomainParam"]


class ApplicationDomainParam(TypedDict, total=False):
    name: Required[str]

    custom_attributes: Annotated[Iterable[CustomAttributeParam], PropertyInfo(alias="customAttributes")]

    deletion_protected: Annotated[bool, PropertyInfo(alias="deletionProtected")]
    """
    If set to true, application domain cannot be deleted until deletion protected is
    disabled.
    """

    description: str

    non_draft_descriptions_editable: Annotated[bool, PropertyInfo(alias="nonDraftDescriptionsEditable")]
    """If set to true, descriptions of entities in a non-draft state can be edited."""

    topic_domain_enforcement_enabled: Annotated[bool, PropertyInfo(alias="topicDomainEnforcementEnabled")]
    """
    Forces all topic addresses within the application domain to be prefixed with one
    of the application domain’s configured topic domains.
    """

    type: str

    unique_topic_address_enforcement_enabled: Annotated[
        bool, PropertyInfo(alias="uniqueTopicAddressEnforcementEnabled")
    ]
    """Forces all topic addresses within the application domain to be unique."""
