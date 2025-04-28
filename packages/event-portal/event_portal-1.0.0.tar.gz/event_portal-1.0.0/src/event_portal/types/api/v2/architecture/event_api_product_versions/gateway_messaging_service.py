# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ......_models import BaseModel

__all__ = ["GatewayMessagingService"]


class GatewayMessagingService(BaseModel):
    id: Optional[str] = None

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    event_api_product_version_id: Optional[str] = FieldInfo(alias="eventApiProductVersionId", default=None)

    messaging_service_id: Optional[str] = FieldInfo(alias="messagingServiceId", default=None)

    supported_protocols: Optional[
        List[
            Literal[
                "smfc",
                "smf",
                "smfs",
                "amqp",
                "amqps",
                "mqtt",
                "mqtts",
                "mqttws",
                "mqttwss",
                "secure-mqtt",
                "secure-mqttws",
                "rest",
                "rests",
            ]
        ]
    ] = FieldInfo(alias="supportedProtocols", default=None)

    type: Optional[str] = None

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""
