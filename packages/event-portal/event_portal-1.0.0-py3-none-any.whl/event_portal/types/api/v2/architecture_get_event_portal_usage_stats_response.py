# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["ArchitectureGetEventPortalUsageStatsResponse", "Data"]


class Data(BaseModel):
    application_count: Optional[int] = FieldInfo(alias="applicationCount", default=None)

    application_domain_count: Optional[int] = FieldInfo(alias="applicationDomainCount", default=None)

    application_version_count: Optional[int] = FieldInfo(alias="applicationVersionCount", default=None)

    application_versions_in_event_meshes_count: Optional[int] = FieldInfo(
        alias="applicationVersionsInEventMeshesCount", default=None
    )

    ca_app_domain_scoped_app_domain_def_count: Optional[int] = FieldInfo(
        alias="caAppDomainScopedAppDomainDefCount", default=None
    )

    ca_app_domain_scoped_app_domain_value_count: Optional[int] = FieldInfo(
        alias="caAppDomainScopedAppDomainValueCount", default=None
    )

    ca_app_domain_scoped_def_parent_count: Optional[int] = FieldInfo(
        alias="caAppDomainScopedDefParentCount", default=None
    )

    ca_app_domain_scoped_def_version_count: Optional[int] = FieldInfo(
        alias="caAppDomainScopedDefVersionCount", default=None
    )

    ca_app_domain_scoped_parent_value_count: Optional[int] = FieldInfo(
        alias="caAppDomainScopedParentValueCount", default=None
    )

    ca_app_domain_scoped_version_value_count: Optional[int] = FieldInfo(
        alias="caAppDomainScopedVersionValueCount", default=None
    )

    ca_global_app_domain_def_count: Optional[int] = FieldInfo(alias="caGlobalAppDomainDefCount", default=None)

    ca_global_app_domain_value_count: Optional[int] = FieldInfo(alias="caGlobalAppDomainValueCount", default=None)

    ca_global_def_parent_count: Optional[int] = FieldInfo(alias="caGlobalDefParentCount", default=None)

    ca_global_def_version_count: Optional[int] = FieldInfo(alias="caGlobalDefVersionCount", default=None)

    ca_global_parent_value_count: Optional[int] = FieldInfo(alias="caGlobalParentValueCount", default=None)

    ca_global_version_value_count: Optional[int] = FieldInfo(alias="caGlobalVersionValueCount", default=None)

    configuration_count: Optional[int] = FieldInfo(alias="configurationCount", default=None)

    configuration_template_count: Optional[int] = FieldInfo(alias="configurationTemplateCount", default=None)

    consumer_count: Optional[int] = FieldInfo(alias="consumerCount", default=None)

    custom_attribute_count: Optional[int] = FieldInfo(alias="customAttributeCount", default=None)

    custom_attribute_definition_count: Optional[int] = FieldInfo(alias="customAttributeDefinitionCount", default=None)

    domain_scoped_custom_attribute_count: Optional[int] = FieldInfo(
        alias="domainScopedCustomAttributeCount", default=None
    )

    enum_count: Optional[int] = FieldInfo(alias="enumCount", default=None)

    enum_value_count: Optional[int] = FieldInfo(alias="enumValueCount", default=None)

    enum_version_count: Optional[int] = FieldInfo(alias="enumVersionCount", default=None)

    environment_count: Optional[int] = FieldInfo(alias="environmentCount", default=None)

    environment_id_to_unique_applications_count: Optional[Dict[str, int]] = FieldInfo(
        alias="environmentIdToUniqueApplicationsCount", default=None
    )

    environment_id_to_unique_events_count: Optional[Dict[str, int]] = FieldInfo(
        alias="environmentIdToUniqueEventsCount", default=None
    )

    environment_id_to_unique_schemas_count: Optional[Dict[str, int]] = FieldInfo(
        alias="environmentIdToUniqueSchemasCount", default=None
    )

    event_api_count: Optional[int] = FieldInfo(alias="eventApiCount", default=None)

    event_api_product_count: Optional[int] = FieldInfo(alias="eventApiProductCount", default=None)

    event_api_product_version_count: Optional[int] = FieldInfo(alias="eventApiProductVersionCount", default=None)

    event_api_version_count: Optional[int] = FieldInfo(alias="eventApiVersionCount", default=None)

    event_count: Optional[int] = FieldInfo(alias="eventCount", default=None)

    event_mesh_count: Optional[int] = FieldInfo(alias="eventMeshCount", default=None)

    event_version_count: Optional[int] = FieldInfo(alias="eventVersionCount", default=None)

    message_service_count: Optional[int] = FieldInfo(alias="messageServiceCount", default=None)

    org_scoped_custom_attribute_count: Optional[int] = FieldInfo(alias="orgScopedCustomAttributeCount", default=None)

    published_event_api_product_version_count: Optional[int] = FieldInfo(
        alias="publishedEventApiProductVersionCount", default=None
    )

    schema_count: Optional[int] = FieldInfo(alias="schemaCount", default=None)

    schema_version_count: Optional[int] = FieldInfo(alias="schemaVersionCount", default=None)

    self_managed_event_management_agent_count: Optional[int] = FieldInfo(
        alias="selfManagedEventManagementAgentCount", default=None
    )

    subscription_count: Optional[int] = FieldInfo(alias="subscriptionCount", default=None)

    sum_unique_applications_in_each_environment_count: Optional[int] = FieldInfo(
        alias="sumUniqueApplicationsInEachEnvironmentCount", default=None
    )

    sum_unique_events_in_each_environment_count: Optional[int] = FieldInfo(
        alias="sumUniqueEventsInEachEnvironmentCount", default=None
    )

    sum_unique_schemas_in_each_environment_count: Optional[int] = FieldInfo(
        alias="sumUniqueSchemasInEachEnvironmentCount", default=None
    )

    type: Optional[str] = None


class ArchitectureGetEventPortalUsageStatsResponse(BaseModel):
    data: Optional[Data] = None

    meta: Optional[Dict[str, object]] = None
