# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable
from typing_extensions import Literal, Required, Annotated, TypedDict

from ....._utils import PropertyInfo
from .custom_attribute_param import CustomAttributeParam

__all__ = [
    "EventAPIProductVersionParam",
    "EventAPIProductRegistration",
    "Filter",
    "FilterTopicFilter",
    "Plan",
    "PlanSolaceClassOfServicePolicy",
    "SolaceMessagingService",
]


class EventAPIProductRegistration(TypedDict, total=False):
    access_request_id: Required[Annotated[str, PropertyInfo(alias="accessRequestId")]]

    application_domain_id: Required[Annotated[str, PropertyInfo(alias="applicationDomainId")]]

    event_api_product_version_id: Required[Annotated[str, PropertyInfo(alias="eventApiProductVersionId")]]

    plan_id: Required[Annotated[str, PropertyInfo(alias="planId")]]

    registration_id: Required[Annotated[str, PropertyInfo(alias="registrationId")]]

    custom_attributes: Annotated[Dict[str, str], PropertyInfo(alias="customAttributes")]

    state: Literal["Pending Approval", "Rejected", "Revoked", "Approved", "Error", "Live"]


class FilterTopicFilter(TypedDict, total=False):
    event_version_ids: Required[Annotated[List[str], PropertyInfo(alias="eventVersionIds")]]

    filter_value: Annotated[str, PropertyInfo(alias="filterValue")]
    """Different filter values separated by comma"""

    name: str
    """name of address node"""


class Filter(TypedDict, total=False):
    id: str

    event_version_id: Annotated[str, PropertyInfo(alias="eventVersionId")]

    topic_filters: Annotated[Iterable[FilterTopicFilter], PropertyInfo(alias="topicFilters")]
    """List of variable that contains address node name and filters"""


class PlanSolaceClassOfServicePolicy(TypedDict, total=False):
    access_type: Annotated[Literal["exclusive", "non-exclusive"], PropertyInfo(alias="accessType")]

    maximum_time_to_live: Annotated[int, PropertyInfo(alias="maximumTimeToLive")]
    """Duration in seconds of how long a message can live in a queue"""

    max_msg_spool_usage: Annotated[int, PropertyInfo(alias="maxMsgSpoolUsage")]
    """Total number of MBs available for the queue to use"""

    message_delivery_mode: Annotated[Literal["direct", "guaranteed"], PropertyInfo(alias="messageDeliveryMode")]
    """The mode that will be used for message delivery (ex: `guaranteed` uses a queue)"""

    queue_type: Annotated[Literal["single", "combined"], PropertyInfo(alias="queueType")]
    """
    The arrangement of queues on a broker used for message delivery (ex: `single`
    uses one queue per event API version in this event API product)
    """


class Plan(TypedDict, total=False):
    name: str
    """Title of the object"""

    solace_class_of_service_policy: Annotated[
        PlanSolaceClassOfServicePolicy, PropertyInfo(alias="solaceClassOfServicePolicy")
    ]
    """Solace class of service policy"""


class SolaceMessagingService(TypedDict, total=False):
    solace_cloud_messaging_service_id: Annotated[str, PropertyInfo(alias="solaceCloudMessagingServiceId")]

    supported_protocols: Annotated[List[str], PropertyInfo(alias="supportedProtocols")]
    """Values for allowed supported protocols"""


class EventAPIProductVersionParam(TypedDict, total=False):
    event_api_product_id: Required[Annotated[str, PropertyInfo(alias="eventApiProductId")]]

    approval_type: Annotated[Literal["automatic", "manual"], PropertyInfo(alias="approvalType")]
    """Approval type"""

    custom_attributes: Annotated[Iterable[CustomAttributeParam], PropertyInfo(alias="customAttributes")]

    description: str

    display_name: Annotated[str, PropertyInfo(alias="displayName")]

    end_of_life_date: Annotated[str, PropertyInfo(alias="endOfLifeDate")]

    event_api_product_registrations: Annotated[
        Iterable[EventAPIProductRegistration], PropertyInfo(alias="eventApiProductRegistrations")
    ]

    event_api_version_ids: Annotated[List[str], PropertyInfo(alias="eventApiVersionIds")]
    """List of IDs of associated event API versions"""

    filters: Iterable[Filter]
    """List of filters that contains eventVersionId name and variables"""

    plans: Iterable[Plan]

    publish_state: Annotated[Literal["unset", "published"], PropertyInfo(alias="publishState")]
    """Publish state"""

    solace_messaging_services: Annotated[
        Iterable[SolaceMessagingService], PropertyInfo(alias="solaceMessagingServices")
    ]
    """Solace Messaging Services"""

    state_id: Annotated[str, PropertyInfo(alias="stateId")]

    summary: str

    version: str
