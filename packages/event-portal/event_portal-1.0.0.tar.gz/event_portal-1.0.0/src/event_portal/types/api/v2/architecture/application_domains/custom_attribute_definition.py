# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ......_models import BaseModel
from ..validation_messages_dto import ValidationMessagesDto

__all__ = ["CustomAttributeDefinition", "AssociatedEntity"]


class AssociatedEntity(BaseModel):
    application_domain_ids: Optional[List[str]] = FieldInfo(alias="applicationDomainIds", default=None)

    entity_type: Optional[str] = FieldInfo(alias="entityType", default=None)


class CustomAttributeDefinition(BaseModel):
    scope: Literal["organization", "applicationDomain"]

    id: Optional[str] = None

    application_domain_id: Optional[str] = FieldInfo(alias="applicationDomainId", default=None)

    associated_entities: Optional[List[AssociatedEntity]] = FieldInfo(alias="associatedEntities", default=None)

    associated_entity_types: Optional[List[str]] = FieldInfo(alias="associatedEntityTypes", default=None)

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    name: Optional[str] = None

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""

    validation_messages: Optional[ValidationMessagesDto] = FieldInfo(alias="validationMessages", default=None)

    value_type: Optional[Literal["STRING", "LONG_TEXT", "MULTI_STRING_VALUE"]] = FieldInfo(
        alias="valueType", default=None
    )
