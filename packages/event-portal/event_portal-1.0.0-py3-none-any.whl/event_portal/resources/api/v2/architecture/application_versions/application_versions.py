# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

from .exports import (
    ExportsResource,
    AsyncExportsResource,
    ExportsResourceWithRawResponse,
    AsyncExportsResourceWithRawResponse,
    ExportsResourceWithStreamingResponse,
    AsyncExportsResourceWithStreamingResponse,
)
from ......_types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ......_utils import maybe_transform, async_maybe_transform
from ......_compat import cached_property
from ......_resource import SyncAPIResource, AsyncAPIResource
from ......_response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ......_base_client import make_request_options
from .event_access_requests import (
    EventAccessRequestsResource,
    AsyncEventAccessRequestsResource,
    EventAccessRequestsResourceWithRawResponse,
    AsyncEventAccessRequestsResourceWithRawResponse,
    EventAccessRequestsResourceWithStreamingResponse,
    AsyncEventAccessRequestsResourceWithStreamingResponse,
)
from ......types.api.v2.architecture import (
    application_version_list_params,
    application_version_create_params,
    application_version_update_params,
    application_version_update_state_params,
    application_version_get_async_api_params,
    application_version_replace_messaging_service_params,
)
from ......types.api.v2.architecture.custom_attribute_param import CustomAttributeParam
from ......types.api.v2.architecture.application_version_response import ApplicationVersionResponse
from ......types.api.v2.architecture.state_change_request_response import StateChangeRequestResponse
from ......types.api.v2.architecture.validation_messages_dto_param import ValidationMessagesDtoParam
from ......types.api.v2.architecture.application_version_list_response import ApplicationVersionListResponse
from ......types.api.v2.architecture.messaging_service_association_response import MessagingServiceAssociationResponse
from ......types.api.v2.architecture.application_version_event_access_requests_response import (
    ApplicationVersionEventAccessRequestsResponse,
)

__all__ = ["ApplicationVersionsResource", "AsyncApplicationVersionsResource"]


