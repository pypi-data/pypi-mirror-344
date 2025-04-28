# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable

import httpx

from ......_types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ......_utils import maybe_transform, async_maybe_transform
from ......_compat import cached_property
from ......_resource import SyncAPIResource, AsyncAPIResource
from ......_response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    to_custom_raw_response_wrapper,
    async_to_streamed_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ......_base_client import make_request_options
from .custom_attribute_definitions import (
    CustomAttributeDefinitionsResource,
    AsyncCustomAttributeDefinitionsResource,
    CustomAttributeDefinitionsResourceWithRawResponse,
    AsyncCustomAttributeDefinitionsResourceWithRawResponse,
    CustomAttributeDefinitionsResourceWithStreamingResponse,
    AsyncCustomAttributeDefinitionsResourceWithStreamingResponse,
)
from ......types.api.v2.architecture import (
    application_domain_list_params,
    application_domain_create_params,
    application_domain_import_params,
    application_domain_update_params,
    application_domain_retrieve_params,
)
from ......types.api.v2.architecture.event_param import EventParam
from ......types.api.v2.architecture.event_api_param import EventAPIParam
from ......types.api.v2.architecture.application_param import ApplicationParam
from ......types.api.v2.architecture.topic_domain_param import TopicDomainParam
from ......types.api.v2.architecture.event_version_param import EventVersionParam
from ......types.api.v2.architecture.schema_object_param import SchemaObjectParam
from ......types.api.v2.architecture.schema_version_param import SchemaVersionParam
from ......types.api.v2.architecture.custom_attribute_param import CustomAttributeParam
from ......types.api.v2.architecture.event_api_product_param import EventAPIProductParam
from ......types.api.v2.architecture.event_api_version_param import EventAPIVersionParam
from ......types.api.v2.architecture.application_domain_param import ApplicationDomainParam
from ......types.api.v2.architecture.topic_address_enum_param import TopicAddressEnumParam
from ......types.api.v2.architecture.application_version_param import ApplicationVersionParam
from ......types.api.v2.architecture.application_domain_response import ApplicationDomainResponse
from ......types.api.v2.architecture.validation_messages_dto_param import ValidationMessagesDtoParam
from ......types.api.v2.architecture.event_api_product_version_param import EventAPIProductVersionParam
from ......types.api.v2.architecture.application_domain_list_response import ApplicationDomainListResponse
from ......types.api.v2.architecture.topic_address_enum_version_param import TopicAddressEnumVersionParam
from ......types.api.v2.architecture.application_domains.custom_attribute_definition_param import (
    CustomAttributeDefinitionParam,
)

__all__ = ["ApplicationDomainsResource", "AsyncApplicationDomainsResource"]


