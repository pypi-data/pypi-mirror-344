# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from .about import (
    AboutResource,
    AsyncAboutResource,
    AboutResourceWithRawResponse,
    AsyncAboutResourceWithRawResponse,
    AboutResourceWithStreamingResponse,
    AsyncAboutResourceWithStreamingResponse,
)
from .enums import (
    EnumsResource,
    AsyncEnumsResource,
    EnumsResourceWithRawResponse,
    AsyncEnumsResourceWithRawResponse,
    EnumsResourceWithStreamingResponse,
    AsyncEnumsResourceWithStreamingResponse,
)
from .events import (
    EventsResource,
    AsyncEventsResource,
    EventsResourceWithRawResponse,
    AsyncEventsResourceWithRawResponse,
    EventsResourceWithStreamingResponse,
    AsyncEventsResourceWithStreamingResponse,
)
from .schemas import (
    SchemasResource,
    AsyncSchemasResource,
    SchemasResourceWithRawResponse,
    AsyncSchemasResourceWithRawResponse,
    SchemasResourceWithStreamingResponse,
    AsyncSchemasResourceWithStreamingResponse,
)
from .consumers import (
    ConsumersResource,
    AsyncConsumersResource,
    ConsumersResourceWithRawResponse,
    AsyncConsumersResourceWithRawResponse,
    ConsumersResourceWithStreamingResponse,
    AsyncConsumersResourceWithStreamingResponse,
)
from ....._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from .event_apis import (
    EventAPIsResource,
    AsyncEventAPIsResource,
    EventAPIsResourceWithRawResponse,
    AsyncEventAPIsResourceWithRawResponse,
    EventAPIsResourceWithStreamingResponse,
    AsyncEventAPIsResourceWithStreamingResponse,
)
from ....._compat import cached_property
from .applications import (
    ApplicationsResource,
    AsyncApplicationsResource,
    ApplicationsResourceWithRawResponse,
    AsyncApplicationsResourceWithRawResponse,
    ApplicationsResourceWithStreamingResponse,
    AsyncApplicationsResourceWithStreamingResponse,
)
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .enum_versions import (
    EnumVersionsResource,
    AsyncEnumVersionsResource,
    EnumVersionsResourceWithRawResponse,
    AsyncEnumVersionsResourceWithRawResponse,
    EnumVersionsResourceWithStreamingResponse,
    AsyncEnumVersionsResourceWithStreamingResponse,
)
from .topic_domains import (
    TopicDomainsResource,
    AsyncTopicDomainsResource,
    TopicDomainsResourceWithRawResponse,
    AsyncTopicDomainsResourceWithRawResponse,
    TopicDomainsResourceWithStreamingResponse,
    AsyncTopicDomainsResourceWithStreamingResponse,
)
from .event_versions import (
    EventVersionsResource,
    AsyncEventVersionsResource,
    EventVersionsResourceWithRawResponse,
    AsyncEventVersionsResourceWithRawResponse,
    EventVersionsResourceWithStreamingResponse,
    AsyncEventVersionsResourceWithStreamingResponse,
)
from .schema_versions import (
    SchemaVersionsResource,
    AsyncSchemaVersionsResource,
    SchemaVersionsResourceWithRawResponse,
    AsyncSchemaVersionsResourceWithRawResponse,
    SchemaVersionsResourceWithStreamingResponse,
    AsyncSchemaVersionsResourceWithStreamingResponse,
)
from ....._base_client import make_request_options
from .designer.designer import (
    DesignerResource,
    AsyncDesignerResource,
    DesignerResourceWithRawResponse,
    AsyncDesignerResourceWithRawResponse,
    DesignerResourceWithStreamingResponse,
    AsyncDesignerResourceWithStreamingResponse,
)
from .event_api_products import (
    EventAPIProductsResource,
    AsyncEventAPIProductsResource,
    EventAPIProductsResourceWithRawResponse,
    AsyncEventAPIProductsResourceWithRawResponse,
    EventAPIProductsResourceWithStreamingResponse,
    AsyncEventAPIProductsResourceWithStreamingResponse,
)
from .configuration_types import (
    ConfigurationTypesResource,
    AsyncConfigurationTypesResource,
    ConfigurationTypesResourceWithRawResponse,
    AsyncConfigurationTypesResourceWithRawResponse,
    ConfigurationTypesResourceWithStreamingResponse,
    AsyncConfigurationTypesResourceWithStreamingResponse,
)
from .event_access_reviews import (
    EventAccessReviewsResource,
    AsyncEventAccessReviewsResource,
    EventAccessReviewsResourceWithRawResponse,
    AsyncEventAccessReviewsResourceWithRawResponse,
    EventAccessReviewsResourceWithStreamingResponse,
    AsyncEventAccessReviewsResourceWithStreamingResponse,
)
from .event_access_requests import (
    EventAccessRequestsResource,
    AsyncEventAccessRequestsResource,
    EventAccessRequestsResourceWithRawResponse,
    AsyncEventAccessRequestsResourceWithRawResponse,
    EventAccessRequestsResourceWithStreamingResponse,
    AsyncEventAccessRequestsResourceWithStreamingResponse,
)
from .custom_attribute_definitions import (
    CustomAttributeDefinitionsResource,
    AsyncCustomAttributeDefinitionsResource,
    CustomAttributeDefinitionsResourceWithRawResponse,
    AsyncCustomAttributeDefinitionsResourceWithRawResponse,
    CustomAttributeDefinitionsResourceWithStreamingResponse,
    AsyncCustomAttributeDefinitionsResourceWithStreamingResponse,
)
from .change_application_domain_operations import (
    ChangeApplicationDomainOperationsResource,
    AsyncChangeApplicationDomainOperationsResource,
    ChangeApplicationDomainOperationsResourceWithRawResponse,
    AsyncChangeApplicationDomainOperationsResourceWithRawResponse,
    ChangeApplicationDomainOperationsResourceWithStreamingResponse,
    AsyncChangeApplicationDomainOperationsResourceWithStreamingResponse,
)
from .event_api_versions.event_api_versions import (
    EventAPIVersionsResource,
    AsyncEventAPIVersionsResource,
    EventAPIVersionsResourceWithRawResponse,
    AsyncEventAPIVersionsResourceWithRawResponse,
    EventAPIVersionsResourceWithStreamingResponse,
    AsyncEventAPIVersionsResourceWithStreamingResponse,
)
from .application_domains.application_domains import (
    ApplicationDomainsResource,
    AsyncApplicationDomainsResource,
    ApplicationDomainsResourceWithRawResponse,
    AsyncApplicationDomainsResourceWithRawResponse,
    ApplicationDomainsResourceWithStreamingResponse,
    AsyncApplicationDomainsResourceWithStreamingResponse,
)
from .application_versions.application_versions import (
    ApplicationVersionsResource,
    AsyncApplicationVersionsResource,
    ApplicationVersionsResourceWithRawResponse,
    AsyncApplicationVersionsResourceWithRawResponse,
    ApplicationVersionsResourceWithStreamingResponse,
    AsyncApplicationVersionsResourceWithStreamingResponse,
)
from .configuration_template.configuration_template import (
    ConfigurationTemplateResource,
    AsyncConfigurationTemplateResource,
    ConfigurationTemplateResourceWithRawResponse,
    AsyncConfigurationTemplateResourceWithRawResponse,
    ConfigurationTemplateResourceWithStreamingResponse,
    AsyncConfigurationTemplateResourceWithStreamingResponse,
)
from .....types.api.v2.architecture_get_states_response import ArchitectureGetStatesResponse
from .event_api_product_versions.event_api_product_versions import (
    EventAPIProductVersionsResource,
    AsyncEventAPIProductVersionsResource,
    EventAPIProductVersionsResourceWithRawResponse,
    AsyncEventAPIProductVersionsResourceWithRawResponse,
    EventAPIProductVersionsResourceWithStreamingResponse,
    AsyncEventAPIProductVersionsResourceWithStreamingResponse,
)
from .....types.api.v2.architecture_get_event_portal_usage_stats_response import (
    ArchitectureGetEventPortalUsageStatsResponse,
)

