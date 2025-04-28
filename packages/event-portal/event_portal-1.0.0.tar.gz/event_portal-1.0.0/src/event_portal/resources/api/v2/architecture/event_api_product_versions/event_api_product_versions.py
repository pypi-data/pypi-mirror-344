# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

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
from .mem_associations import (
    MemAssociationsResource,
    AsyncMemAssociationsResource,
    MemAssociationsResourceWithRawResponse,
    AsyncMemAssociationsResourceWithRawResponse,
    MemAssociationsResourceWithStreamingResponse,
    AsyncMemAssociationsResourceWithStreamingResponse,
)
from ......_base_client import make_request_options
from ......types.api.v2.architecture import (
    event_api_product_version_list_params,
    event_api_product_version_create_params,
    event_api_product_version_update_params,
    event_api_product_version_publish_params,
    event_api_product_version_retrieve_params,
    event_api_product_version_update_state_params,
)
from ......types.api.v2.architecture.custom_attribute_param import CustomAttributeParam
from ......types.api.v2.architecture.state_change_request_response import StateChangeRequestResponse
from ......types.api.v2.architecture.event_api_product_version_response import EventAPIProductVersionResponse
from ......types.api.v2.architecture.event_api_product_version_list_response import EventAPIProductVersionListResponse

__all__ = ["EventAPIProductVersionsResource", "AsyncEventAPIProductVersionsResource"]