class ApplicationVersionsResource(SyncAPIResource):
    @cached_property
    def event_access_requests(self) -> EventAccessRequestsResource:
        return EventAccessRequestsResource(self._client)

    @cached_property
    def exports(self) -> ExportsResource:
        return ExportsResource(self._client)

    @cached_property
    def with_raw_response(self) -> ApplicationVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return ApplicationVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ApplicationVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return ApplicationVersionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        application_id: str,
        version: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        declared_consumed_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        declared_event_api_product_version_ids: List[str] | NotGiven = NOT_GIVEN,
        declared_produced_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        validation_messages: ValidationMessagesDtoParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVersionResponse:
        """
        Create an application version

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._post(
            "/api/v2/architecture/applicationVersions",
            body=maybe_transform(
                {
                    "application_id": application_id,
                    "version": version,
                    "custom_attributes": custom_attributes,
                    "declared_consumed_event_version_ids": declared_consumed_event_version_ids,
                    "declared_event_api_product_version_ids": declared_event_api_product_version_ids,
                    "declared_produced_event_version_ids": declared_produced_event_version_ids,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "type": type,
                    "validation_messages": validation_messages,
                },
                application_version_create_params.ApplicationVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationVersionResponse,
        )

    def retrieve(
        self,
        version_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVersionResponse:
        """
        Use this API to get a single application version by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            f"/api/v2/architecture/applicationVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationVersionResponse,
        )

    def update(
        self,
        version_id: str,
        *,
        application_id: str,
        version: str,
        include: List[str] | NotGiven = NOT_GIVEN,
        relations_broker_type: str | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        declared_consumed_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        declared_event_api_product_version_ids: List[str] | NotGiven = NOT_GIVEN,
        declared_produced_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        validation_messages: ValidationMessagesDtoParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVersionResponse:
        """Use this API to update an application version.

        You only need to specify the
        fields that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._patch(
            f"/api/v2/architecture/applicationVersions/{version_id}",
            body=maybe_transform(
                {
                    "application_id": application_id,
                    "version": version,
                    "custom_attributes": custom_attributes,
                    "declared_consumed_event_version_ids": declared_consumed_event_version_ids,
                    "declared_event_api_product_version_ids": declared_event_api_product_version_ids,
                    "declared_produced_event_version_ids": declared_produced_event_version_ids,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "type": type,
                    "validation_messages": validation_messages,
                },
                application_version_update_params.ApplicationVersionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "include": include,
                        "relations_broker_type": relations_broker_type,
                    },
                    application_version_update_params.ApplicationVersionUpdateParams,
                ),
            ),
            cast_to=ApplicationVersionResponse,
        )

    def list(
        self,
        *,
        application_ids: List[str] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        messaging_service_ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        state_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVersionListResponse:
        """
        Use this API to get a list of application versions that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_ids: Match only application versions of these application IDs, separated by commas.

          ids: Match only application versions with the given IDs, separated by commas.

          messaging_service_ids: Match only application versions with the given messaging service IDs, separated
              by commas.

          page_number: The page number to get.

          page_size: The number of application versions to get per page.

          state_ids: Match only application versions with the given state IDs, separated by commas.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            "/api/v2/architecture/applicationVersions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "application_ids": application_ids,
                        "ids": ids,
                        "messaging_service_ids": messaging_service_ids,
                        "page_number": page_number,
                        "page_size": page_size,
                        "state_ids": state_ids,
                    },
                    application_version_list_params.ApplicationVersionListParams,
                ),
            ),
            cast_to=ApplicationVersionListResponse,
        )

    def delete(
        self,
        version_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Use this API to delete an application version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v2/architecture/applicationVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def get_async_api(
        self,
        application_version_id: str,
        *,
        async_api_version: Literal["2.0.0", "2.2.0", "2.5.0"] | NotGiven = NOT_GIVEN,
        context_id: str | NotGiven = NOT_GIVEN,
        context_type: Literal["eventBroker", "eventMesh"] | NotGiven = NOT_GIVEN,
        environment_options: Literal["include_declared_and_attracted_events", "include_attracted_events_only"]
        | NotGiven = NOT_GIVEN,
        expand: Literal[
            "declaredSubscribedEvents",
            "attractedEvents",
            "servers",
            "serverBindings",
            "declaredSubscribedEventBindings",
            "attractedEventBindings",
        ]
        | NotGiven = NOT_GIVEN,
        format: Literal["json", "yaml"] | NotGiven = NOT_GIVEN,
        included_extensions: Literal["all", "parent", "version", "none"] | NotGiven = NOT_GIVEN,
        messaging_service_id: str | NotGiven = NOT_GIVEN,
        show_versioning: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Use this API to get the AsyncAPI specification for an application version
        annotated with Event Portal metadata. Deprecation Date: 2025-01-20 Removal Date:
        2026-01-20 Reason: Replaced by
        /applicationVersions/{applicationVersionId}/exports/asyncAPI

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:generate_async_api:*` ]

        Args:
          async_api_version: The version of AsyncAPI to use.

          context_id: Applies bindings from subscribed events that are published in this event broker
              or event mesh.

          context_type: The context of which events are attracted from.

          environment_options: Determines whether bindings are applied to declared subscribed events or
              published subscribed events in the event mesh or both.

              Replacement: Use expand instead.

              Reason: The change is to allow for increased flexibility of the API.

              Removal Date: 2025-09-20 18:00:00.000.

          expand: A comma separated list of sections of the asyncapi document to include.

          format: The format in which to get the AsyncAPI specification. Possible values are yaml
              and json.

          included_extensions: The event portal database keys to include for each AsyncAPI object.

          messaging_service_id: Applies bindings from attracted events that are published in this messaging
              service's modeled event mesh.

              Replacement: Use contextId with contextType instead.

              Reason: The change is to allow for increased flexibility of the API.

              Removal Date: 2025-09-20 18:00:00.000.

          show_versioning: Include versions in each AsyncAPI object's name when only one version is present

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_version_id:
            raise ValueError(
                f"Expected a non-empty value for `application_version_id` but received {application_version_id!r}"
            )
        return self._get(
            f"/api/v2/architecture/applicationVersions/{application_version_id}/asyncApi",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "async_api_version": async_api_version,
                        "context_id": context_id,
                        "context_type": context_type,
                        "environment_options": environment_options,
                        "expand": expand,
                        "format": format,
                        "included_extensions": included_extensions,
                        "messaging_service_id": messaging_service_id,
                        "show_versioning": show_versioning,
                    },
                    application_version_get_async_api_params.ApplicationVersionGetAsyncAPIParams,
                ),
            ),
            cast_to=str,
        )

    def get_event_access_request_preview(
        self,
        application_version_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVersionEventAccessRequestsResponse:
        """
        Get expected event access requests by application version id

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_version_id:
            raise ValueError(
                f"Expected a non-empty value for `application_version_id` but received {application_version_id!r}"
            )
        return self._get(
            f"/api/v2/architecture/applicationVersions/{application_version_id}/eventAccessRequestPreview",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationVersionEventAccessRequestsResponse,
        )

    def replace_messaging_service(
        self,
        version_id: str,
        *,
        messaging_service_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MessagingServiceAssociationResponse:
        """
        Use this API to replace the messaging service association for an application
        version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_runtime:write` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._put(
            f"/api/v2/architecture/applicationVersions/{version_id}/messagingServices",
            body=maybe_transform(
                {"messaging_service_ids": messaging_service_ids},
                application_version_replace_messaging_service_params.ApplicationVersionReplaceMessagingServiceParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MessagingServiceAssociationResponse,
        )

    def update_state(
        self,
        version_id: str,
        *,
        state_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StateChangeRequestResponse:
        """Use this API to update the state of an application version.

        You only need to
        specify the target stateId field.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update_state:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._patch(
            f"/api/v2/architecture/applicationVersions/{version_id}/state",
            body=maybe_transform(
                {"state_id": state_id}, application_version_update_state_params.ApplicationVersionUpdateStateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StateChangeRequestResponse,
        )


class AsyncApplicationVersionsResource(AsyncAPIResource):
    @cached_property
    def event_access_requests(self) -> AsyncEventAccessRequestsResource:
        return AsyncEventAccessRequestsResource(self._client)

    @cached_property
    def exports(self) -> AsyncExportsResource:
        return AsyncExportsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncApplicationVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncApplicationVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncApplicationVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncApplicationVersionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        application_id: str,
        version: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        declared_consumed_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        declared_event_api_product_version_ids: List[str] | NotGiven = NOT_GIVEN,
        declared_produced_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        validation_messages: ValidationMessagesDtoParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVersionResponse:
        """
        Create an application version

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._post(
            "/api/v2/architecture/applicationVersions",
            body=await async_maybe_transform(
                {
                    "application_id": application_id,
                    "version": version,
                    "custom_attributes": custom_attributes,
                    "declared_consumed_event_version_ids": declared_consumed_event_version_ids,
                    "declared_event_api_product_version_ids": declared_event_api_product_version_ids,
                    "declared_produced_event_version_ids": declared_produced_event_version_ids,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "type": type,
                    "validation_messages": validation_messages,
                },
                application_version_create_params.ApplicationVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationVersionResponse,
        )

    async def retrieve(
        self,
        version_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVersionResponse:
        """
        Use this API to get a single application version by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            f"/api/v2/architecture/applicationVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationVersionResponse,
        )

    async def update(
        self,
        version_id: str,
        *,
        application_id: str,
        version: str,
        include: List[str] | NotGiven = NOT_GIVEN,
        relations_broker_type: str | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        declared_consumed_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        declared_event_api_product_version_ids: List[str] | NotGiven = NOT_GIVEN,
        declared_produced_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        validation_messages: ValidationMessagesDtoParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVersionResponse:
        """Use this API to update an application version.

        You only need to specify the
        fields that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._patch(
            f"/api/v2/architecture/applicationVersions/{version_id}",
            body=await async_maybe_transform(
                {
                    "application_id": application_id,
                    "version": version,
                    "custom_attributes": custom_attributes,
                    "declared_consumed_event_version_ids": declared_consumed_event_version_ids,
                    "declared_event_api_product_version_ids": declared_event_api_product_version_ids,
                    "declared_produced_event_version_ids": declared_produced_event_version_ids,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "type": type,
                    "validation_messages": validation_messages,
                },
                application_version_update_params.ApplicationVersionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "include": include,
                        "relations_broker_type": relations_broker_type,
                    },
                    application_version_update_params.ApplicationVersionUpdateParams,
                ),
            ),
            cast_to=ApplicationVersionResponse,
        )

    async def list(
        self,
        *,
        application_ids: List[str] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        messaging_service_ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        state_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVersionListResponse:
        """
        Use this API to get a list of application versions that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_ids: Match only application versions of these application IDs, separated by commas.

          ids: Match only application versions with the given IDs, separated by commas.

          messaging_service_ids: Match only application versions with the given messaging service IDs, separated
              by commas.

          page_number: The page number to get.

          page_size: The number of application versions to get per page.

          state_ids: Match only application versions with the given state IDs, separated by commas.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            "/api/v2/architecture/applicationVersions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "application_ids": application_ids,
                        "ids": ids,
                        "messaging_service_ids": messaging_service_ids,
                        "page_number": page_number,
                        "page_size": page_size,
                        "state_ids": state_ids,
                    },
                    application_version_list_params.ApplicationVersionListParams,
                ),
            ),
            cast_to=ApplicationVersionListResponse,
        )

    async def delete(
        self,
        version_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Use this API to delete an application version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v2/architecture/applicationVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def get_async_api(
        self,
        application_version_id: str,
        *,
        async_api_version: Literal["2.0.0", "2.2.0", "2.5.0"] | NotGiven = NOT_GIVEN,
        context_id: str | NotGiven = NOT_GIVEN,
        context_type: Literal["eventBroker", "eventMesh"] | NotGiven = NOT_GIVEN,
        environment_options: Literal["include_declared_and_attracted_events", "include_attracted_events_only"]
        | NotGiven = NOT_GIVEN,
        expand: Literal[
            "declaredSubscribedEvents",
            "attractedEvents",
            "servers",
            "serverBindings",
            "declaredSubscribedEventBindings",
            "attractedEventBindings",
        ]
        | NotGiven = NOT_GIVEN,
        format: Literal["json", "yaml"] | NotGiven = NOT_GIVEN,
        included_extensions: Literal["all", "parent", "version", "none"] | NotGiven = NOT_GIVEN,
        messaging_service_id: str | NotGiven = NOT_GIVEN,
        show_versioning: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Use this API to get the AsyncAPI specification for an application version
        annotated with Event Portal metadata. Deprecation Date: 2025-01-20 Removal Date:
        2026-01-20 Reason: Replaced by
        /applicationVersions/{applicationVersionId}/exports/asyncAPI

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:generate_async_api:*` ]

        Args:
          async_api_version: The version of AsyncAPI to use.

          context_id: Applies bindings from subscribed events that are published in this event broker
              or event mesh.

          context_type: The context of which events are attracted from.

          environment_options: Determines whether bindings are applied to declared subscribed events or
              published subscribed events in the event mesh or both.

              Replacement: Use expand instead.

              Reason: The change is to allow for increased flexibility of the API.

              Removal Date: 2025-09-20 18:00:00.000.

          expand: A comma separated list of sections of the asyncapi document to include.

          format: The format in which to get the AsyncAPI specification. Possible values are yaml
              and json.

          included_extensions: The event portal database keys to include for each AsyncAPI object.

          messaging_service_id: Applies bindings from attracted events that are published in this messaging
              service's modeled event mesh.

              Replacement: Use contextId with contextType instead.

              Reason: The change is to allow for increased flexibility of the API.

              Removal Date: 2025-09-20 18:00:00.000.

          show_versioning: Include versions in each AsyncAPI object's name when only one version is present

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_version_id:
            raise ValueError(
                f"Expected a non-empty value for `application_version_id` but received {application_version_id!r}"
            )
        return await self._get(
            f"/api/v2/architecture/applicationVersions/{application_version_id}/asyncApi",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "async_api_version": async_api_version,
                        "context_id": context_id,
                        "context_type": context_type,
                        "environment_options": environment_options,
                        "expand": expand,
                        "format": format,
                        "included_extensions": included_extensions,
                        "messaging_service_id": messaging_service_id,
                        "show_versioning": show_versioning,
                    },
                    application_version_get_async_api_params.ApplicationVersionGetAsyncAPIParams,
                ),
            ),
            cast_to=str,
        )

    async def get_event_access_request_preview(
        self,
        application_version_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVersionEventAccessRequestsResponse:
        """
        Get expected event access requests by application version id

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_version_id:
            raise ValueError(
                f"Expected a non-empty value for `application_version_id` but received {application_version_id!r}"
            )
        return await self._get(
            f"/api/v2/architecture/applicationVersions/{application_version_id}/eventAccessRequestPreview",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ApplicationVersionEventAccessRequestsResponse,
        )

    async def replace_messaging_service(
        self,
        version_id: str,
        *,
        messaging_service_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MessagingServiceAssociationResponse:
        """
        Use this API to replace the messaging service association for an application
        version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_runtime:write` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._put(
            f"/api/v2/architecture/applicationVersions/{version_id}/messagingServices",
            body=await async_maybe_transform(
                {"messaging_service_ids": messaging_service_ids},
                application_version_replace_messaging_service_params.ApplicationVersionReplaceMessagingServiceParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MessagingServiceAssociationResponse,
        )

    async def update_state(
        self,
        version_id: str,
        *,
        state_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StateChangeRequestResponse:
        """Use this API to update the state of an application version.

        You only need to
        specify the target stateId field.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update_state:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._patch(
            f"/api/v2/architecture/applicationVersions/{version_id}/state",
            body=await async_maybe_transform(
                {"state_id": state_id}, application_version_update_state_params.ApplicationVersionUpdateStateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StateChangeRequestResponse,
        )


class ApplicationVersionsResourceWithRawResponse:
    def __init__(self, application_versions: ApplicationVersionsResource) -> None:
        self._application_versions = application_versions

        self.create = to_raw_response_wrapper(
            application_versions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            application_versions.retrieve,
        )
        self.update = to_raw_response_wrapper(
            application_versions.update,
        )
        self.list = to_raw_response_wrapper(
            application_versions.list,
        )
        self.delete = to_raw_response_wrapper(
            application_versions.delete,
        )
        self.get_async_api = to_raw_response_wrapper(
            application_versions.get_async_api,
        )
        self.get_event_access_request_preview = to_raw_response_wrapper(
            application_versions.get_event_access_request_preview,
        )
        self.replace_messaging_service = to_raw_response_wrapper(
            application_versions.replace_messaging_service,
        )
        self.update_state = to_raw_response_wrapper(
            application_versions.update_state,
        )

    @cached_property
    def event_access_requests(self) -> EventAccessRequestsResourceWithRawResponse:
        return EventAccessRequestsResourceWithRawResponse(self._application_versions.event_access_requests)

    @cached_property
    def exports(self) -> ExportsResourceWithRawResponse:
        return ExportsResourceWithRawResponse(self._application_versions.exports)


class AsyncApplicationVersionsResourceWithRawResponse:
    def __init__(self, application_versions: AsyncApplicationVersionsResource) -> None:
        self._application_versions = application_versions

        self.create = async_to_raw_response_wrapper(
            application_versions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            application_versions.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            application_versions.update,
        )
        self.list = async_to_raw_response_wrapper(
            application_versions.list,
        )
        self.delete = async_to_raw_response_wrapper(
            application_versions.delete,
        )
        self.get_async_api = async_to_raw_response_wrapper(
            application_versions.get_async_api,
        )
        self.get_event_access_request_preview = async_to_raw_response_wrapper(
            application_versions.get_event_access_request_preview,
        )
        self.replace_messaging_service = async_to_raw_response_wrapper(
            application_versions.replace_messaging_service,
        )
        self.update_state = async_to_raw_response_wrapper(
            application_versions.update_state,
        )

    @cached_property
    def event_access_requests(self) -> AsyncEventAccessRequestsResourceWithRawResponse:
        return AsyncEventAccessRequestsResourceWithRawResponse(self._application_versions.event_access_requests)

    @cached_property
    def exports(self) -> AsyncExportsResourceWithRawResponse:
        return AsyncExportsResourceWithRawResponse(self._application_versions.exports)


class ApplicationVersionsResourceWithStreamingResponse:
    def __init__(self, application_versions: ApplicationVersionsResource) -> None:
        self._application_versions = application_versions

        self.create = to_streamed_response_wrapper(
            application_versions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            application_versions.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            application_versions.update,
        )
        self.list = to_streamed_response_wrapper(
            application_versions.list,
        )
        self.delete = to_streamed_response_wrapper(
            application_versions.delete,
        )
        self.get_async_api = to_streamed_response_wrapper(
            application_versions.get_async_api,
        )
        self.get_event_access_request_preview = to_streamed_response_wrapper(
            application_versions.get_event_access_request_preview,
        )
        self.replace_messaging_service = to_streamed_response_wrapper(
            application_versions.replace_messaging_service,
        )
        self.update_state = to_streamed_response_wrapper(
            application_versions.update_state,
        )

    @cached_property
    def event_access_requests(self) -> EventAccessRequestsResourceWithStreamingResponse:
        return EventAccessRequestsResourceWithStreamingResponse(self._application_versions.event_access_requests)

    @cached_property
    def exports(self) -> ExportsResourceWithStreamingResponse:
        return ExportsResourceWithStreamingResponse(self._application_versions.exports)


class AsyncApplicationVersionsResourceWithStreamingResponse:
    def __init__(self, application_versions: AsyncApplicationVersionsResource) -> None:
        self._application_versions = application_versions

        self.create = async_to_streamed_response_wrapper(
            application_versions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            application_versions.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            application_versions.update,
        )
        self.list = async_to_streamed_response_wrapper(
            application_versions.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            application_versions.delete,
        )
        self.get_async_api = async_to_streamed_response_wrapper(
            application_versions.get_async_api,
        )
        self.get_event_access_request_preview = async_to_streamed_response_wrapper(
            application_versions.get_event_access_request_preview,
        )
        self.replace_messaging_service = async_to_streamed_response_wrapper(
            application_versions.replace_messaging_service,
        )
        self.update_state = async_to_streamed_response_wrapper(
            application_versions.update_state,
        )

    @cached_property
    def event_access_requests(self) -> AsyncEventAccessRequestsResourceWithStreamingResponse:
        return AsyncEventAccessRequestsResourceWithStreamingResponse(self._application_versions.event_access_requests)

    @cached_property
    def exports(self) -> AsyncExportsResourceWithStreamingResponse:
        return AsyncExportsResourceWithStreamingResponse(self._application_versions.exports)
