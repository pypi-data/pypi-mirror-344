# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Annotated, TypedDict

from ....._utils import PropertyInfo
from .event_param import EventParam
from .event_api_param import EventAPIParam
from .application_param import ApplicationParam
from .topic_domain_param import TopicDomainParam
from .event_version_param import EventVersionParam
from .schema_object_param import SchemaObjectParam
from .schema_version_param import SchemaVersionParam
from .event_api_product_param import EventAPIProductParam
from .event_api_version_param import EventAPIVersionParam
from .application_domain_param import ApplicationDomainParam
from .topic_address_enum_param import TopicAddressEnumParam
from .application_version_param import ApplicationVersionParam
from .validation_messages_dto_param import ValidationMessagesDtoParam
from .event_api_product_version_param import EventAPIProductVersionParam
from .topic_address_enum_version_param import TopicAddressEnumVersionParam
from .application_domains.custom_attribute_definition_param import CustomAttributeDefinitionParam

__all__ = ["ApplicationDomainImportParams", "AddressSpace"]


class ApplicationDomainImportParams(TypedDict, total=False):
    address_spaces: Annotated[Iterable[AddressSpace], PropertyInfo(alias="addressSpaces")]

    application_domains: Annotated[Iterable[ApplicationDomainParam], PropertyInfo(alias="applicationDomains")]

    applications: Iterable[ApplicationParam]

    application_versions: Annotated[Iterable[ApplicationVersionParam], PropertyInfo(alias="applicationVersions")]

    custom_attribute_definitions: Annotated[
        Iterable[CustomAttributeDefinitionParam], PropertyInfo(alias="customAttributeDefinitions")
    ]

    enums: Iterable[TopicAddressEnumParam]

    enum_versions: Annotated[Iterable[TopicAddressEnumVersionParam], PropertyInfo(alias="enumVersions")]

    event_api_products: Annotated[Iterable[EventAPIProductParam], PropertyInfo(alias="eventApiProducts")]

    event_api_product_versions: Annotated[
        Iterable[EventAPIProductVersionParam], PropertyInfo(alias="eventApiProductVersions")
    ]

    event_apis: Annotated[Iterable[EventAPIParam], PropertyInfo(alias="eventApis")]

    event_api_versions: Annotated[Iterable[EventAPIVersionParam], PropertyInfo(alias="eventApiVersions")]

    events: Iterable[EventParam]

    event_versions: Annotated[Iterable[EventVersionParam], PropertyInfo(alias="eventVersions")]

    format_version: Annotated[str, PropertyInfo(alias="formatVersion")]

    schemas: Iterable[SchemaObjectParam]

    schema_versions: Annotated[Iterable[SchemaVersionParam], PropertyInfo(alias="schemaVersions")]

    topic_domains: Annotated[Iterable[TopicDomainParam], PropertyInfo(alias="topicDomains")]

    validation_messages: Annotated[ValidationMessagesDtoParam, PropertyInfo(alias="validationMessages")]


class AddressSpace(TypedDict, total=False):
    broker_type: Annotated[str, PropertyInfo(alias="brokerType")]

    delimiter: str