class EventAPIProductVersionsResource(SyncAPIResource):
    @cached_property
    def mem_associations(self) -> MemAssociationsResource:
        return MemAssociationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> EventAPIProductVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return EventAPIProductVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventAPIProductVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return EventAPIProductVersionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        event_api_product_id: str,
        approval_type: Literal["automatic", "manual"] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        event_api_product_registrations: Iterable[event_api_product_version_create_params.EventAPIProductRegistration]
        | NotGiven = NOT_GIVEN,
        event_api_version_ids: List[str] | NotGiven = NOT_GIVEN,
        filters: Iterable[event_api_product_version_create_params.Filter] | NotGiven = NOT_GIVEN,
        plans: Iterable[event_api_product_version_create_params.Plan] | NotGiven = NOT_GIVEN,
        publish_state: Literal["unset", "published"] | NotGiven = NOT_GIVEN,
        solace_messaging_services: Iterable[event_api_product_version_create_params.SolaceMessagingService]
        | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        summary: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIProductVersionResponse:
        """
        Use this API to create an Event API Product version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update:*` ]

        Args:
          approval_type: Approval type

          event_api_version_ids: List of IDs of associated event API versions

          filters: List of filters that contains eventVersionId name and variables

          publish_state: Publish state

          solace_messaging_services: Solace Messaging Services

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/architecture/eventApiProductVersions",
            body=maybe_transform(
                {
                    "event_api_product_id": event_api_product_id,
                    "approval_type": approval_type,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "event_api_product_registrations": event_api_product_registrations,
                    "event_api_version_ids": event_api_version_ids,
                    "filters": filters,
                    "plans": plans,
                    "publish_state": publish_state,
                    "solace_messaging_services": solace_messaging_services,
                    "state_id": state_id,
                    "summary": summary,
                    "version": version,
                },
                event_api_product_version_create_params.EventAPIProductVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIProductVersionResponse,
        )

    def retrieve(
        self,
        version_id: str,
        *,
        client_app_id: str | NotGiven = NOT_GIVEN,
        include: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIProductVersionResponse:
        """
        Use this API to get a single Event API Product version by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:get:*` ]

        Args:
          client_app_id: Match Event API Product versions with the given clientAppId.

          include: A list of additional entities to include in the response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return self._get(
            f"/api/v2/architecture/eventApiProductVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "client_app_id": client_app_id,
                        "include": include,
                    },
                    event_api_product_version_retrieve_params.EventAPIProductVersionRetrieveParams,
                ),
            ),
            cast_to=EventAPIProductVersionResponse,
        )

    def update(
        self,
        version_id: str,
        *,
        event_api_product_id: str,
        approval_type: Literal["automatic", "manual"] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        event_api_product_registrations: Iterable[event_api_product_version_update_params.EventAPIProductRegistration]
        | NotGiven = NOT_GIVEN,
        event_api_version_ids: List[str] | NotGiven = NOT_GIVEN,
        filters: Iterable[event_api_product_version_update_params.Filter] | NotGiven = NOT_GIVEN,
        plans: Iterable[event_api_product_version_update_params.Plan] | NotGiven = NOT_GIVEN,
        publish_state: Literal["unset", "published"] | NotGiven = NOT_GIVEN,
        solace_messaging_services: Iterable[event_api_product_version_update_params.SolaceMessagingService]
        | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        summary: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIProductVersionResponse:
        """Use this API to update an Event API Product version.

        You only need to specify
        the fields that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update:*` ]

        Args:
          approval_type: Approval type

          event_api_version_ids: List of IDs of associated event API versions

          filters: List of filters that contains eventVersionId name and variables

          publish_state: Publish state

          solace_messaging_services: Solace Messaging Services

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return self._patch(
            f"/api/v2/architecture/eventApiProductVersions/{version_id}",
            body=maybe_transform(
                {
                    "event_api_product_id": event_api_product_id,
                    "approval_type": approval_type,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "event_api_product_registrations": event_api_product_registrations,
                    "event_api_version_ids": event_api_version_ids,
                    "filters": filters,
                    "plans": plans,
                    "publish_state": publish_state,
                    "solace_messaging_services": solace_messaging_services,
                    "state_id": state_id,
                    "summary": summary,
                    "version": version,
                },
                event_api_product_version_update_params.EventAPIProductVersionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIProductVersionResponse,
        )

    def list(
        self,
        *,
        client_app_id: str | NotGiven = NOT_GIVEN,
        custom_attributes: str | NotGiven = NOT_GIVEN,
        event_api_product_ids: List[str] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        include: str | NotGiven = NOT_GIVEN,
        latest: bool | NotGiven = NOT_GIVEN,
        messaging_service_id: str | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIProductVersionListResponse:
        """
        Use this API to get a list of Event API Product versions that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          client_app_id: Match Event API Product versions with the given clientAppId.

          custom_attributes: Returns the entities that match the custom attribute filter. To filter by custom
              attribute name and value, use the format:
              `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
              by custom attribute name, use the format:
              `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
              operator for multiple custom attribute definitions (not multiple values for a
              given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
              operation. Note: the filter supports custom attribute values containing only the
              characters `[a-zA-Z0-9_\\--\\.. ]`.

          event_api_product_ids: Match only Event API Product versions of these Event API Product IDs, separated
              by commas.

          ids: Match Event API Product versions with the given IDs, separated by commas.

          include: A list of additional entities to include in the response.

          latest: Only return the latest version of Event API Products.

          messaging_service_id: Match Event API Product versions with the given messagingServiceId.

          page_number: The page number to get results from based on the page size.

          page_size: The number of results to return in one page of results.

          shared: Match Event API Product versions with the parent objects shared setting.

          state_id: Match Event API Product versions with the given state ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/v2/architecture/eventApiProductVersions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "client_app_id": client_app_id,
                        "custom_attributes": custom_attributes,
                        "event_api_product_ids": event_api_product_ids,
                        "ids": ids,
                        "include": include,
                        "latest": latest,
                        "messaging_service_id": messaging_service_id,
                        "page_number": page_number,
                        "page_size": page_size,
                        "shared": shared,
                        "state_id": state_id,
                    },
                    event_api_product_version_list_params.EventAPIProductVersionListParams,
                ),
            ),
            cast_to=EventAPIProductVersionListResponse,
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
        Use this API to delete an Event API Product version by ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update:*` ]

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
            f"/api/v2/architecture/eventApiProductVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def publish(
        self,
        version_id: str,
        *,
        event_api_product_id: str,
        approval_type: Literal["automatic", "manual"] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        event_api_product_registrations: Iterable[event_api_product_version_publish_params.EventAPIProductRegistration]
        | NotGiven = NOT_GIVEN,
        event_api_version_ids: List[str] | NotGiven = NOT_GIVEN,
        filters: Iterable[event_api_product_version_publish_params.Filter] | NotGiven = NOT_GIVEN,
        plans: Iterable[event_api_product_version_publish_params.Plan] | NotGiven = NOT_GIVEN,
        publish_state: Literal["unset", "published"] | NotGiven = NOT_GIVEN,
        solace_messaging_services: Iterable[event_api_product_version_publish_params.SolaceMessagingService]
        | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        summary: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StateChangeRequestResponse:
        """Use this API to publish Event API Product version.

        Cannot unset once it is
        published.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update_state:*` ]

        Args:
          approval_type: Approval type

          event_api_version_ids: List of IDs of associated event API versions

          filters: List of filters that contains eventVersionId name and variables

          publish_state: Publish state

          solace_messaging_services: Solace Messaging Services

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return self._patch(
            f"/api/v2/architecture/eventApiProductVersions/{version_id}/publish",
            body=maybe_transform(
                {
                    "event_api_product_id": event_api_product_id,
                    "approval_type": approval_type,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "event_api_product_registrations": event_api_product_registrations,
                    "event_api_version_ids": event_api_version_ids,
                    "filters": filters,
                    "plans": plans,
                    "publish_state": publish_state,
                    "solace_messaging_services": solace_messaging_services,
                    "state_id": state_id,
                    "summary": summary,
                    "version": version,
                },
                event_api_product_version_publish_params.EventAPIProductVersionPublishParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StateChangeRequestResponse,
        )

    def update_state(
        self,
        version_id: str,
        *,
        event_api_product_id: str,
        approval_type: Literal["automatic", "manual"] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        event_api_product_registrations: Iterable[
            event_api_product_version_update_state_params.EventAPIProductRegistration
        ]
        | NotGiven = NOT_GIVEN,
        event_api_version_ids: List[str] | NotGiven = NOT_GIVEN,
        filters: Iterable[event_api_product_version_update_state_params.Filter] | NotGiven = NOT_GIVEN,
        plans: Iterable[event_api_product_version_update_state_params.Plan] | NotGiven = NOT_GIVEN,
        publish_state: Literal["unset", "published"] | NotGiven = NOT_GIVEN,
        solace_messaging_services: Iterable[event_api_product_version_update_state_params.SolaceMessagingService]
        | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        summary: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StateChangeRequestResponse:
        """Use this API to update the state of an Event API Product version.

        You only need
        to specify the state ID field with the desired state ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update_state:*` ]

        Args:
          approval_type: Approval type

          event_api_version_ids: List of IDs of associated event API versions

          filters: List of filters that contains eventVersionId name and variables

          publish_state: Publish state

          solace_messaging_services: Solace Messaging Services

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return self._patch(
            f"/api/v2/architecture/eventApiProductVersions/{version_id}/state",
            body=maybe_transform(
                {
                    "event_api_product_id": event_api_product_id,
                    "approval_type": approval_type,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "event_api_product_registrations": event_api_product_registrations,
                    "event_api_version_ids": event_api_version_ids,
                    "filters": filters,
                    "plans": plans,
                    "publish_state": publish_state,
                    "solace_messaging_services": solace_messaging_services,
                    "state_id": state_id,
                    "summary": summary,
                    "version": version,
                },
                event_api_product_version_update_state_params.EventAPIProductVersionUpdateStateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StateChangeRequestResponse,
        )


class AsyncEventAPIProductVersionsResource(AsyncAPIResource):
    @cached_property
    def mem_associations(self) -> AsyncMemAssociationsResource:
        return AsyncMemAssociationsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncEventAPIProductVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEventAPIProductVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventAPIProductVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncEventAPIProductVersionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        event_api_product_id: str,
        approval_type: Literal["automatic", "manual"] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        event_api_product_registrations: Iterable[event_api_product_version_create_params.EventAPIProductRegistration]
        | NotGiven = NOT_GIVEN,
        event_api_version_ids: List[str] | NotGiven = NOT_GIVEN,
        filters: Iterable[event_api_product_version_create_params.Filter] | NotGiven = NOT_GIVEN,
        plans: Iterable[event_api_product_version_create_params.Plan] | NotGiven = NOT_GIVEN,
        publish_state: Literal["unset", "published"] | NotGiven = NOT_GIVEN,
        solace_messaging_services: Iterable[event_api_product_version_create_params.SolaceMessagingService]
        | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        summary: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIProductVersionResponse:
        """
        Use this API to create an Event API Product version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update:*` ]

        Args:
          approval_type: Approval type

          event_api_version_ids: List of IDs of associated event API versions

          filters: List of filters that contains eventVersionId name and variables

          publish_state: Publish state

          solace_messaging_services: Solace Messaging Services

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/architecture/eventApiProductVersions",
            body=await async_maybe_transform(
                {
                    "event_api_product_id": event_api_product_id,
                    "approval_type": approval_type,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "event_api_product_registrations": event_api_product_registrations,
                    "event_api_version_ids": event_api_version_ids,
                    "filters": filters,
                    "plans": plans,
                    "publish_state": publish_state,
                    "solace_messaging_services": solace_messaging_services,
                    "state_id": state_id,
                    "summary": summary,
                    "version": version,
                },
                event_api_product_version_create_params.EventAPIProductVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIProductVersionResponse,
        )

    async def retrieve(
        self,
        version_id: str,
        *,
        client_app_id: str | NotGiven = NOT_GIVEN,
        include: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIProductVersionResponse:
        """
        Use this API to get a single Event API Product version by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:get:*` ]

        Args:
          client_app_id: Match Event API Product versions with the given clientAppId.

          include: A list of additional entities to include in the response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return await self._get(
            f"/api/v2/architecture/eventApiProductVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "client_app_id": client_app_id,
                        "include": include,
                    },
                    event_api_product_version_retrieve_params.EventAPIProductVersionRetrieveParams,
                ),
            ),
            cast_to=EventAPIProductVersionResponse,
        )

    async def update(
        self,
        version_id: str,
        *,
        event_api_product_id: str,
        approval_type: Literal["automatic", "manual"] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        event_api_product_registrations: Iterable[event_api_product_version_update_params.EventAPIProductRegistration]
        | NotGiven = NOT_GIVEN,
        event_api_version_ids: List[str] | NotGiven = NOT_GIVEN,
        filters: Iterable[event_api_product_version_update_params.Filter] | NotGiven = NOT_GIVEN,
        plans: Iterable[event_api_product_version_update_params.Plan] | NotGiven = NOT_GIVEN,
        publish_state: Literal["unset", "published"] | NotGiven = NOT_GIVEN,
        solace_messaging_services: Iterable[event_api_product_version_update_params.SolaceMessagingService]
        | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        summary: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIProductVersionResponse:
        """Use this API to update an Event API Product version.

        You only need to specify
        the fields that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update:*` ]

        Args:
          approval_type: Approval type

          event_api_version_ids: List of IDs of associated event API versions

          filters: List of filters that contains eventVersionId name and variables

          publish_state: Publish state

          solace_messaging_services: Solace Messaging Services

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return await self._patch(
            f"/api/v2/architecture/eventApiProductVersions/{version_id}",
            body=await async_maybe_transform(
                {
                    "event_api_product_id": event_api_product_id,
                    "approval_type": approval_type,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "event_api_product_registrations": event_api_product_registrations,
                    "event_api_version_ids": event_api_version_ids,
                    "filters": filters,
                    "plans": plans,
                    "publish_state": publish_state,
                    "solace_messaging_services": solace_messaging_services,
                    "state_id": state_id,
                    "summary": summary,
                    "version": version,
                },
                event_api_product_version_update_params.EventAPIProductVersionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIProductVersionResponse,
        )

    async def list(
        self,
        *,
        client_app_id: str | NotGiven = NOT_GIVEN,
        custom_attributes: str | NotGiven = NOT_GIVEN,
        event_api_product_ids: List[str] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        include: str | NotGiven = NOT_GIVEN,
        latest: bool | NotGiven = NOT_GIVEN,
        messaging_service_id: str | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIProductVersionListResponse:
        """
        Use this API to get a list of Event API Product versions that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          client_app_id: Match Event API Product versions with the given clientAppId.

          custom_attributes: Returns the entities that match the custom attribute filter. To filter by custom
              attribute name and value, use the format:
              `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
              by custom attribute name, use the format:
              `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
              operator for multiple custom attribute definitions (not multiple values for a
              given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
              operation. Note: the filter supports custom attribute values containing only the
              characters `[a-zA-Z0-9_\\--\\.. ]`.

          event_api_product_ids: Match only Event API Product versions of these Event API Product IDs, separated
              by commas.

          ids: Match Event API Product versions with the given IDs, separated by commas.

          include: A list of additional entities to include in the response.

          latest: Only return the latest version of Event API Products.

          messaging_service_id: Match Event API Product versions with the given messagingServiceId.

          page_number: The page number to get results from based on the page size.

          page_size: The number of results to return in one page of results.

          shared: Match Event API Product versions with the parent objects shared setting.

          state_id: Match Event API Product versions with the given state ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/v2/architecture/eventApiProductVersions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "client_app_id": client_app_id,
                        "custom_attributes": custom_attributes,
                        "event_api_product_ids": event_api_product_ids,
                        "ids": ids,
                        "include": include,
                        "latest": latest,
                        "messaging_service_id": messaging_service_id,
                        "page_number": page_number,
                        "page_size": page_size,
                        "shared": shared,
                        "state_id": state_id,
                    },
                    event_api_product_version_list_params.EventAPIProductVersionListParams,
                ),
            ),
            cast_to=EventAPIProductVersionListResponse,
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
        Use this API to delete an Event API Product version by ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update:*` ]

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
            f"/api/v2/architecture/eventApiProductVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def publish(
        self,
        version_id: str,
        *,
        event_api_product_id: str,
        approval_type: Literal["automatic", "manual"] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        event_api_product_registrations: Iterable[event_api_product_version_publish_params.EventAPIProductRegistration]
        | NotGiven = NOT_GIVEN,
        event_api_version_ids: List[str] | NotGiven = NOT_GIVEN,
        filters: Iterable[event_api_product_version_publish_params.Filter] | NotGiven = NOT_GIVEN,
        plans: Iterable[event_api_product_version_publish_params.Plan] | NotGiven = NOT_GIVEN,
        publish_state: Literal["unset", "published"] | NotGiven = NOT_GIVEN,
        solace_messaging_services: Iterable[event_api_product_version_publish_params.SolaceMessagingService]
        | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        summary: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StateChangeRequestResponse:
        """Use this API to publish Event API Product version.

        Cannot unset once it is
        published.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update_state:*` ]

        Args:
          approval_type: Approval type

          event_api_version_ids: List of IDs of associated event API versions

          filters: List of filters that contains eventVersionId name and variables

          publish_state: Publish state

          solace_messaging_services: Solace Messaging Services

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return await self._patch(
            f"/api/v2/architecture/eventApiProductVersions/{version_id}/publish",
            body=await async_maybe_transform(
                {
                    "event_api_product_id": event_api_product_id,
                    "approval_type": approval_type,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "event_api_product_registrations": event_api_product_registrations,
                    "event_api_version_ids": event_api_version_ids,
                    "filters": filters,
                    "plans": plans,
                    "publish_state": publish_state,
                    "solace_messaging_services": solace_messaging_services,
                    "state_id": state_id,
                    "summary": summary,
                    "version": version,
                },
                event_api_product_version_publish_params.EventAPIProductVersionPublishParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StateChangeRequestResponse,
        )

    async def update_state(
        self,
        version_id: str,
        *,
        event_api_product_id: str,
        approval_type: Literal["automatic", "manual"] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        event_api_product_registrations: Iterable[
            event_api_product_version_update_state_params.EventAPIProductRegistration
        ]
        | NotGiven = NOT_GIVEN,
        event_api_version_ids: List[str] | NotGiven = NOT_GIVEN,
        filters: Iterable[event_api_product_version_update_state_params.Filter] | NotGiven = NOT_GIVEN,
        plans: Iterable[event_api_product_version_update_state_params.Plan] | NotGiven = NOT_GIVEN,
        publish_state: Literal["unset", "published"] | NotGiven = NOT_GIVEN,
        solace_messaging_services: Iterable[event_api_product_version_update_state_params.SolaceMessagingService]
        | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        summary: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StateChangeRequestResponse:
        """Use this API to update the state of an Event API Product version.

        You only need
        to specify the state ID field with the desired state ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update_state:*` ]

        Args:
          approval_type: Approval type

          event_api_version_ids: List of IDs of associated event API versions

          filters: List of filters that contains eventVersionId name and variables

          publish_state: Publish state

          solace_messaging_services: Solace Messaging Services

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return await self._patch(
            f"/api/v2/architecture/eventApiProductVersions/{version_id}/state",
            body=await async_maybe_transform(
                {
                    "event_api_product_id": event_api_product_id,
                    "approval_type": approval_type,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "event_api_product_registrations": event_api_product_registrations,
                    "event_api_version_ids": event_api_version_ids,
                    "filters": filters,
                    "plans": plans,
                    "publish_state": publish_state,
                    "solace_messaging_services": solace_messaging_services,
                    "state_id": state_id,
                    "summary": summary,
                    "version": version,
                },
                event_api_product_version_update_state_params.EventAPIProductVersionUpdateStateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StateChangeRequestResponse,
        )


class EventAPIProductVersionsResourceWithRawResponse:
    def __init__(self, event_api_product_versions: EventAPIProductVersionsResource) -> None:
        self._event_api_product_versions = event_api_product_versions

        self.create = to_raw_response_wrapper(
            event_api_product_versions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            event_api_product_versions.retrieve,
        )
        self.update = to_raw_response_wrapper(
            event_api_product_versions.update,
        )
        self.list = to_raw_response_wrapper(
            event_api_product_versions.list,
        )
        self.delete = to_raw_response_wrapper(
            event_api_product_versions.delete,
        )
        self.publish = to_raw_response_wrapper(
            event_api_product_versions.publish,
        )
        self.update_state = to_raw_response_wrapper(
            event_api_product_versions.update_state,
        )

    @cached_property
    def mem_associations(self) -> MemAssociationsResourceWithRawResponse:
        return MemAssociationsResourceWithRawResponse(self._event_api_product_versions.mem_associations)


class AsyncEventAPIProductVersionsResourceWithRawResponse:
    def __init__(self, event_api_product_versions: AsyncEventAPIProductVersionsResource) -> None:
        self._event_api_product_versions = event_api_product_versions

        self.create = async_to_raw_response_wrapper(
            event_api_product_versions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            event_api_product_versions.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            event_api_product_versions.update,
        )
        self.list = async_to_raw_response_wrapper(
            event_api_product_versions.list,
        )
        self.delete = async_to_raw_response_wrapper(
            event_api_product_versions.delete,
        )
        self.publish = async_to_raw_response_wrapper(
            event_api_product_versions.publish,
        )
        self.update_state = async_to_raw_response_wrapper(
            event_api_product_versions.update_state,
        )

    @cached_property
    def mem_associations(self) -> AsyncMemAssociationsResourceWithRawResponse:
        return AsyncMemAssociationsResourceWithRawResponse(self._event_api_product_versions.mem_associations)


class EventAPIProductVersionsResourceWithStreamingResponse:
    def __init__(self, event_api_product_versions: EventAPIProductVersionsResource) -> None:
        self._event_api_product_versions = event_api_product_versions

        self.create = to_streamed_response_wrapper(
            event_api_product_versions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            event_api_product_versions.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            event_api_product_versions.update,
        )
        self.list = to_streamed_response_wrapper(
            event_api_product_versions.list,
        )
        self.delete = to_streamed_response_wrapper(
            event_api_product_versions.delete,
        )
        self.publish = to_streamed_response_wrapper(
            event_api_product_versions.publish,
        )
        self.update_state = to_streamed_response_wrapper(
            event_api_product_versions.update_state,
        )

    @cached_property
    def mem_associations(self) -> MemAssociationsResourceWithStreamingResponse:
        return MemAssociationsResourceWithStreamingResponse(self._event_api_product_versions.mem_associations)


class AsyncEventAPIProductVersionsResourceWithStreamingResponse:
    def __init__(self, event_api_product_versions: AsyncEventAPIProductVersionsResource) -> None:
        self._event_api_product_versions = event_api_product_versions

        self.create = async_to_streamed_response_wrapper(
            event_api_product_versions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            event_api_product_versions.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            event_api_product_versions.update,
        )
        self.list = async_to_streamed_response_wrapper(
            event_api_product_versions.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            event_api_product_versions.delete,
        )
        self.publish = async_to_streamed_response_wrapper(
            event_api_product_versions.publish,
        )
        self.update_state = async_to_streamed_response_wrapper(
            event_api_product_versions.update_state,
        )

    @cached_property
    def mem_associations(self) -> AsyncMemAssociationsResourceWithStreamingResponse:
        return AsyncMemAssociationsResourceWithStreamingResponse(self._event_api_product_versions.mem_associations)
