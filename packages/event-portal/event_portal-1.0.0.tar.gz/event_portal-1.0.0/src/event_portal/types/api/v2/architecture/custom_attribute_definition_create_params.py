# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .validation_messages_dto_param import ValidationMessagesDtoParam

__all__ = ["CustomAttributeDefinitionCreateParams", "AssociatedEntity"]


class CustomAttributeDefinitionCreateParams(TypedDict, total=False):
    scope: Required[Literal["organization", "applicationDomain"]]

    id: str

    application_domain_id: Annotated[str, PropertyInfo(alias="applicationDomainId")]

    associated_entities: Annotated[Iterable[AssociatedEntity], PropertyInfo(alias="associatedEntities")]

    associated_entity_types: Annotated[List[str], PropertyInfo(alias="associatedEntityTypes")]

    name: str

    type: str

    validation_messages: Annotated[ValidationMessagesDtoParam, PropertyInfo(alias="validationMessages")]

    value_type: Annotated[Literal["STRING", "LONG_TEXT", "MULTI_STRING_VALUE"], PropertyInfo(alias="valueType")]


class AssociatedEntity(TypedDict, total=False):
    application_domain_ids: Annotated[List[str], PropertyInfo(alias="applicationDomainIds")]

    entity_type: Annotated[str, PropertyInfo(alias="entityType")]