class ApplicationDomainsResource(SyncAPIResource):
    @cached_property
    def custom_attribute_definitions(self) -> CustomAttributeDefinitionsResource:
        return CustomAttributeDefinitionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ApplicationDomainsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return ApplicationDomainsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ApplicationDomainsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return ApplicationDomainsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        deletion_protected: bool | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        non_draft_descriptions_editable: bool | NotGiven = NOT_GIVEN,
        topic_domain_enforcement_enabled: bool | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        unique_topic_address_enforcement_enabled: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationDomainResponse:
        """
        To help keep your event-driven architecture organized, use application domains
        to create namespaces for your applications, events and schemas.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application_domain:create:*` ]

        Args:
          deletion_protected: If set to true, application domain cannot be deleted until deletion protected is
              disabled.

          non_draft_descriptions_editable: If set to true, descriptions of entities in a non-draft state can be edited.

          topic_domain_enforcement_enabled: Forces all topic addresses within the application domain to be prefixed with one
              of the application domain’s configured topic domains.

          unique_topic_address_enforcement_enabled: Forces all topic addresses within the application domain to be unique.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._post(
            "/api/v2/architecture/applicationDomains",
            body=maybe_transform(
                {
                    "name": name,
                    "custom_attributes": custom_attributes,
                    "deletion_protected": deletion_protected,
                    "description": description,
                    "non_draft_descriptions_editable": non_draft_descriptions_editable,
                    "topic_domain_enforcement_enabled": topic_domain_enforcement_enabled,
                    "type": type,
                    "unique_topic_address_enforcement_enabled": unique_topic_address_enforcement_enabled,
                },
                application_domain_create_params.ApplicationDomainCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationDomainResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        include: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationDomainResponse:
        """
        Use this API to get a single application domain by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application_domain:get:*` ]

        Args:
          include: Specify extra data to be included, options are: stats

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            f"/api/v2/architecture/applicationDomains/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include": include}, application_domain_retrieve_params.ApplicationDomainRetrieveParams
                ),
            ),
            cast_to=ApplicationDomainResponse,
        )

    def update(
        self,
        id: str,
        *,
        name: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        deletion_protected: bool | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        non_draft_descriptions_editable: bool | NotGiven = NOT_GIVEN,
        topic_domain_enforcement_enabled: bool | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        unique_topic_address_enforcement_enabled: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationDomainResponse:
        """Use this API to update an application domain.

        You only need to specify the
        fields that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application_domain:update:*` ]

        Args:
          deletion_protected: If set to true, application domain cannot be deleted until deletion protected is
              disabled.

          non_draft_descriptions_editable: If set to true, descriptions of entities in a non-draft state can be edited.

          topic_domain_enforcement_enabled: Forces all topic addresses within the application domain to be prefixed with one
              of the application domain’s configured topic domains.

          unique_topic_address_enforcement_enabled: Forces all topic addresses within the application domain to be unique.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._patch(
            f"/api/v2/architecture/applicationDomains/{id}",
            body=maybe_transform(
                {
                    "name": name,
                    "custom_attributes": custom_attributes,
                    "deletion_protected": deletion_protected,
                    "description": description,
                    "non_draft_descriptions_editable": non_draft_descriptions_editable,
                    "topic_domain_enforcement_enabled": topic_domain_enforcement_enabled,
                    "type": type,
                    "unique_topic_address_enforcement_enabled": unique_topic_address_enforcement_enabled,
                },
                application_domain_update_params.ApplicationDomainUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationDomainResponse,
        )

    def list(
        self,
        *,
        ids: List[str] | NotGiven = NOT_GIVEN,
        include: List[str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationDomainListResponse:
        """
        Use this API to get a list of application domains that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          ids: Match only application domains with the given IDs separated by commas.

          include: Specify extra data to be included, options are: stats

          name: Name to be used to match the application domain.

          page_number: The page number to get.

          page_size: The number of application domains to get per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/v2/architecture/applicationDomains",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "include": include,
                        "name": name,
                        "page_number": page_number,
                        "page_size": page_size,
                    },
                    application_domain_list_params.ApplicationDomainListParams,
                ),
            ),
            cast_to=ApplicationDomainListResponse,
        )

    def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Use this API to delete an application domain.

        This action also deletes all
        applications, events, and schemas in the application domain. You cannot undo
        this operation.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application_domain:delete:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v2/architecture/applicationDomains/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def export(
        self,
        ids: object,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        Get application domains and their entities and export them as a JSON file that
        can be used to create new application domains in other PubSub+ accounts. This
        API is intended for providing application domain data to other accounts and not
        for data storage or backup. Your token must have one of the permissions listed
        in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application_domain:export:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            f"/api/v2/architecture/applicationDomains/export/{ids}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )

    def import_(
        self,
        *,
        address_spaces: Iterable[application_domain_import_params.AddressSpace] | NotGiven = NOT_GIVEN,
        application_domains: Iterable[ApplicationDomainParam] | NotGiven = NOT_GIVEN,
        applications: Iterable[ApplicationParam] | NotGiven = NOT_GIVEN,
        application_versions: Iterable[ApplicationVersionParam] | NotGiven = NOT_GIVEN,
        custom_attribute_definitions: Iterable[CustomAttributeDefinitionParam] | NotGiven = NOT_GIVEN,
        enums: Iterable[TopicAddressEnumParam] | NotGiven = NOT_GIVEN,
        enum_versions: Iterable[TopicAddressEnumVersionParam] | NotGiven = NOT_GIVEN,
        event_api_products: Iterable[EventAPIProductParam] | NotGiven = NOT_GIVEN,
        event_api_product_versions: Iterable[EventAPIProductVersionParam] | NotGiven = NOT_GIVEN,
        event_apis: Iterable[EventAPIParam] | NotGiven = NOT_GIVEN,
        event_api_versions: Iterable[EventAPIVersionParam] | NotGiven = NOT_GIVEN,
        events: Iterable[EventParam] | NotGiven = NOT_GIVEN,
        event_versions: Iterable[EventVersionParam] | NotGiven = NOT_GIVEN,
        format_version: str | NotGiven = NOT_GIVEN,
        schemas: Iterable[SchemaObjectParam] | NotGiven = NOT_GIVEN,
        schema_versions: Iterable[SchemaVersionParam] | NotGiven = NOT_GIVEN,
        topic_domains: Iterable[TopicDomainParam] | NotGiven = NOT_GIVEN,
        validation_messages: ValidationMessagesDtoParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create new application domains and their nested entities by importing
        application domains that have been previously exported from a PubSub+ account.
        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application_domain:import:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/api/v2/architecture/applicationDomains/import",
            body=maybe_transform(
                {
                    "address_spaces": address_spaces,
                    "application_domains": application_domains,
                    "applications": applications,
                    "application_versions": application_versions,
                    "custom_attribute_definitions": custom_attribute_definitions,
                    "enums": enums,
                    "enum_versions": enum_versions,
                    "event_api_products": event_api_products,
                    "event_api_product_versions": event_api_product_versions,
                    "event_apis": event_apis,
                    "event_api_versions": event_api_versions,
                    "events": events,
                    "event_versions": event_versions,
                    "format_version": format_version,
                    "schemas": schemas,
                    "schema_versions": schema_versions,
                    "topic_domains": topic_domains,
                    "validation_messages": validation_messages,
                },
                application_domain_import_params.ApplicationDomainImportParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncApplicationDomainsResource(AsyncAPIResource):
    @cached_property
    def custom_attribute_definitions(self) -> AsyncCustomAttributeDefinitionsResource:
        return AsyncCustomAttributeDefinitionsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncApplicationDomainsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncApplicationDomainsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncApplicationDomainsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncApplicationDomainsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        deletion_protected: bool | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        non_draft_descriptions_editable: bool | NotGiven = NOT_GIVEN,
        topic_domain_enforcement_enabled: bool | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        unique_topic_address_enforcement_enabled: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationDomainResponse:
        """
        To help keep your event-driven architecture organized, use application domains
        to create namespaces for your applications, events and schemas.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application_domain:create:*` ]

        Args:
          deletion_protected: If set to true, application domain cannot be deleted until deletion protected is
              disabled.

          non_draft_descriptions_editable: If set to true, descriptions of entities in a non-draft state can be edited.

          topic_domain_enforcement_enabled: Forces all topic addresses within the application domain to be prefixed with one
              of the application domain’s configured topic domains.

          unique_topic_address_enforcement_enabled: Forces all topic addresses within the application domain to be unique.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._post(
            "/api/v2/architecture/applicationDomains",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "custom_attributes": custom_attributes,
                    "deletion_protected": deletion_protected,
                    "description": description,
                    "non_draft_descriptions_editable": non_draft_descriptions_editable,
                    "topic_domain_enforcement_enabled": topic_domain_enforcement_enabled,
                    "type": type,
                    "unique_topic_address_enforcement_enabled": unique_topic_address_enforcement_enabled,
                },
                application_domain_create_params.ApplicationDomainCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationDomainResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        include: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationDomainResponse:
        """
        Use this API to get a single application domain by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application_domain:get:*` ]

        Args:
          include: Specify extra data to be included, options are: stats

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            f"/api/v2/architecture/applicationDomains/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include": include}, application_domain_retrieve_params.ApplicationDomainRetrieveParams
                ),
            ),
            cast_to=ApplicationDomainResponse,
        )

    async def update(
        self,
        id: str,
        *,
        name: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        deletion_protected: bool | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        non_draft_descriptions_editable: bool | NotGiven = NOT_GIVEN,
        topic_domain_enforcement_enabled: bool | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        unique_topic_address_enforcement_enabled: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationDomainResponse:
        """Use this API to update an application domain.

        You only need to specify the
        fields that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application_domain:update:*` ]

        Args:
          deletion_protected: If set to true, application domain cannot be deleted until deletion protected is
              disabled.

          non_draft_descriptions_editable: If set to true, descriptions of entities in a non-draft state can be edited.

          topic_domain_enforcement_enabled: Forces all topic addresses within the application domain to be prefixed with one
              of the application domain’s configured topic domains.

          unique_topic_address_enforcement_enabled: Forces all topic addresses within the application domain to be unique.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._patch(
            f"/api/v2/architecture/applicationDomains/{id}",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "custom_attributes": custom_attributes,
                    "deletion_protected": deletion_protected,
                    "description": description,
                    "non_draft_descriptions_editable": non_draft_descriptions_editable,
                    "topic_domain_enforcement_enabled": topic_domain_enforcement_enabled,
                    "type": type,
                    "unique_topic_address_enforcement_enabled": unique_topic_address_enforcement_enabled,
                },
                application_domain_update_params.ApplicationDomainUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationDomainResponse,
        )

    async def list(
        self,
        *,
        ids: List[str] | NotGiven = NOT_GIVEN,
        include: List[str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationDomainListResponse:
        """
        Use this API to get a list of application domains that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          ids: Match only application domains with the given IDs separated by commas.

          include: Specify extra data to be included, options are: stats

          name: Name to be used to match the application domain.

          page_number: The page number to get.

          page_size: The number of application domains to get per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/v2/architecture/applicationDomains",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "include": include,
                        "name": name,
                        "page_number": page_number,
                        "page_size": page_size,
                    },
                    application_domain_list_params.ApplicationDomainListParams,
                ),
            ),
            cast_to=ApplicationDomainListResponse,
        )

    async def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """Use this API to delete an application domain.

        This action also deletes all
        applications, events, and schemas in the application domain. You cannot undo
        this operation.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application_domain:delete:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v2/architecture/applicationDomains/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def export(
        self,
        ids: object,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        Get application domains and their entities and export them as a JSON file that
        can be used to create new application domains in other PubSub+ accounts. This
        API is intended for providing application domain data to other accounts and not
        for data storage or backup. Your token must have one of the permissions listed
        in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application_domain:export:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            f"/api/v2/architecture/applicationDomains/export/{ids}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )

    async def import_(
        self,
        *,
        address_spaces: Iterable[application_domain_import_params.AddressSpace] | NotGiven = NOT_GIVEN,
        application_domains: Iterable[ApplicationDomainParam] | NotGiven = NOT_GIVEN,
        applications: Iterable[ApplicationParam] | NotGiven = NOT_GIVEN,
        application_versions: Iterable[ApplicationVersionParam] | NotGiven = NOT_GIVEN,
        custom_attribute_definitions: Iterable[CustomAttributeDefinitionParam] | NotGiven = NOT_GIVEN,
        enums: Iterable[TopicAddressEnumParam] | NotGiven = NOT_GIVEN,
        enum_versions: Iterable[TopicAddressEnumVersionParam] | NotGiven = NOT_GIVEN,
        event_api_products: Iterable[EventAPIProductParam] | NotGiven = NOT_GIVEN,
        event_api_product_versions: Iterable[EventAPIProductVersionParam] | NotGiven = NOT_GIVEN,
        event_apis: Iterable[EventAPIParam] | NotGiven = NOT_GIVEN,
        event_api_versions: Iterable[EventAPIVersionParam] | NotGiven = NOT_GIVEN,
        events: Iterable[EventParam] | NotGiven = NOT_GIVEN,
        event_versions: Iterable[EventVersionParam] | NotGiven = NOT_GIVEN,
        format_version: str | NotGiven = NOT_GIVEN,
        schemas: Iterable[SchemaObjectParam] | NotGiven = NOT_GIVEN,
        schema_versions: Iterable[SchemaVersionParam] | NotGiven = NOT_GIVEN,
        topic_domains: Iterable[TopicDomainParam] | NotGiven = NOT_GIVEN,
        validation_messages: ValidationMessagesDtoParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Create new application domains and their nested entities by importing
        application domains that have been previously exported from a PubSub+ account.
        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application_domain:import:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/api/v2/architecture/applicationDomains/import",
            body=await async_maybe_transform(
                {
                    "address_spaces": address_spaces,
                    "application_domains": application_domains,
                    "applications": applications,
                    "application_versions": application_versions,
                    "custom_attribute_definitions": custom_attribute_definitions,
                    "enums": enums,
                    "enum_versions": enum_versions,
                    "event_api_products": event_api_products,
                    "event_api_product_versions": event_api_product_versions,
                    "event_apis": event_apis,
                    "event_api_versions": event_api_versions,
                    "events": events,
                    "event_versions": event_versions,
                    "format_version": format_version,
                    "schemas": schemas,
                    "schema_versions": schema_versions,
                    "topic_domains": topic_domains,
                    "validation_messages": validation_messages,
                },
                application_domain_import_params.ApplicationDomainImportParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class ApplicationDomainsResourceWithRawResponse:
    def __init__(self, application_domains: ApplicationDomainsResource) -> None:
        self._application_domains = application_domains

        self.create = to_raw_response_wrapper(
            application_domains.create,
        )
        self.retrieve = to_raw_response_wrapper(
            application_domains.retrieve,
        )
        self.update = to_raw_response_wrapper(
            application_domains.update,
        )
        self.list = to_raw_response_wrapper(
            application_domains.list,
        )
        self.delete = to_raw_response_wrapper(
            application_domains.delete,
        )
        self.export = to_custom_raw_response_wrapper(
            application_domains.export,
            BinaryAPIResponse,
        )
        self.import_ = to_raw_response_wrapper(
            application_domains.import_,
        )

    @cached_property
    def custom_attribute_definitions(self) -> CustomAttributeDefinitionsResourceWithRawResponse:
        return CustomAttributeDefinitionsResourceWithRawResponse(self._application_domains.custom_attribute_definitions)


class AsyncApplicationDomainsResourceWithRawResponse:
    def __init__(self, application_domains: AsyncApplicationDomainsResource) -> None:
        self._application_domains = application_domains

        self.create = async_to_raw_response_wrapper(
            application_domains.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            application_domains.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            application_domains.update,
        )
        self.list = async_to_raw_response_wrapper(
            application_domains.list,
        )
        self.delete = async_to_raw_response_wrapper(
            application_domains.delete,
        )
        self.export = async_to_custom_raw_response_wrapper(
            application_domains.export,
            AsyncBinaryAPIResponse,
        )
        self.import_ = async_to_raw_response_wrapper(
            application_domains.import_,
        )

    @cached_property
    def custom_attribute_definitions(self) -> AsyncCustomAttributeDefinitionsResourceWithRawResponse:
        return AsyncCustomAttributeDefinitionsResourceWithRawResponse(
            self._application_domains.custom_attribute_definitions
        )


class ApplicationDomainsResourceWithStreamingResponse:
    def __init__(self, application_domains: ApplicationDomainsResource) -> None:
        self._application_domains = application_domains

        self.create = to_streamed_response_wrapper(
            application_domains.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            application_domains.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            application_domains.update,
        )
        self.list = to_streamed_response_wrapper(
            application_domains.list,
        )
        self.delete = to_streamed_response_wrapper(
            application_domains.delete,
        )
        self.export = to_custom_streamed_response_wrapper(
            application_domains.export,
            StreamedBinaryAPIResponse,
        )
        self.import_ = to_streamed_response_wrapper(
            application_domains.import_,
        )

    @cached_property
    def custom_attribute_definitions(self) -> CustomAttributeDefinitionsResourceWithStreamingResponse:
        return CustomAttributeDefinitionsResourceWithStreamingResponse(
            self._application_domains.custom_attribute_definitions
        )


class AsyncApplicationDomainsResourceWithStreamingResponse:
    def __init__(self, application_domains: AsyncApplicationDomainsResource) -> None:
        self._application_domains = application_domains

        self.create = async_to_streamed_response_wrapper(
            application_domains.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            application_domains.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            application_domains.update,
        )
        self.list = async_to_streamed_response_wrapper(
            application_domains.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            application_domains.delete,
        )
        self.export = async_to_custom_streamed_response_wrapper(
            application_domains.export,
            AsyncStreamedBinaryAPIResponse,
        )
        self.import_ = async_to_streamed_response_wrapper(
            application_domains.import_,
        )

    @cached_property
    def custom_attribute_definitions(self) -> AsyncCustomAttributeDefinitionsResourceWithStreamingResponse:
        return AsyncCustomAttributeDefinitionsResourceWithStreamingResponse(
            self._application_domains.custom_attribute_definitions
        )
