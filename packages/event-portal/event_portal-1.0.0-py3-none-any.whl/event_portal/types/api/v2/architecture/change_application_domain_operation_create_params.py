# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal, Annotated, TypedDict

from ....._utils import PropertyInfo

__all__ = ["ChangeApplicationDomainOperationCreateParams", "Entity"]


class ChangeApplicationDomainOperationCreateParams(TypedDict, total=False):
    entities: Iterable[Entity]

    target_app_domain_id: Annotated[str, PropertyInfo(alias="targetAppDomainId")]


class Entity(TypedDict, total=False):
    entity_type: Annotated[Literal["application", "schema", "event"], PropertyInfo(alias="entityType")]

    selected_entity_ids: Annotated[List[str], PropertyInfo(alias="selectedEntityIds")]