__all__ = ["ArchitectureResource", "AsyncArchitectureResource"]


class ArchitectureResource(SyncAPIResource):
    @cached_property
    def change_application_domain_operations(self) -> ChangeApplicationDomainOperationsResource:
        return ChangeApplicationDomainOperationsResource(self._client)

    @cached_property
    def application_domains(self) -> ApplicationDomainsResource:
        return ApplicationDomainsResource(self._client)

    @cached_property
    def application_versions(self) -> ApplicationVersionsResource:
        return ApplicationVersionsResource(self._client)

    @cached_property
    def about(self) -> AboutResource:
        return AboutResource(self._client)

    @cached_property
    def applications(self) -> ApplicationsResource:
        return ApplicationsResource(self._client)

    @cached_property
    def configuration_template(self) -> ConfigurationTemplateResource:
        return ConfigurationTemplateResource(self._client)

    @cached_property
    def configuration_types(self) -> ConfigurationTypesResource:
        return ConfigurationTypesResource(self._client)

    @cached_property
    def consumers(self) -> ConsumersResource:
        return ConsumersResource(self._client)

    @cached_property
    def custom_attribute_definitions(self) -> CustomAttributeDefinitionsResource:
        return CustomAttributeDefinitionsResource(self._client)

    @cached_property
    def designer(self) -> DesignerResource:
        return DesignerResource(self._client)

    @cached_property
    def enum_versions(self) -> EnumVersionsResource:
        return EnumVersionsResource(self._client)

    @cached_property
    def enums(self) -> EnumsResource:
        return EnumsResource(self._client)

    @cached_property
    def event_api_product_versions(self) -> EventAPIProductVersionsResource:
        return EventAPIProductVersionsResource(self._client)

    @cached_property
    def event_api_products(self) -> EventAPIProductsResource:
        return EventAPIProductsResource(self._client)

    @cached_property
    def event_api_versions(self) -> EventAPIVersionsResource:
        return EventAPIVersionsResource(self._client)

    @cached_property
    def event_apis(self) -> EventAPIsResource:
        return EventAPIsResource(self._client)

    @cached_property
    def event_access_requests(self) -> EventAccessRequestsResource:
        return EventAccessRequestsResource(self._client)

    @cached_property
    def event_access_reviews(self) -> EventAccessReviewsResource:
        return EventAccessReviewsResource(self._client)

    @cached_property
    def event_versions(self) -> EventVersionsResource:
        return EventVersionsResource(self._client)

    @cached_property
    def events(self) -> EventsResource:
        return EventsResource(self._client)

    @cached_property
    def schema_versions(self) -> SchemaVersionsResource:
        return SchemaVersionsResource(self._client)

    @cached_property
    def schemas(self) -> SchemasResource:
        return SchemasResource(self._client)

    @cached_property
    def topic_domains(self) -> TopicDomainsResource:
        return TopicDomainsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ArchitectureResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return ArchitectureResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ArchitectureResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return ArchitectureResourceWithStreamingResponse(self)

    def delete_event_api_product_mem_association(
        self,
        mem_association_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Use this API to disassociate an Event API Product version and gateway messaging
        service by association ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not mem_association_id:
            raise ValueError(f"Expected a non-empty value for `mem_association_id` but received {mem_association_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v2/architecture/eventApiProductMemAssociations/{mem_association_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def get_event_portal_usage_stats(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArchitectureGetEventPortalUsageStatsResponse:
        """
        Use this API to get event portal usage stats

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            "/api/v2/architecture/eventPortalUsageStats",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArchitectureGetEventPortalUsageStatsResponse,
        )

    def get_states(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArchitectureGetStatesResponse:
        """
        Use this API to get a list of lifecycle states that match the given parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            "/api/v2/architecture/states",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArchitectureGetStatesResponse,
        )


class AsyncArchitectureResource(AsyncAPIResource):
    @cached_property
    def change_application_domain_operations(self) -> AsyncChangeApplicationDomainOperationsResource:
        return AsyncChangeApplicationDomainOperationsResource(self._client)

    @cached_property
    def application_domains(self) -> AsyncApplicationDomainsResource:
        return AsyncApplicationDomainsResource(self._client)

    @cached_property
    def application_versions(self) -> AsyncApplicationVersionsResource:
        return AsyncApplicationVersionsResource(self._client)

    @cached_property
    def about(self) -> AsyncAboutResource:
        return AsyncAboutResource(self._client)

    @cached_property
    def applications(self) -> AsyncApplicationsResource:
        return AsyncApplicationsResource(self._client)

    @cached_property
    def configuration_template(self) -> AsyncConfigurationTemplateResource:
        return AsyncConfigurationTemplateResource(self._client)

    @cached_property
    def configuration_types(self) -> AsyncConfigurationTypesResource:
        return AsyncConfigurationTypesResource(self._client)

    @cached_property
    def consumers(self) -> AsyncConsumersResource:
        return AsyncConsumersResource(self._client)

    @cached_property
    def custom_attribute_definitions(self) -> AsyncCustomAttributeDefinitionsResource:
        return AsyncCustomAttributeDefinitionsResource(self._client)

    @cached_property
    def designer(self) -> AsyncDesignerResource:
        return AsyncDesignerResource(self._client)

    @cached_property
    def enum_versions(self) -> AsyncEnumVersionsResource:
        return AsyncEnumVersionsResource(self._client)

    @cached_property
    def enums(self) -> AsyncEnumsResource:
        return AsyncEnumsResource(self._client)

    @cached_property
    def event_api_product_versions(self) -> AsyncEventAPIProductVersionsResource:
        return AsyncEventAPIProductVersionsResource(self._client)

    @cached_property
    def event_api_products(self) -> AsyncEventAPIProductsResource:
        return AsyncEventAPIProductsResource(self._client)

    @cached_property
    def event_api_versions(self) -> AsyncEventAPIVersionsResource:
        return AsyncEventAPIVersionsResource(self._client)

    @cached_property
    def event_apis(self) -> AsyncEventAPIsResource:
        return AsyncEventAPIsResource(self._client)

    @cached_property
    def event_access_requests(self) -> AsyncEventAccessRequestsResource:
        return AsyncEventAccessRequestsResource(self._client)

    @cached_property
    def event_access_reviews(self) -> AsyncEventAccessReviewsResource:
        return AsyncEventAccessReviewsResource(self._client)

    @cached_property
    def event_versions(self) -> AsyncEventVersionsResource:
        return AsyncEventVersionsResource(self._client)

    @cached_property
    def events(self) -> AsyncEventsResource:
        return AsyncEventsResource(self._client)

    @cached_property
    def schema_versions(self) -> AsyncSchemaVersionsResource:
        return AsyncSchemaVersionsResource(self._client)

    @cached_property
    def schemas(self) -> AsyncSchemasResource:
        return AsyncSchemasResource(self._client)

    @cached_property
    def topic_domains(self) -> AsyncTopicDomainsResource:
        return AsyncTopicDomainsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncArchitectureResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncArchitectureResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncArchitectureResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncArchitectureResourceWithStreamingResponse(self)

    async def delete_event_api_product_mem_association(
        self,
        mem_association_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Use this API to disassociate an Event API Product version and gateway messaging
        service by association ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not mem_association_id:
            raise ValueError(f"Expected a non-empty value for `mem_association_id` but received {mem_association_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v2/architecture/eventApiProductMemAssociations/{mem_association_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def get_event_portal_usage_stats(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArchitectureGetEventPortalUsageStatsResponse:
        """
        Use this API to get event portal usage stats

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            "/api/v2/architecture/eventPortalUsageStats",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArchitectureGetEventPortalUsageStatsResponse,
        )

    async def get_states(
        self,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ArchitectureGetStatesResponse:
        """
        Use this API to get a list of lifecycle states that match the given parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            "/api/v2/architecture/states",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ArchitectureGetStatesResponse,
        )


class ArchitectureResourceWithRawResponse:
    def __init__(self, architecture: ArchitectureResource) -> None:
        self._architecture = architecture

        self.delete_event_api_product_mem_association = to_raw_response_wrapper(
            architecture.delete_event_api_product_mem_association,
        )
        self.get_event_portal_usage_stats = to_raw_response_wrapper(
            architecture.get_event_portal_usage_stats,
        )
        self.get_states = to_raw_response_wrapper(
            architecture.get_states,
        )

    @cached_property
    def change_application_domain_operations(self) -> ChangeApplicationDomainOperationsResourceWithRawResponse:
        return ChangeApplicationDomainOperationsResourceWithRawResponse(
            self._architecture.change_application_domain_operations
        )

    @cached_property
    def application_domains(self) -> ApplicationDomainsResourceWithRawResponse:
        return ApplicationDomainsResourceWithRawResponse(self._architecture.application_domains)

    @cached_property
    def application_versions(self) -> ApplicationVersionsResourceWithRawResponse:
        return ApplicationVersionsResourceWithRawResponse(self._architecture.application_versions)

    @cached_property
    def about(self) -> AboutResourceWithRawResponse:
        return AboutResourceWithRawResponse(self._architecture.about)

    @cached_property
    def applications(self) -> ApplicationsResourceWithRawResponse:
        return ApplicationsResourceWithRawResponse(self._architecture.applications)

    @cached_property
    def configuration_template(self) -> ConfigurationTemplateResourceWithRawResponse:
        return ConfigurationTemplateResourceWithRawResponse(self._architecture.configuration_template)

    @cached_property
    def configuration_types(self) -> ConfigurationTypesResourceWithRawResponse:
        return ConfigurationTypesResourceWithRawResponse(self._architecture.configuration_types)

    @cached_property
    def consumers(self) -> ConsumersResourceWithRawResponse:
        return ConsumersResourceWithRawResponse(self._architecture.consumers)

    @cached_property
    def custom_attribute_definitions(self) -> CustomAttributeDefinitionsResourceWithRawResponse:
        return CustomAttributeDefinitionsResourceWithRawResponse(self._architecture.custom_attribute_definitions)

    @cached_property
    def designer(self) -> DesignerResourceWithRawResponse:
        return DesignerResourceWithRawResponse(self._architecture.designer)

    @cached_property
    def enum_versions(self) -> EnumVersionsResourceWithRawResponse:
        return EnumVersionsResourceWithRawResponse(self._architecture.enum_versions)

    @cached_property
    def enums(self) -> EnumsResourceWithRawResponse:
        return EnumsResourceWithRawResponse(self._architecture.enums)

    @cached_property
    def event_api_product_versions(self) -> EventAPIProductVersionsResourceWithRawResponse:
        return EventAPIProductVersionsResourceWithRawResponse(self._architecture.event_api_product_versions)

    @cached_property
    def event_api_products(self) -> EventAPIProductsResourceWithRawResponse:
        return EventAPIProductsResourceWithRawResponse(self._architecture.event_api_products)

    @cached_property
    def event_api_versions(self) -> EventAPIVersionsResourceWithRawResponse:
        return EventAPIVersionsResourceWithRawResponse(self._architecture.event_api_versions)

    @cached_property
    def event_apis(self) -> EventAPIsResourceWithRawResponse:
        return EventAPIsResourceWithRawResponse(self._architecture.event_apis)

    @cached_property
    def event_access_requests(self) -> EventAccessRequestsResourceWithRawResponse:
        return EventAccessRequestsResourceWithRawResponse(self._architecture.event_access_requests)

    @cached_property
    def event_access_reviews(self) -> EventAccessReviewsResourceWithRawResponse:
        return EventAccessReviewsResourceWithRawResponse(self._architecture.event_access_reviews)

    @cached_property
    def event_versions(self) -> EventVersionsResourceWithRawResponse:
        return EventVersionsResourceWithRawResponse(self._architecture.event_versions)

    @cached_property
    def events(self) -> EventsResourceWithRawResponse:
        return EventsResourceWithRawResponse(self._architecture.events)

    @cached_property
    def schema_versions(self) -> SchemaVersionsResourceWithRawResponse:
        return SchemaVersionsResourceWithRawResponse(self._architecture.schema_versions)

    @cached_property
    def schemas(self) -> SchemasResourceWithRawResponse:
        return SchemasResourceWithRawResponse(self._architecture.schemas)

    @cached_property
    def topic_domains(self) -> TopicDomainsResourceWithRawResponse:
        return TopicDomainsResourceWithRawResponse(self._architecture.topic_domains)


class AsyncArchitectureResourceWithRawResponse:
    def __init__(self, architecture: AsyncArchitectureResource) -> None:
        self._architecture = architecture

        self.delete_event_api_product_mem_association = async_to_raw_response_wrapper(
            architecture.delete_event_api_product_mem_association,
        )
        self.get_event_portal_usage_stats = async_to_raw_response_wrapper(
            architecture.get_event_portal_usage_stats,
        )
        self.get_states = async_to_raw_response_wrapper(
            architecture.get_states,
        )

    @cached_property
    def change_application_domain_operations(self) -> AsyncChangeApplicationDomainOperationsResourceWithRawResponse:
        return AsyncChangeApplicationDomainOperationsResourceWithRawResponse(
            self._architecture.change_application_domain_operations
        )

    @cached_property
    def application_domains(self) -> AsyncApplicationDomainsResourceWithRawResponse:
        return AsyncApplicationDomainsResourceWithRawResponse(self._architecture.application_domains)

    @cached_property
    def application_versions(self) -> AsyncApplicationVersionsResourceWithRawResponse:
        return AsyncApplicationVersionsResourceWithRawResponse(self._architecture.application_versions)

    @cached_property
    def about(self) -> AsyncAboutResourceWithRawResponse:
        return AsyncAboutResourceWithRawResponse(self._architecture.about)

    @cached_property
    def applications(self) -> AsyncApplicationsResourceWithRawResponse:
        return AsyncApplicationsResourceWithRawResponse(self._architecture.applications)

    @cached_property
    def configuration_template(self) -> AsyncConfigurationTemplateResourceWithRawResponse:
        return AsyncConfigurationTemplateResourceWithRawResponse(self._architecture.configuration_template)

    @cached_property
    def configuration_types(self) -> AsyncConfigurationTypesResourceWithRawResponse:
        return AsyncConfigurationTypesResourceWithRawResponse(self._architecture.configuration_types)

    @cached_property
    def consumers(self) -> AsyncConsumersResourceWithRawResponse:
        return AsyncConsumersResourceWithRawResponse(self._architecture.consumers)

    @cached_property
    def custom_attribute_definitions(self) -> AsyncCustomAttributeDefinitionsResourceWithRawResponse:
        return AsyncCustomAttributeDefinitionsResourceWithRawResponse(self._architecture.custom_attribute_definitions)

    @cached_property
    def designer(self) -> AsyncDesignerResourceWithRawResponse:
        return AsyncDesignerResourceWithRawResponse(self._architecture.designer)

    @cached_property
    def enum_versions(self) -> AsyncEnumVersionsResourceWithRawResponse:
        return AsyncEnumVersionsResourceWithRawResponse(self._architecture.enum_versions)

    @cached_property
    def enums(self) -> AsyncEnumsResourceWithRawResponse:
        return AsyncEnumsResourceWithRawResponse(self._architecture.enums)

    @cached_property
    def event_api_product_versions(self) -> AsyncEventAPIProductVersionsResourceWithRawResponse:
        return AsyncEventAPIProductVersionsResourceWithRawResponse(self._architecture.event_api_product_versions)

    @cached_property
    def event_api_products(self) -> AsyncEventAPIProductsResourceWithRawResponse:
        return AsyncEventAPIProductsResourceWithRawResponse(self._architecture.event_api_products)

    @cached_property
    def event_api_versions(self) -> AsyncEventAPIVersionsResourceWithRawResponse:
        return AsyncEventAPIVersionsResourceWithRawResponse(self._architecture.event_api_versions)

    @cached_property
    def event_apis(self) -> AsyncEventAPIsResourceWithRawResponse:
        return AsyncEventAPIsResourceWithRawResponse(self._architecture.event_apis)

    @cached_property
    def event_access_requests(self) -> AsyncEventAccessRequestsResourceWithRawResponse:
        return AsyncEventAccessRequestsResourceWithRawResponse(self._architecture.event_access_requests)

    @cached_property
    def event_access_reviews(self) -> AsyncEventAccessReviewsResourceWithRawResponse:
        return AsyncEventAccessReviewsResourceWithRawResponse(self._architecture.event_access_reviews)

    @cached_property
    def event_versions(self) -> AsyncEventVersionsResourceWithRawResponse:
        return AsyncEventVersionsResourceWithRawResponse(self._architecture.event_versions)

    @cached_property
    def events(self) -> AsyncEventsResourceWithRawResponse:
        return AsyncEventsResourceWithRawResponse(self._architecture.events)

    @cached_property
    def schema_versions(self) -> AsyncSchemaVersionsResourceWithRawResponse:
        return AsyncSchemaVersionsResourceWithRawResponse(self._architecture.schema_versions)

    @cached_property
    def schemas(self) -> AsyncSchemasResourceWithRawResponse:
        return AsyncSchemasResourceWithRawResponse(self._architecture.schemas)

    @cached_property
    def topic_domains(self) -> AsyncTopicDomainsResourceWithRawResponse:
        return AsyncTopicDomainsResourceWithRawResponse(self._architecture.topic_domains)


class ArchitectureResourceWithStreamingResponse:
    def __init__(self, architecture: ArchitectureResource) -> None:
        self._architecture = architecture

        self.delete_event_api_product_mem_association = to_streamed_response_wrapper(
            architecture.delete_event_api_product_mem_association,
        )
        self.get_event_portal_usage_stats = to_streamed_response_wrapper(
            architecture.get_event_portal_usage_stats,
        )
        self.get_states = to_streamed_response_wrapper(
            architecture.get_states,
        )

    @cached_property
    def change_application_domain_operations(self) -> ChangeApplicationDomainOperationsResourceWithStreamingResponse:
        return ChangeApplicationDomainOperationsResourceWithStreamingResponse(
            self._architecture.change_application_domain_operations
        )

    @cached_property
    def application_domains(self) -> ApplicationDomainsResourceWithStreamingResponse:
        return ApplicationDomainsResourceWithStreamingResponse(self._architecture.application_domains)

    @cached_property
    def application_versions(self) -> ApplicationVersionsResourceWithStreamingResponse:
        return ApplicationVersionsResourceWithStreamingResponse(self._architecture.application_versions)

    @cached_property
    def about(self) -> AboutResourceWithStreamingResponse:
        return AboutResourceWithStreamingResponse(self._architecture.about)

    @cached_property
    def applications(self) -> ApplicationsResourceWithStreamingResponse:
        return ApplicationsResourceWithStreamingResponse(self._architecture.applications)

    @cached_property
    def configuration_template(self) -> ConfigurationTemplateResourceWithStreamingResponse:
        return ConfigurationTemplateResourceWithStreamingResponse(self._architecture.configuration_template)

    @cached_property
    def configuration_types(self) -> ConfigurationTypesResourceWithStreamingResponse:
        return ConfigurationTypesResourceWithStreamingResponse(self._architecture.configuration_types)

    @cached_property
    def consumers(self) -> ConsumersResourceWithStreamingResponse:
        return ConsumersResourceWithStreamingResponse(self._architecture.consumers)

    @cached_property
    def custom_attribute_definitions(self) -> CustomAttributeDefinitionsResourceWithStreamingResponse:
        return CustomAttributeDefinitionsResourceWithStreamingResponse(self._architecture.custom_attribute_definitions)

    @cached_property
    def designer(self) -> DesignerResourceWithStreamingResponse:
        return DesignerResourceWithStreamingResponse(self._architecture.designer)

    @cached_property
    def enum_versions(self) -> EnumVersionsResourceWithStreamingResponse:
        return EnumVersionsResourceWithStreamingResponse(self._architecture.enum_versions)

    @cached_property
    def enums(self) -> EnumsResourceWithStreamingResponse:
        return EnumsResourceWithStreamingResponse(self._architecture.enums)

    @cached_property
    def event_api_product_versions(self) -> EventAPIProductVersionsResourceWithStreamingResponse:
        return EventAPIProductVersionsResourceWithStreamingResponse(self._architecture.event_api_product_versions)

    @cached_property
    def event_api_products(self) -> EventAPIProductsResourceWithStreamingResponse:
        return EventAPIProductsResourceWithStreamingResponse(self._architecture.event_api_products)

    @cached_property
    def event_api_versions(self) -> EventAPIVersionsResourceWithStreamingResponse:
        return EventAPIVersionsResourceWithStreamingResponse(self._architecture.event_api_versions)

    @cached_property
    def event_apis(self) -> EventAPIsResourceWithStreamingResponse:
        return EventAPIsResourceWithStreamingResponse(self._architecture.event_apis)

    @cached_property
    def event_access_requests(self) -> EventAccessRequestsResourceWithStreamingResponse:
        return EventAccessRequestsResourceWithStreamingResponse(self._architecture.event_access_requests)

    @cached_property
    def event_access_reviews(self) -> EventAccessReviewsResourceWithStreamingResponse:
        return EventAccessReviewsResourceWithStreamingResponse(self._architecture.event_access_reviews)

    @cached_property
    def event_versions(self) -> EventVersionsResourceWithStreamingResponse:
        return EventVersionsResourceWithStreamingResponse(self._architecture.event_versions)

    @cached_property
    def events(self) -> EventsResourceWithStreamingResponse:
        return EventsResourceWithStreamingResponse(self._architecture.events)

    @cached_property
    def schema_versions(self) -> SchemaVersionsResourceWithStreamingResponse:
        return SchemaVersionsResourceWithStreamingResponse(self._architecture.schema_versions)

    @cached_property
    def schemas(self) -> SchemasResourceWithStreamingResponse:
        return SchemasResourceWithStreamingResponse(self._architecture.schemas)

    @cached_property
    def topic_domains(self) -> TopicDomainsResourceWithStreamingResponse:
        return TopicDomainsResourceWithStreamingResponse(self._architecture.topic_domains)


class AsyncArchitectureResourceWithStreamingResponse:
    def __init__(self, architecture: AsyncArchitectureResource) -> None:
        self._architecture = architecture

        self.delete_event_api_product_mem_association = async_to_streamed_response_wrapper(
            architecture.delete_event_api_product_mem_association,
        )
        self.get_event_portal_usage_stats = async_to_streamed_response_wrapper(
            architecture.get_event_portal_usage_stats,
        )
        self.get_states = async_to_streamed_response_wrapper(
            architecture.get_states,
        )

    @cached_property
    def change_application_domain_operations(
        self,
    ) -> AsyncChangeApplicationDomainOperationsResourceWithStreamingResponse:
        return AsyncChangeApplicationDomainOperationsResourceWithStreamingResponse(
            self._architecture.change_application_domain_operations
        )

    @cached_property
    def application_domains(self) -> AsyncApplicationDomainsResourceWithStreamingResponse:
        return AsyncApplicationDomainsResourceWithStreamingResponse(self._architecture.application_domains)

    @cached_property
    def application_versions(self) -> AsyncApplicationVersionsResourceWithStreamingResponse:
        return AsyncApplicationVersionsResourceWithStreamingResponse(self._architecture.application_versions)

    @cached_property
    def about(self) -> AsyncAboutResourceWithStreamingResponse:
        return AsyncAboutResourceWithStreamingResponse(self._architecture.about)

    @cached_property
    def applications(self) -> AsyncApplicationsResourceWithStreamingResponse:
        return AsyncApplicationsResourceWithStreamingResponse(self._architecture.applications)

    @cached_property
    def configuration_template(self) -> AsyncConfigurationTemplateResourceWithStreamingResponse:
        return AsyncConfigurationTemplateResourceWithStreamingResponse(self._architecture.configuration_template)

    @cached_property
    def configuration_types(self) -> AsyncConfigurationTypesResourceWithStreamingResponse:
        return AsyncConfigurationTypesResourceWithStreamingResponse(self._architecture.configuration_types)

    @cached_property
    def consumers(self) -> AsyncConsumersResourceWithStreamingResponse:
        return AsyncConsumersResourceWithStreamingResponse(self._architecture.consumers)

    @cached_property
    def custom_attribute_definitions(self) -> AsyncCustomAttributeDefinitionsResourceWithStreamingResponse:
        return AsyncCustomAttributeDefinitionsResourceWithStreamingResponse(
            self._architecture.custom_attribute_definitions
        )

    @cached_property
    def designer(self) -> AsyncDesignerResourceWithStreamingResponse:
        return AsyncDesignerResourceWithStreamingResponse(self._architecture.designer)

    @cached_property
    def enum_versions(self) -> AsyncEnumVersionsResourceWithStreamingResponse:
        return AsyncEnumVersionsResourceWithStreamingResponse(self._architecture.enum_versions)

    @cached_property
    def enums(self) -> AsyncEnumsResourceWithStreamingResponse:
        return AsyncEnumsResourceWithStreamingResponse(self._architecture.enums)

    @cached_property
    def event_api_product_versions(self) -> AsyncEventAPIProductVersionsResourceWithStreamingResponse:
        return AsyncEventAPIProductVersionsResourceWithStreamingResponse(self._architecture.event_api_product_versions)

    @cached_property
    def event_api_products(self) -> AsyncEventAPIProductsResourceWithStreamingResponse:
        return AsyncEventAPIProductsResourceWithStreamingResponse(self._architecture.event_api_products)

    @cached_property
    def event_api_versions(self) -> AsyncEventAPIVersionsResourceWithStreamingResponse:
        return AsyncEventAPIVersionsResourceWithStreamingResponse(self._architecture.event_api_versions)

    @cached_property
    def event_apis(self) -> AsyncEventAPIsResourceWithStreamingResponse:
        return AsyncEventAPIsResourceWithStreamingResponse(self._architecture.event_apis)

    @cached_property
    def event_access_requests(self) -> AsyncEventAccessRequestsResourceWithStreamingResponse:
        return AsyncEventAccessRequestsResourceWithStreamingResponse(self._architecture.event_access_requests)

    @cached_property
    def event_access_reviews(self) -> AsyncEventAccessReviewsResourceWithStreamingResponse:
        return AsyncEventAccessReviewsResourceWithStreamingResponse(self._architecture.event_access_reviews)

    @cached_property
    def event_versions(self) -> AsyncEventVersionsResourceWithStreamingResponse:
        return AsyncEventVersionsResourceWithStreamingResponse(self._architecture.event_versions)

    @cached_property
    def events(self) -> AsyncEventsResourceWithStreamingResponse:
        return AsyncEventsResourceWithStreamingResponse(self._architecture.events)

    @cached_property
    def schema_versions(self) -> AsyncSchemaVersionsResourceWithStreamingResponse:
        return AsyncSchemaVersionsResourceWithStreamingResponse(self._architecture.schema_versions)

    @cached_property
    def schemas(self) -> AsyncSchemasResourceWithStreamingResponse:
        return AsyncSchemasResourceWithStreamingResponse(self._architecture.schemas)

    @cached_property
    def topic_domains(self) -> AsyncTopicDomainsResourceWithStreamingResponse:
        return AsyncTopicDomainsResourceWithStreamingResponse(self._architecture.topic_domains)
