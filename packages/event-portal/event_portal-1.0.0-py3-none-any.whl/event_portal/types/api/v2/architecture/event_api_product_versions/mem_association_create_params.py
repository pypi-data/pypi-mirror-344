# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from ......_utils import PropertyInfo

__all__ = ["MemAssociationCreateParams"]


class MemAssociationCreateParams(TypedDict, total=False):
    id: str

    body_event_api_product_version_id: Annotated[str, PropertyInfo(alias="eventApiProductVersionId")]

    messaging_service_id: Annotated[str, PropertyInfo(alias="messagingServiceId")]

    supported_protocols: Annotated[
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
        ],
        PropertyInfo(alias="supportedProtocols"),
    ]

    type: str
