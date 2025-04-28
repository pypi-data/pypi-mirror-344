# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from ....._models import BaseModel

__all__ = ["ConfigurationType"]


class ConfigurationType(BaseModel):
    broker_type: str = FieldInfo(alias="brokerType")

    id: Optional[str] = None

    associated_entity_types: Optional[List[str]] = FieldInfo(alias="associatedEntityTypes", default=None)

    type: Optional[str] = None

    value_schema: Optional[Dict[str, object]] = FieldInfo(alias="valueSchema", default=None)
    """JSON schema definition of the configuration type"""
