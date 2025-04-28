# API

## V2

### Architecture

Types:

```python
from event_portal.types.api.v2 import (
    ArchitectureGetEventPortalUsageStatsResponse,
    ArchitectureGetStatesResponse,
)
```

Methods:

- <code title="delete /api/v2/architecture/eventApiProductMemAssociations/{memAssociationId}">client.api.v2.architecture.<a href="./src/event_portal/resources/api/v2/architecture/architecture.py">delete_event_api_product_mem_association</a>(mem_association_id) -> None</code>
- <code title="get /api/v2/architecture/eventPortalUsageStats">client.api.v2.architecture.<a href="./src/event_portal/resources/api/v2/architecture/architecture.py">get_event_portal_usage_stats</a>() -> <a href="./src/event_portal/types/api/v2/architecture_get_event_portal_usage_stats_response.py">ArchitectureGetEventPortalUsageStatsResponse</a></code>
- <code title="get /api/v2/architecture/states">client.api.v2.architecture.<a href="./src/event_portal/resources/api/v2/architecture/architecture.py">get_states</a>() -> <a href="./src/event_portal/types/api/v2/architecture_get_states_response.py">ArchitectureGetStatesResponse</a></code>

#### ChangeApplicationDomainOperations

Types:

```python
from event_portal.types.api.v2.architecture import ChangeApplicationDomainOperationRetrieveResponse
```

Methods:

- <code title="post /api/v2/architecture/changeApplicationDomainOperations">client.api.v2.architecture.change_application_domain_operations.<a href="./src/event_portal/resources/api/v2/architecture/change_application_domain_operations.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/change_application_domain_operation_create_params.py">params</a>) -> None</code>
- <code title="get /api/v2/architecture/changeApplicationDomainOperations/{id}">client.api.v2.architecture.change_application_domain_operations.<a href="./src/event_portal/resources/api/v2/architecture/change_application_domain_operations.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/change_application_domain_operation_retrieve_response.py">ChangeApplicationDomainOperationRetrieveResponse</a></code>

#### ApplicationDomains

Types:

