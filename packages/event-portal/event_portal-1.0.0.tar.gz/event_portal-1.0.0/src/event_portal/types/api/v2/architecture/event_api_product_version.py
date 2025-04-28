# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ....._models import BaseModel
from .custom_attribute import CustomAttribute

__all__ = [
    "EventAPIProductVersion",
    "EventAPIProductRegistration",
    "Filter",
    "FilterTopicFilter",
    "Plan",
    "PlanSolaceClassOfServicePolicy",
    "SolaceMessagingService",
]


class EventAPIProductRegistration(BaseModel):
    access_request_id: str = FieldInfo(alias="accessRequestId")

    application_domain_id: str = FieldInfo(alias="applicationDomainId")

    event_api_product_version_id: str = FieldInfo(alias="eventApiProductVersionId")

    plan_id: str = FieldInfo(alias="planId")

    registration_id: str = FieldInfo(alias="registrationId")

    id: Optional[str] = None

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    custom_attributes: Optional[Dict[str, str]] = FieldInfo(alias="customAttributes", default=None)

    state: Optional[Literal["Pending Approval", "Rejected", "Revoked", "Approved", "Error", "Live"]] = None

    type: Optional[str] = None
    """The type of payload"""

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""


class FilterTopicFilter(BaseModel):
    event_version_ids: List[str] = FieldInfo(alias="eventVersionIds")

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    filter_value: Optional[str] = FieldInfo(alias="filterValue", default=None)
    """Different filter values separated by comma"""

    name: Optional[str] = None
    """name of address node"""

    type: Optional[str] = None
    """The type of payload"""

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""


class Filter(BaseModel):
    id: Optional[str] = None

    event_version_id: Optional[str] = FieldInfo(alias="eventVersionId", default=None)

    topic_filters: Optional[List[FilterTopicFilter]] = FieldInfo(alias="topicFilters", default=None)
    """List of variable that contains address node name and filters"""

    type: Optional[str] = None
    """The type of payload"""


class PlanSolaceClassOfServicePolicy(BaseModel):
    id: Optional[str] = None
    """ID value of the object"""

    access_type: Optional[Literal["exclusive", "non-exclusive"]] = FieldInfo(alias="accessType", default=None)

    maximum_time_to_live: Optional[int] = FieldInfo(alias="maximumTimeToLive", default=None)
    """Duration in seconds of how long a message can live in a queue"""

    max_msg_spool_usage: Optional[int] = FieldInfo(alias="maxMsgSpoolUsage", default=None)
    """Total number of MBs available for the queue to use"""

    message_delivery_mode: Optional[Literal["direct", "guaranteed"]] = FieldInfo(
        alias="messageDeliveryMode", default=None
    )
    """The mode that will be used for message delivery (ex: `guaranteed` uses a queue)"""

    queue_type: Optional[Literal["single", "combined"]] = FieldInfo(alias="queueType", default=None)
    """
    The arrangement of queues on a broker used for message delivery (ex: `single`
    uses one queue per event API version in this event API product)
    """

    type: Optional[str] = None
    """The type of payload"""


class Plan(BaseModel):
    id: Optional[str] = None
    """ID value of the object"""

    name: Optional[str] = None
    """Title of the object"""

    solace_class_of_service_policy: Optional[PlanSolaceClassOfServicePolicy] = FieldInfo(
        alias="solaceClassOfServicePolicy", default=None
    )
    """Solace class of service policy"""

    type: Optional[str] = None
    """The type of this payload"""


class SolaceMessagingService(BaseModel):
    id: Optional[str] = None
    """ID value of the object"""

    environment_id: Optional[str] = FieldInfo(alias="environmentId", default=None)

    environment_name: Optional[str] = FieldInfo(alias="environmentName", default=None)
    """
    _Deprecation Date: 2025-01-17 Removal Date: 2026-01-17 Reason: Environment name
    should be fetched from Platform APIs._
    """

    event_mesh_id: Optional[str] = FieldInfo(alias="eventMeshId", default=None)

    event_mesh_name: Optional[str] = FieldInfo(alias="eventMeshName", default=None)

    messaging_service_id: Optional[str] = FieldInfo(alias="messagingServiceId", default=None)
    """ID of the Event Portal messaging service"""

    messaging_service_name: Optional[str] = FieldInfo(alias="messagingServiceName", default=None)
    """Name of the Event Portal messaging service"""

    solace_cloud_messaging_service_id: Optional[str] = FieldInfo(alias="solaceCloudMessagingServiceId", default=None)

    supported_protocols: Optional[List[str]] = FieldInfo(alias="supportedProtocols", default=None)
    """Values for allowed supported protocols"""

    type: Optional[str] = None
    """The type of payload"""


class EventAPIProductVersion(BaseModel):
    event_api_product_id: str = FieldInfo(alias="eventApiProductId")

    id: Optional[str] = None

    approval_type: Optional[Literal["automatic", "manual"]] = FieldInfo(alias="approvalType", default=None)
    """Approval type"""

    changed_by: Optional[str] = FieldInfo(alias="changedBy", default=None)
    """The user who last updated the entity"""

    created_by: Optional[str] = FieldInfo(alias="createdBy", default=None)
    """The user who created the entity"""

    created_time: Optional[str] = FieldInfo(alias="createdTime", default=None)
    """The time the entity was created"""

    custom_attributes: Optional[List[CustomAttribute]] = FieldInfo(alias="customAttributes", default=None)

    description: Optional[str] = None

    display_name: Optional[str] = FieldInfo(alias="displayName", default=None)

    end_of_life_date: Optional[str] = FieldInfo(alias="endOfLifeDate", default=None)

    event_api_product_registrations: Optional[List[EventAPIProductRegistration]] = FieldInfo(
        alias="eventApiProductRegistrations", default=None
    )

    event_api_version_ids: Optional[List[str]] = FieldInfo(alias="eventApiVersionIds", default=None)
    """List of IDs of associated event API versions"""

    filters: Optional[List[Filter]] = None
    """List of filters that contains eventVersionId name and variables"""

    plans: Optional[List[Plan]] = None

    published_time: Optional[str] = FieldInfo(alias="publishedTime", default=None)

    publish_state: Optional[Literal["unset", "published"]] = FieldInfo(alias="publishState", default=None)
    """Publish state"""

    solace_messaging_services: Optional[List[SolaceMessagingService]] = FieldInfo(
        alias="solaceMessagingServices", default=None
    )
    """Solace Messaging Services"""

    state_id: Optional[str] = FieldInfo(alias="stateId", default=None)

    summary: Optional[str] = None

    type: Optional[str] = None
    """The type of payload"""

    updated_time: Optional[str] = FieldInfo(alias="updatedTime", default=None)
    """The time the entity was last updated"""

    version: Optional[str] = None