```python
from event_portal.types.api.v2.architecture import (
    ApplicationDomain,
    ApplicationDomainResponse,
    CustomAttribute,
    Meta,
    ValidationMessageDto,
    ValidationMessagesDto,
    ApplicationDomainListResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/applicationDomains">client.api.v2.architecture.application_domains.<a href="./src/event_portal/resources/api/v2/architecture/application_domains/application_domains.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/application_domain_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_domain_response.py">ApplicationDomainResponse</a></code>
- <code title="get /api/v2/architecture/applicationDomains/{id}">client.api.v2.architecture.application_domains.<a href="./src/event_portal/resources/api/v2/architecture/application_domains/application_domains.py">retrieve</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/application_domain_retrieve_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_domain_response.py">ApplicationDomainResponse</a></code>
- <code title="patch /api/v2/architecture/applicationDomains/{id}">client.api.v2.architecture.application_domains.<a href="./src/event_portal/resources/api/v2/architecture/application_domains/application_domains.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/application_domain_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_domain_response.py">ApplicationDomainResponse</a></code>
- <code title="get /api/v2/architecture/applicationDomains">client.api.v2.architecture.application_domains.<a href="./src/event_portal/resources/api/v2/architecture/application_domains/application_domains.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/application_domain_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_domain_list_response.py">ApplicationDomainListResponse</a></code>
- <code title="delete /api/v2/architecture/applicationDomains/{id}">client.api.v2.architecture.application_domains.<a href="./src/event_portal/resources/api/v2/architecture/application_domains/application_domains.py">delete</a>(id) -> None</code>
- <code title="get /api/v2/architecture/applicationDomains/export/{ids}">client.api.v2.architecture.application_domains.<a href="./src/event_portal/resources/api/v2/architecture/application_domains/application_domains.py">export</a>(ids) -> BinaryAPIResponse</code>
- <code title="post /api/v2/architecture/applicationDomains/import">client.api.v2.architecture.application*domains.<a href="./src/event_portal/resources/api/v2/architecture/application_domains/application_domains.py">import*</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/application_domain_import_params.py">params</a>) -> None</code>

##### CustomAttributeDefinitions

Types:

```python
from event_portal.types.api.v2.architecture.application_domains import (
    CustomAttributeDefinition,
    CustomAttributeDefinitionResponse,
    CustomAttributeDefinitionsResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/applicationDomains/{applicationDomainId}/customAttributeDefinitions">client.api.v2.architecture.application_domains.custom_attribute_definitions.<a href="./src/event_portal/resources/api/v2/architecture/application_domains/custom_attribute_definitions.py">create</a>(path_application_domain_id, \*\*<a href="src/event_portal/types/api/v2/architecture/application_domains/custom_attribute_definition_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_domains/custom_attribute_definition_response.py">CustomAttributeDefinitionResponse</a></code>
- <code title="patch /api/v2/architecture/applicationDomains/{applicationDomainId}/customAttributeDefinitions/{customAttributeId}">client.api.v2.architecture.application_domains.custom_attribute_definitions.<a href="./src/event_portal/resources/api/v2/architecture/application_domains/custom_attribute_definitions.py">update</a>(custom_attribute_id, \*, path_application_domain_id, \*\*<a href="src/event_portal/types/api/v2/architecture/application_domains/custom_attribute_definition_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_domains/custom_attribute_definition_response.py">CustomAttributeDefinitionResponse</a></code>
- <code title="get /api/v2/architecture/applicationDomains/{applicationDomainId}/customAttributeDefinitions">client.api.v2.architecture.application_domains.custom_attribute_definitions.<a href="./src/event_portal/resources/api/v2/architecture/application_domains/custom_attribute_definitions.py">list</a>(application_domain_id, \*\*<a href="src/event_portal/types/api/v2/architecture/application_domains/custom_attribute_definition_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_domains/custom_attribute_definitions_response.py">CustomAttributeDefinitionsResponse</a></code>
- <code title="delete /api/v2/architecture/applicationDomains/{applicationDomainId}/customAttributeDefinitions">client.api.v2.architecture.application_domains.custom_attribute_definitions.<a href="./src/event_portal/resources/api/v2/architecture/application_domains/custom_attribute_definitions.py">delete</a>(application_domain_id) -> None</code>
- <code title="delete /api/v2/architecture/applicationDomains/{applicationDomainId}/customAttributeDefinitions/{customAttributeId}">client.api.v2.architecture.application_domains.custom_attribute_definitions.<a href="./src/event_portal/resources/api/v2/architecture/application_domains/custom_attribute_definitions.py">delete_by_id</a>(custom_attribute_id, \*, application_domain_id) -> None</code>

#### ApplicationVersions

Types:

```python
from event_portal.types.api.v2.architecture import (
    ApplicationVersion,
    ApplicationVersionEventAccessRequestsResponse,
    ApplicationVersionResponse,
    MessagingServiceAssociationDto,
    MessagingServiceAssociationResponse,
    StateChangeRequestResponse,
    VersionedObjectStateChangeRequest,
    ApplicationVersionListResponse,
    ApplicationVersionGetAsyncAPIResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/applicationVersions">client.api.v2.architecture.application_versions.<a href="./src/event_portal/resources/api/v2/architecture/application_versions/application_versions.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/application_version_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_version_response.py">ApplicationVersionResponse</a></code>
- <code title="get /api/v2/architecture/applicationVersions/{versionId}">client.api.v2.architecture.application_versions.<a href="./src/event_portal/resources/api/v2/architecture/application_versions/application_versions.py">retrieve</a>(version_id) -> <a href="./src/event_portal/types/api/v2/architecture/application_version_response.py">ApplicationVersionResponse</a></code>
- <code title="patch /api/v2/architecture/applicationVersions/{versionId}">client.api.v2.architecture.application_versions.<a href="./src/event_portal/resources/api/v2/architecture/application_versions/application_versions.py">update</a>(version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/application_version_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_version_response.py">ApplicationVersionResponse</a></code>
- <code title="get /api/v2/architecture/applicationVersions">client.api.v2.architecture.application_versions.<a href="./src/event_portal/resources/api/v2/architecture/application_versions/application_versions.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/application_version_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_version_list_response.py">ApplicationVersionListResponse</a></code>
- <code title="delete /api/v2/architecture/applicationVersions/{versionId}">client.api.v2.architecture.application_versions.<a href="./src/event_portal/resources/api/v2/architecture/application_versions/application_versions.py">delete</a>(version_id) -> None</code>
- <code title="get /api/v2/architecture/applicationVersions/{applicationVersionId}/asyncApi">client.api.v2.architecture.application_versions.<a href="./src/event_portal/resources/api/v2/architecture/application_versions/application_versions.py">get_async_api</a>(application_version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/application_version_get_async_api_params.py">params</a>) -> str</code>
- <code title="get /api/v2/architecture/applicationVersions/{applicationVersionId}/eventAccessRequestPreview">client.api.v2.architecture.application_versions.<a href="./src/event_portal/resources/api/v2/architecture/application_versions/application_versions.py">get_event_access_request_preview</a>(application_version_id) -> <a href="./src/event_portal/types/api/v2/architecture/application_version_event_access_requests_response.py">ApplicationVersionEventAccessRequestsResponse</a></code>
- <code title="put /api/v2/architecture/applicationVersions/{versionId}/messagingServices">client.api.v2.architecture.application_versions.<a href="./src/event_portal/resources/api/v2/architecture/application_versions/application_versions.py">replace_messaging_service</a>(version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/application_version_replace_messaging_service_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/messaging_service_association_response.py">MessagingServiceAssociationResponse</a></code>
- <code title="patch /api/v2/architecture/applicationVersions/{versionId}/state">client.api.v2.architecture.application_versions.<a href="./src/event_portal/resources/api/v2/architecture/application_versions/application_versions.py">update_state</a>(version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/application_version_update_state_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/state_change_request_response.py">StateChangeRequestResponse</a></code>

##### EventAccessRequests

Types:

```python
from event_portal.types.api.v2.architecture.application_versions import (
    EventAccessRequestsListResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/applicationVersions/{applicationVersionId}/eventAccessRequests">client.api.v2.architecture.application_versions.event_access_requests.<a href="./src/event_portal/resources/api/v2/architecture/application_versions/event_access_requests.py">create</a>(application_version_id) -> <a href="./src/event_portal/types/api/v2/architecture/application_versions/event_access_requests_list_response.py">EventAccessRequestsListResponse</a></code>
- <code title="get /api/v2/architecture/applicationVersions/{applicationVersionId}/eventAccessRequests">client.api.v2.architecture.application_versions.event_access_requests.<a href="./src/event_portal/resources/api/v2/architecture/application_versions/event_access_requests.py">list</a>(application_version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/application_versions/event_access_request_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_version_event_access_requests_response.py">ApplicationVersionEventAccessRequestsResponse</a></code>

##### Exports

Types:

```python
from event_portal.types.api.v2.architecture.application_versions import ExportGetAsyncAPIResponse
```

Methods:

- <code title="get /api/v2/architecture/applicationVersions/{applicationVersionId}/exports/asyncApi">client.api.v2.architecture.application_versions.exports.<a href="./src/event_portal/resources/api/v2/architecture/application_versions/exports.py">get_async_api</a>(application_version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/application_versions/export_get_async_api_params.py">params</a>) -> str</code>

#### About

Methods:

- <code title="get /api/v2/architecture/about/applications">client.api.v2.architecture.about.<a href="./src/event_portal/resources/api/v2/architecture/about.py">list_applications</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/about_list_applications_params.py">params</a>) -> BinaryAPIResponse</code>

#### Applications

Types:

```python
from event_portal.types.api.v2.architecture import (
    Application,
    ApplicationResponse,
    ApplicationListResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/applications">client.api.v2.architecture.applications.<a href="./src/event_portal/resources/api/v2/architecture/applications.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/application_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_response.py">ApplicationResponse</a></code>
- <code title="get /api/v2/architecture/applications/{id}">client.api.v2.architecture.applications.<a href="./src/event_portal/resources/api/v2/architecture/applications.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/application_response.py">ApplicationResponse</a></code>
- <code title="patch /api/v2/architecture/applications/{id}">client.api.v2.architecture.applications.<a href="./src/event_portal/resources/api/v2/architecture/applications.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/application_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_response.py">ApplicationResponse</a></code>
- <code title="get /api/v2/architecture/applications">client.api.v2.architecture.applications.<a href="./src/event_portal/resources/api/v2/architecture/applications.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/application_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_list_response.py">ApplicationListResponse</a></code>
- <code title="delete /api/v2/architecture/applications/{id}">client.api.v2.architecture.applications.<a href="./src/event_portal/resources/api/v2/architecture/applications.py">delete</a>(id) -> None</code>

#### ConfigurationTemplate

##### SolaceClientProfileNames

Types:

```python
from event_portal.types.api.v2.architecture.configuration_template import (
    SolaceClientProfileName,
    SolaceClientProfileNameConfigurationTemplateResponse,
    SolaceClientProfileNameListResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/configurationTemplate/solaceClientProfileNames">client.api.v2.architecture.configuration_template.solace_client_profile_names.<a href="./src/event_portal/resources/api/v2/architecture/configuration_template/solace_client_profile_names.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/configuration_template/solace_client_profile_name_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/configuration_template/solace_client_profile_name_configuration_template_response.py">SolaceClientProfileNameConfigurationTemplateResponse</a></code>
- <code title="get /api/v2/architecture/configurationTemplate/solaceClientProfileNames/{id}">client.api.v2.architecture.configuration_template.solace_client_profile_names.<a href="./src/event_portal/resources/api/v2/architecture/configuration_template/solace_client_profile_names.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/configuration_template/solace_client_profile_name_configuration_template_response.py">SolaceClientProfileNameConfigurationTemplateResponse</a></code>
- <code title="patch /api/v2/architecture/configurationTemplate/solaceClientProfileNames/{id}">client.api.v2.architecture.configuration_template.solace_client_profile_names.<a href="./src/event_portal/resources/api/v2/architecture/configuration_template/solace_client_profile_names.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/configuration_template/solace_client_profile_name_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/configuration_template/solace_client_profile_name_configuration_template_response.py">SolaceClientProfileNameConfigurationTemplateResponse</a></code>
- <code title="get /api/v2/architecture/configurationTemplate/solaceClientProfileNames">client.api.v2.architecture.configuration_template.solace_client_profile_names.<a href="./src/event_portal/resources/api/v2/architecture/configuration_template/solace_client_profile_names.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/configuration_template/solace_client_profile_name_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/configuration_template/solace_client_profile_name_list_response.py">SolaceClientProfileNameListResponse</a></code>
- <code title="delete /api/v2/architecture/configurationTemplate/solaceClientProfileNames/{id}">client.api.v2.architecture.configuration_template.solace_client_profile_names.<a href="./src/event_portal/resources/api/v2/architecture/configuration_template/solace_client_profile_names.py">delete</a>(id) -> None</code>

##### SolaceQueues

Types:

```python
from event_portal.types.api.v2.architecture.configuration_template import (
    SolaceQueueConfigurationTemplate,
    SolaceQueueConfigurationTemplateResponse,
    SolaceQueueListResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/configurationTemplate/solaceQueues">client.api.v2.architecture.configuration_template.solace_queues.<a href="./src/event_portal/resources/api/v2/architecture/configuration_template/solace_queues.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/configuration_template/solace_queue_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/configuration_template/solace_queue_configuration_template_response.py">SolaceQueueConfigurationTemplateResponse</a></code>
- <code title="get /api/v2/architecture/configurationTemplate/solaceQueues/{id}">client.api.v2.architecture.configuration_template.solace_queues.<a href="./src/event_portal/resources/api/v2/architecture/configuration_template/solace_queues.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/configuration_template/solace_queue_configuration_template_response.py">SolaceQueueConfigurationTemplateResponse</a></code>
- <code title="patch /api/v2/architecture/configurationTemplate/solaceQueues/{id}">client.api.v2.architecture.configuration_template.solace_queues.<a href="./src/event_portal/resources/api/v2/architecture/configuration_template/solace_queues.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/configuration_template/solace_queue_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/configuration_template/solace_queue_configuration_template_response.py">SolaceQueueConfigurationTemplateResponse</a></code>
- <code title="get /api/v2/architecture/configurationTemplate/solaceQueues">client.api.v2.architecture.configuration_template.solace_queues.<a href="./src/event_portal/resources/api/v2/architecture/configuration_template/solace_queues.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/configuration_template/solace_queue_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/configuration_template/solace_queue_list_response.py">SolaceQueueListResponse</a></code>
- <code title="delete /api/v2/architecture/configurationTemplate/solaceQueues/{id}">client.api.v2.architecture.configuration_template.solace_queues.<a href="./src/event_portal/resources/api/v2/architecture/configuration_template/solace_queues.py">delete</a>(id) -> None</code>

#### ConfigurationTypes

Types:

```python
from event_portal.types.api.v2.architecture import (
    ConfigurationType,
    ConfigurationTypeRetrieveResponse,
    ConfigurationTypeListResponse,
)
```

Methods:

- <code title="get /api/v2/architecture/configurationTypes/{id}">client.api.v2.architecture.configuration_types.<a href="./src/event_portal/resources/api/v2/architecture/configuration_types.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/configuration_type_retrieve_response.py">ConfigurationTypeRetrieveResponse</a></code>
- <code title="get /api/v2/architecture/configurationTypes">client.api.v2.architecture.configuration_types.<a href="./src/event_portal/resources/api/v2/architecture/configuration_types.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/configuration_type_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/configuration_type_list_response.py">ConfigurationTypeListResponse</a></code>

#### Consumers

Types:

```python
from event_portal.types.api.v2.architecture import (
    Consumer,
    ConsumerRequest,
    ConsumerResponse,
    Subscription,
    ConsumerListResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/consumers">client.api.v2.architecture.consumers.<a href="./src/event_portal/resources/api/v2/architecture/consumers.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/consumer_create_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="get /api/v2/architecture/consumers/{id}">client.api.v2.architecture.consumers.<a href="./src/event_portal/resources/api/v2/architecture/consumers.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/consumer_response.py">ConsumerResponse</a></code>
- <code title="patch /api/v2/architecture/consumers/{id}">client.api.v2.architecture.consumers.<a href="./src/event_portal/resources/api/v2/architecture/consumers.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/consumer_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/consumer_response.py">ConsumerResponse</a></code>
- <code title="get /api/v2/architecture/consumers">client.api.v2.architecture.consumers.<a href="./src/event_portal/resources/api/v2/architecture/consumers.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/consumer_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/consumer_list_response.py">ConsumerListResponse</a></code>
- <code title="delete /api/v2/architecture/consumers/{id}">client.api.v2.architecture.consumers.<a href="./src/event_portal/resources/api/v2/architecture/consumers.py">delete</a>(id) -> None</code>

#### CustomAttributeDefinitions

Methods:

- <code title="post /api/v2/architecture/customAttributeDefinitions">client.api.v2.architecture.custom_attribute_definitions.<a href="./src/event_portal/resources/api/v2/architecture/custom_attribute_definitions.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/custom_attribute_definition_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_domains/custom_attribute_definition_response.py">CustomAttributeDefinitionResponse</a></code>
- <code title="get /api/v2/architecture/customAttributeDefinitions/{id}">client.api.v2.architecture.custom_attribute_definitions.<a href="./src/event_portal/resources/api/v2/architecture/custom_attribute_definitions.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/application_domains/custom_attribute_definition_response.py">CustomAttributeDefinitionResponse</a></code>
- <code title="patch /api/v2/architecture/customAttributeDefinitions/{id}">client.api.v2.architecture.custom_attribute_definitions.<a href="./src/event_portal/resources/api/v2/architecture/custom_attribute_definitions.py">update</a>(path_id, \*\*<a href="src/event_portal/types/api/v2/architecture/custom_attribute_definition_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_domains/custom_attribute_definition_response.py">CustomAttributeDefinitionResponse</a></code>
- <code title="get /api/v2/architecture/customAttributeDefinitions">client.api.v2.architecture.custom_attribute_definitions.<a href="./src/event_portal/resources/api/v2/architecture/custom_attribute_definitions.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/custom_attribute_definition_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_domains/custom_attribute_definitions_response.py">CustomAttributeDefinitionsResponse</a></code>
- <code title="delete /api/v2/architecture/customAttributeDefinitions/{id}">client.api.v2.architecture.custom_attribute_definitions.<a href="./src/event_portal/resources/api/v2/architecture/custom_attribute_definitions.py">delete</a>(id) -> None</code>

#### Designer

##### Configuration

###### SolaceAuthorizationGroups

Types:

```python
from event_portal.types.api.v2.architecture.designer.configuration import (
    Configuration,
    ConfigurationResponse,
    ConfigurationsResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/designer/configuration/solaceAuthorizationGroups">client.api.v2.architecture.designer.configuration.solace_authorization_groups.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_authorization_groups.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/designer/configuration/solace_authorization_group_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/designer/configuration/configuration_response.py">ConfigurationResponse</a></code>
- <code title="get /api/v2/architecture/designer/configuration/solaceAuthorizationGroups/{id}">client.api.v2.architecture.designer.configuration.solace_authorization_groups.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_authorization_groups.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/designer/configuration/configuration_response.py">ConfigurationResponse</a></code>
- <code title="get /api/v2/architecture/designer/configuration/solaceAuthorizationGroups">client.api.v2.architecture.designer.configuration.solace_authorization_groups.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_authorization_groups.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/designer/configuration/solace_authorization_group_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/designer/configuration/configurations_response.py">ConfigurationsResponse</a></code>
- <code title="delete /api/v2/architecture/designer/configuration/solaceAuthorizationGroups/{id}">client.api.v2.architecture.designer.configuration.solace_authorization_groups.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_authorization_groups.py">delete</a>(id) -> None</code>

###### SolaceClientProfileNames

Methods:

- <code title="post /api/v2/architecture/designer/configuration/solaceClientProfileNames">client.api.v2.architecture.designer.configuration.solace_client_profile_names.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_client_profile_names.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/designer/configuration/solace_client_profile_name_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/designer/configuration/configuration_response.py">ConfigurationResponse</a></code>
- <code title="get /api/v2/architecture/designer/configuration/solaceClientProfileNames/{id}">client.api.v2.architecture.designer.configuration.solace_client_profile_names.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_client_profile_names.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/designer/configuration/configuration_response.py">ConfigurationResponse</a></code>
- <code title="get /api/v2/architecture/designer/configuration/solaceClientProfileNames">client.api.v2.architecture.designer.configuration.solace_client_profile_names.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_client_profile_names.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/designer/configuration/solace_client_profile_name_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/designer/configuration/configurations_response.py">ConfigurationsResponse</a></code>
- <code title="delete /api/v2/architecture/designer/configuration/solaceClientProfileNames/{id}">client.api.v2.architecture.designer.configuration.solace_client_profile_names.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_client_profile_names.py">delete</a>(id) -> None</code>

###### SolaceClientUsernames

Methods:

- <code title="post /api/v2/architecture/designer/configuration/solaceClientUsernames">client.api.v2.architecture.designer.configuration.solace_client_usernames.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_client_usernames.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/designer/configuration/solace_client_username_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/designer/configuration/configuration_response.py">ConfigurationResponse</a></code>
- <code title="get /api/v2/architecture/designer/configuration/solaceClientUsernames/{id}">client.api.v2.architecture.designer.configuration.solace_client_usernames.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_client_usernames.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/designer/configuration/configuration_response.py">ConfigurationResponse</a></code>
- <code title="get /api/v2/architecture/designer/configuration/solaceClientUsernames">client.api.v2.architecture.designer.configuration.solace_client_usernames.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_client_usernames.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/designer/configuration/solace_client_username_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/designer/configuration/configurations_response.py">ConfigurationsResponse</a></code>
- <code title="delete /api/v2/architecture/designer/configuration/solaceClientUsernames/{id}">client.api.v2.architecture.designer.configuration.solace_client_usernames.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_client_usernames.py">delete</a>(id) -> None</code>

###### SolaceQueues

Methods:

- <code title="post /api/v2/architecture/designer/configuration/solaceQueues">client.api.v2.architecture.designer.configuration.solace_queues.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_queues.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/designer/configuration/solace_queue_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/designer/configuration/configuration_response.py">ConfigurationResponse</a></code>
- <code title="get /api/v2/architecture/designer/configuration/solaceQueues/{id}">client.api.v2.architecture.designer.configuration.solace_queues.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_queues.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/designer/configuration/configuration_response.py">ConfigurationResponse</a></code>
- <code title="get /api/v2/architecture/designer/configuration/solaceQueues">client.api.v2.architecture.designer.configuration.solace_queues.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_queues.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/designer/configuration/solace_queue_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/designer/configuration/configurations_response.py">ConfigurationsResponse</a></code>
- <code title="delete /api/v2/architecture/designer/configuration/solaceQueues/{id}">client.api.v2.architecture.designer.configuration.solace_queues.<a href="./src/event_portal/resources/api/v2/architecture/designer/configuration/solace_queues.py">delete</a>(id) -> None</code>

#### EnumVersions

Types:

```python
from event_portal.types.api.v2.architecture import (
    TopicAddressEnumVersion,
    TopicAddressEnumVersionResponse,
    EnumVersionListResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/enumVersions">client.api.v2.architecture.enum_versions.<a href="./src/event_portal/resources/api/v2/architecture/enum_versions.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/enum_version_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/topic_address_enum_version_response.py">TopicAddressEnumVersionResponse</a></code>
- <code title="get /api/v2/architecture/enumVersions/{versionId}">client.api.v2.architecture.enum_versions.<a href="./src/event_portal/resources/api/v2/architecture/enum_versions.py">retrieve</a>(version_id) -> <a href="./src/event_portal/types/api/v2/architecture/topic_address_enum_version_response.py">TopicAddressEnumVersionResponse</a></code>
- <code title="patch /api/v2/architecture/enumVersions/{id}">client.api.v2.architecture.enum_versions.<a href="./src/event_portal/resources/api/v2/architecture/enum_versions.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/enum_version_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/topic_address_enum_version_response.py">TopicAddressEnumVersionResponse</a></code>
- <code title="get /api/v2/architecture/enumVersions">client.api.v2.architecture.enum_versions.<a href="./src/event_portal/resources/api/v2/architecture/enum_versions.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/enum_version_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/enum_version_list_response.py">EnumVersionListResponse</a></code>
- <code title="delete /api/v2/architecture/enumVersions/{id}">client.api.v2.architecture.enum_versions.<a href="./src/event_portal/resources/api/v2/architecture/enum_versions.py">delete</a>(id) -> None</code>
- <code title="patch /api/v2/architecture/enumVersions/{id}/state">client.api.v2.architecture.enum_versions.<a href="./src/event_portal/resources/api/v2/architecture/enum_versions.py">update_state</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/enum_version_update_state_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/state_change_request_response.py">StateChangeRequestResponse</a></code>

#### Enums

Types:

```python
from event_portal.types.api.v2.architecture import (
    TopicAddressEnum,
    TopicAddressEnumResponse,
    EnumListResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/enums">client.api.v2.architecture.enums.<a href="./src/event_portal/resources/api/v2/architecture/enums.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/enum_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/topic_address_enum_response.py">TopicAddressEnumResponse</a></code>
- <code title="get /api/v2/architecture/enums/{id}">client.api.v2.architecture.enums.<a href="./src/event_portal/resources/api/v2/architecture/enums.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/topic_address_enum_response.py">TopicAddressEnumResponse</a></code>
- <code title="patch /api/v2/architecture/enums/{id}">client.api.v2.architecture.enums.<a href="./src/event_portal/resources/api/v2/architecture/enums.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/enum_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/topic_address_enum_response.py">TopicAddressEnumResponse</a></code>
- <code title="get /api/v2/architecture/enums">client.api.v2.architecture.enums.<a href="./src/event_portal/resources/api/v2/architecture/enums.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/enum_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/enum_list_response.py">EnumListResponse</a></code>
- <code title="delete /api/v2/architecture/enums/{id}">client.api.v2.architecture.enums.<a href="./src/event_portal/resources/api/v2/architecture/enums.py">delete</a>(id) -> None</code>

#### EventAPIProductVersions

Types:

```python
from event_portal.types.api.v2.architecture import (
    EventAPIProductVersion,
    EventAPIProductVersionResponse,
    EventAPIProductVersionListResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/eventApiProductVersions">client.api.v2.architecture.event_api_product_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_api_product_versions/event_api_product_versions.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_api_product_version_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_product_version_response.py">EventAPIProductVersionResponse</a></code>
- <code title="get /api/v2/architecture/eventApiProductVersions/{versionId}">client.api.v2.architecture.event_api_product_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_api_product_versions/event_api_product_versions.py">retrieve</a>(version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_api_product_version_retrieve_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_product_version_response.py">EventAPIProductVersionResponse</a></code>
- <code title="patch /api/v2/architecture/eventApiProductVersions/{versionId}">client.api.v2.architecture.event_api_product_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_api_product_versions/event_api_product_versions.py">update</a>(version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_api_product_version_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_product_version_response.py">EventAPIProductVersionResponse</a></code>
- <code title="get /api/v2/architecture/eventApiProductVersions">client.api.v2.architecture.event_api_product_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_api_product_versions/event_api_product_versions.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_api_product_version_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_product_version_list_response.py">EventAPIProductVersionListResponse</a></code>
- <code title="delete /api/v2/architecture/eventApiProductVersions/{versionId}">client.api.v2.architecture.event_api_product_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_api_product_versions/event_api_product_versions.py">delete</a>(version_id) -> None</code>
- <code title="patch /api/v2/architecture/eventApiProductVersions/{versionId}/publish">client.api.v2.architecture.event_api_product_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_api_product_versions/event_api_product_versions.py">publish</a>(version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_api_product_version_publish_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/state_change_request_response.py">StateChangeRequestResponse</a></code>
- <code title="patch /api/v2/architecture/eventApiProductVersions/{versionId}/state">client.api.v2.architecture.event_api_product_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_api_product_versions/event_api_product_versions.py">update_state</a>(version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_api_product_version_update_state_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/state_change_request_response.py">StateChangeRequestResponse</a></code>

##### MemAssociations

Types:

```python
from event_portal.types.api.v2.architecture.event_api_product_versions import (
    GatewayMessagingService,
    MemAssociationCreateResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/eventApiProductVersions/{eventApiProductVersionId}/memAssociations">client.api.v2.architecture.event_api_product_versions.mem_associations.<a href="./src/event_portal/resources/api/v2/architecture/event_api_product_versions/mem_associations.py">create</a>(path_event_api_product_version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_api_product_versions/mem_association_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_product_versions/mem_association_create_response.py">MemAssociationCreateResponse</a></code>
- <code title="delete /api/v2/architecture/eventApiProductVersions/{eventApiProductVersionId}/memAssociations/{memAssociationId}">client.api.v2.architecture.event_api_product_versions.mem_associations.<a href="./src/event_portal/resources/api/v2/architecture/event_api_product_versions/mem_associations.py">delete</a>(mem_association_id, \*, event_api_product_version_id) -> None</code>

#### EventAPIProducts

Types:

```python
from event_portal.types.api.v2.architecture import (
    EventAPIProduct,
    EventAPIProductResponse,
    EventAPIProductListResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/eventApiProducts">client.api.v2.architecture.event_api_products.<a href="./src/event_portal/resources/api/v2/architecture/event_api_products.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_api_product_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_product_response.py">EventAPIProductResponse</a></code>
- <code title="get /api/v2/architecture/eventApiProducts/{id}">client.api.v2.architecture.event_api_products.<a href="./src/event_portal/resources/api/v2/architecture/event_api_products.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_product_response.py">EventAPIProductResponse</a></code>
- <code title="patch /api/v2/architecture/eventApiProducts/{id}">client.api.v2.architecture.event_api_products.<a href="./src/event_portal/resources/api/v2/architecture/event_api_products.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_api_product_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_product_response.py">EventAPIProductResponse</a></code>
- <code title="get /api/v2/architecture/eventApiProducts">client.api.v2.architecture.event_api_products.<a href="./src/event_portal/resources/api/v2/architecture/event_api_products.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_api_product_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_product_list_response.py">EventAPIProductListResponse</a></code>
- <code title="delete /api/v2/architecture/eventApiProducts/{id}">client.api.v2.architecture.event_api_products.<a href="./src/event_portal/resources/api/v2/architecture/event_api_products.py">delete</a>(id) -> None</code>

#### EventAPIVersions

Types:

```python
from event_portal.types.api.v2.architecture import (
    EventAPIVersion,
    EventAPIVersionResponse,
    EventAPIVersionListResponse,
    EventAPIVersionGetAsyncAPIResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/eventApiVersions">client.api.v2.architecture.event_api_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_api_versions/event_api_versions.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_api_version_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_version_response.py">EventAPIVersionResponse</a></code>
- <code title="get /api/v2/architecture/eventApiVersions/{versionId}">client.api.v2.architecture.event_api_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_api_versions/event_api_versions.py">retrieve</a>(version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_api_version_retrieve_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_version_response.py">EventAPIVersionResponse</a></code>
- <code title="patch /api/v2/architecture/eventApiVersions/{versionId}">client.api.v2.architecture.event_api_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_api_versions/event_api_versions.py">update</a>(version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_api_version_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_version_response.py">EventAPIVersionResponse</a></code>
- <code title="get /api/v2/architecture/eventApiVersions">client.api.v2.architecture.event_api_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_api_versions/event_api_versions.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_api_version_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_version_list_response.py">EventAPIVersionListResponse</a></code>
- <code title="delete /api/v2/architecture/eventApiVersions/{versionId}">client.api.v2.architecture.event_api_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_api_versions/event_api_versions.py">delete</a>(version_id) -> None</code>
- <code title="get /api/v2/architecture/eventApiVersions/{eventApiVersionId}/asyncApi">client.api.v2.architecture.event_api_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_api_versions/event_api_versions.py">get_async_api</a>(event_api_version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_api_version_get_async_api_params.py">params</a>) -> str</code>
- <code title="patch /api/v2/architecture/eventApiVersions/{versionId}/state">client.api.v2.architecture.event_api_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_api_versions/event_api_versions.py">update_state</a>(version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_api_version_update_state_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/state_change_request_response.py">StateChangeRequestResponse</a></code>

##### Exports

Types:

```python
from event_portal.types.api.v2.architecture.event_api_versions import ExportGetAsyncAPIResponse
```

Methods:

- <code title="get /api/v2/architecture/eventApiVersions/{eventApiVersionId}/exports/asyncApi">client.api.v2.architecture.event_api_versions.exports.<a href="./src/event_portal/resources/api/v2/architecture/event_api_versions/exports.py">get_async_api</a>(event_api_version_id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_api_versions/export_get_async_api_params.py">params</a>) -> str</code>

#### EventAPIs

Types:

```python
from event_portal.types.api.v2.architecture import EventAPI, EventAPIResponse, EventAPIListResponse
```

Methods:

- <code title="post /api/v2/architecture/eventApis">client.api.v2.architecture.event_apis.<a href="./src/event_portal/resources/api/v2/architecture/event_apis.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_api_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_response.py">EventAPIResponse</a></code>
- <code title="get /api/v2/architecture/eventApis/{id}">client.api.v2.architecture.event_apis.<a href="./src/event_portal/resources/api/v2/architecture/event_apis.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_response.py">EventAPIResponse</a></code>
- <code title="patch /api/v2/architecture/eventApis/{id}">client.api.v2.architecture.event_apis.<a href="./src/event_portal/resources/api/v2/architecture/event_apis.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_api_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_response.py">EventAPIResponse</a></code>
- <code title="get /api/v2/architecture/eventApis">client.api.v2.architecture.event_apis.<a href="./src/event_portal/resources/api/v2/architecture/event_apis.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_api_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_api_list_response.py">EventAPIListResponse</a></code>
- <code title="delete /api/v2/architecture/eventApis/{id}">client.api.v2.architecture.event_apis.<a href="./src/event_portal/resources/api/v2/architecture/event_apis.py">delete</a>(id) -> None</code>

#### EventAccessRequests

Types:

```python
from event_portal.types.api.v2.architecture import (
    ApproveDeclineRequest,
    EventAccessRequest,
    EventAccessRequestResponse,
    ReviewResponse,
)
```

Methods:

- <code title="get /api/v2/architecture/eventAccessRequests/{id}">client.api.v2.architecture.event_access_requests.<a href="./src/event_portal/resources/api/v2/architecture/event_access_requests.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/event_access_request_response.py">EventAccessRequestResponse</a></code>
- <code title="patch /api/v2/architecture/eventAccessRequests/{id}">client.api.v2.architecture.event_access_requests.<a href="./src/event_portal/resources/api/v2/architecture/event_access_requests.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_access_request_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_access_request_response.py">EventAccessRequestResponse</a></code>
- <code title="get /api/v2/architecture/eventAccessRequests">client.api.v2.architecture.event_access_requests.<a href="./src/event_portal/resources/api/v2/architecture/event_access_requests.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_access_request_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/application_versions/event_access_requests_list_response.py">EventAccessRequestsListResponse</a></code>
- <code title="post /api/v2/architecture/eventAccessRequests/{id}/approve">client.api.v2.architecture.event_access_requests.<a href="./src/event_portal/resources/api/v2/architecture/event_access_requests.py">approve</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_access_request_approve_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/review_response.py">ReviewResponse</a></code>
- <code title="post /api/v2/architecture/eventAccessRequests/{id}/decline">client.api.v2.architecture.event_access_requests.<a href="./src/event_portal/resources/api/v2/architecture/event_access_requests.py">decline</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_access_request_decline_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/review_response.py">ReviewResponse</a></code>

#### EventAccessReviews

Types:

```python
from event_portal.types.api.v2.architecture import Review, EventAccessReviewListResponse
```

Methods:

- <code title="post /api/v2/architecture/eventAccessReviews">client.api.v2.architecture.event_access_reviews.<a href="./src/event_portal/resources/api/v2/architecture/event_access_reviews.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_access_review_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/review_response.py">ReviewResponse</a></code>
- <code title="get /api/v2/architecture/eventAccessReviews/{id}">client.api.v2.architecture.event_access_reviews.<a href="./src/event_portal/resources/api/v2/architecture/event_access_reviews.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/review_response.py">ReviewResponse</a></code>
- <code title="patch /api/v2/architecture/eventAccessReviews/{id}">client.api.v2.architecture.event_access_reviews.<a href="./src/event_portal/resources/api/v2/architecture/event_access_reviews.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_access_review_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/review_response.py">ReviewResponse</a></code>
- <code title="get /api/v2/architecture/eventAccessReviews">client.api.v2.architecture.event_access_reviews.<a href="./src/event_portal/resources/api/v2/architecture/event_access_reviews.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_access_review_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_access_review_list_response.py">EventAccessReviewListResponse</a></code>
- <code title="delete /api/v2/architecture/eventAccessReviews/{id}">client.api.v2.architecture.event_access_reviews.<a href="./src/event_portal/resources/api/v2/architecture/event_access_reviews.py">delete</a>(id) -> None</code>

#### EventVersions

Types:

```python
from event_portal.types.api.v2.architecture import (
    Address,
    DeliveryDescriptor,
    EventVersion,
    EventVersionResponse,
    EventVersionListResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/eventVersions">client.api.v2.architecture.event_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_versions.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_version_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_version_response.py">EventVersionResponse</a></code>
- <code title="get /api/v2/architecture/eventVersions/{id}">client.api.v2.architecture.event_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_versions.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/event_version_response.py">EventVersionResponse</a></code>
- <code title="patch /api/v2/architecture/eventVersions/{id}">client.api.v2.architecture.event_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_versions.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_version_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_version_response.py">EventVersionResponse</a></code>
- <code title="get /api/v2/architecture/eventVersions">client.api.v2.architecture.event_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_versions.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_version_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_version_list_response.py">EventVersionListResponse</a></code>
- <code title="delete /api/v2/architecture/eventVersions/{id}">client.api.v2.architecture.event_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_versions.py">delete</a>(id) -> None</code>
- <code title="put /api/v2/architecture/eventVersions/{id}/messagingServices">client.api.v2.architecture.event_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_versions.py">replace_messaging_service</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_version_replace_messaging_service_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/messaging_service_association_response.py">MessagingServiceAssociationResponse</a></code>
- <code title="patch /api/v2/architecture/eventVersions/{id}/state">client.api.v2.architecture.event_versions.<a href="./src/event_portal/resources/api/v2/architecture/event_versions.py">update_state</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_version_update_state_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/state_change_request_response.py">StateChangeRequestResponse</a></code>

#### Events

Types:

```python
from event_portal.types.api.v2.architecture import Event, EventResponse
```

Methods:

- <code title="post /api/v2/architecture/events">client.api.v2.architecture.events.<a href="./src/event_portal/resources/api/v2/architecture/events.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_response.py">EventResponse</a></code>
- <code title="get /api/v2/architecture/events/{id}">client.api.v2.architecture.events.<a href="./src/event_portal/resources/api/v2/architecture/events.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/event_response.py">EventResponse</a></code>
- <code title="patch /api/v2/architecture/events/{id}">client.api.v2.architecture.events.<a href="./src/event_portal/resources/api/v2/architecture/events.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/event_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/event_response.py">EventResponse</a></code>
- <code title="get /api/v2/architecture/events">client.api.v2.architecture.events.<a href="./src/event_portal/resources/api/v2/architecture/events.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/event_list_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="delete /api/v2/architecture/events/{id}">client.api.v2.architecture.events.<a href="./src/event_portal/resources/api/v2/architecture/events.py">delete</a>(id) -> None</code>

#### SchemaVersions

Types:

```python
from event_portal.types.api.v2.architecture import (
    SchemaVersion,
    SchemaVersionResponse,
    SchemaVersionListResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/schemaVersions">client.api.v2.architecture.schema_versions.<a href="./src/event_portal/resources/api/v2/architecture/schema_versions.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/schema_version_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/schema_version_response.py">SchemaVersionResponse</a></code>
- <code title="get /api/v2/architecture/schemaVersions/{versionId}">client.api.v2.architecture.schema_versions.<a href="./src/event_portal/resources/api/v2/architecture/schema_versions.py">retrieve</a>(version_id) -> <a href="./src/event_portal/types/api/v2/architecture/schema_version_response.py">SchemaVersionResponse</a></code>
- <code title="patch /api/v2/architecture/schemaVersions/{id}">client.api.v2.architecture.schema_versions.<a href="./src/event_portal/resources/api/v2/architecture/schema_versions.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/schema_version_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/schema_version_response.py">SchemaVersionResponse</a></code>
- <code title="get /api/v2/architecture/schemaVersions">client.api.v2.architecture.schema_versions.<a href="./src/event_portal/resources/api/v2/architecture/schema_versions.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/schema_version_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/schema_version_list_response.py">SchemaVersionListResponse</a></code>
- <code title="delete /api/v2/architecture/schemaVersions/{id}">client.api.v2.architecture.schema_versions.<a href="./src/event_portal/resources/api/v2/architecture/schema_versions.py">delete</a>(id) -> None</code>
- <code title="patch /api/v2/architecture/schemaVersions/{id}/state">client.api.v2.architecture.schema_versions.<a href="./src/event_portal/resources/api/v2/architecture/schema_versions.py">update_state</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/schema_version_update_state_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/state_change_request_response.py">StateChangeRequestResponse</a></code>

#### Schemas

Types:

```python
from event_portal.types.api.v2.architecture import SchemaObject, SchemaResponse, SchemaListResponse
```

Methods:

- <code title="post /api/v2/architecture/schemas">client.api.v2.architecture.schemas.<a href="./src/event_portal/resources/api/v2/architecture/schemas.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/schema_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/schema_response.py">SchemaResponse</a></code>
- <code title="get /api/v2/architecture/schemas/{id}">client.api.v2.architecture.schemas.<a href="./src/event_portal/resources/api/v2/architecture/schemas.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/schema_response.py">SchemaResponse</a></code>
- <code title="patch /api/v2/architecture/schemas/{id}">client.api.v2.architecture.schemas.<a href="./src/event_portal/resources/api/v2/architecture/schemas.py">update</a>(id, \*\*<a href="src/event_portal/types/api/v2/architecture/schema_update_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/schema_response.py">SchemaResponse</a></code>
- <code title="get /api/v2/architecture/schemas">client.api.v2.architecture.schemas.<a href="./src/event_portal/resources/api/v2/architecture/schemas.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/schema_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/schema_list_response.py">SchemaListResponse</a></code>
- <code title="delete /api/v2/architecture/schemas/{id}">client.api.v2.architecture.schemas.<a href="./src/event_portal/resources/api/v2/architecture/schemas.py">delete</a>(id) -> None</code>

#### TopicDomains

Types:

```python
from event_portal.types.api.v2.architecture import (
    AddressLevel,
    TopicDomain,
    TopicDomainResponse,
    TopicDomainListResponse,
)
```

Methods:

- <code title="post /api/v2/architecture/topicDomains">client.api.v2.architecture.topic_domains.<a href="./src/event_portal/resources/api/v2/architecture/topic_domains.py">create</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/topic_domain_create_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/topic_domain_response.py">TopicDomainResponse</a></code>
- <code title="get /api/v2/architecture/topicDomains/{id}">client.api.v2.architecture.topic_domains.<a href="./src/event_portal/resources/api/v2/architecture/topic_domains.py">retrieve</a>(id) -> <a href="./src/event_portal/types/api/v2/architecture/topic_domain_response.py">TopicDomainResponse</a></code>
- <code title="get /api/v2/architecture/topicDomains">client.api.v2.architecture.topic_domains.<a href="./src/event_portal/resources/api/v2/architecture/topic_domains.py">list</a>(\*\*<a href="src/event_portal/types/api/v2/architecture/topic_domain_list_params.py">params</a>) -> <a href="./src/event_portal/types/api/v2/architecture/topic_domain_list_response.py">TopicDomainListResponse</a></code>
- <code title="delete /api/v2/architecture/topicDomains/{id}">client.api.v2.architecture.topic_domains.<a href="./src/event_portal/resources/api/v2/architecture/topic_domains.py">delete</a>(id) -> BinaryAPIResponse</code>
