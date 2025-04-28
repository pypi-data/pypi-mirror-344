# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ....._utils import maybe_transform, async_maybe_transform
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.api.v2.architecture import (
    event_version_list_params,
    event_version_create_params,
    event_version_update_params,
    event_version_update_state_params,
    event_version_replace_messaging_service_params,
)
from .....types.api.v2.architecture.custom_attribute_param import CustomAttributeParam
from .....types.api.v2.architecture.event_version_response import EventVersionResponse
from .....types.api.v2.architecture.delivery_descriptor_param import DeliveryDescriptorParam
from .....types.api.v2.architecture.event_version_list_response import EventVersionListResponse
from .....types.api.v2.architecture.state_change_request_response import StateChangeRequestResponse
from .....types.api.v2.architecture.validation_messages_dto_param import ValidationMessagesDtoParam
from .....types.api.v2.architecture.messaging_service_association_response import MessagingServiceAssociationResponse

__all__ = ["EventVersionsResource", "AsyncEventVersionsResource"]


class EventVersionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EventVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return EventVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return EventVersionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        event_id: str,
        version: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        delivery_descriptor: DeliveryDescriptorParam | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        schema_primitive_type: Literal["BOOLEAN", "BYTES", "DOUBLE", "FLOAT", "INT", "LONG", "NULL", "NUMBER", "STRING"]
        | NotGiven = NOT_GIVEN,
        schema_version_id: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        validation_messages: ValidationMessagesDtoParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventVersionResponse:
        """
        Create an event version

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._post(
            "/api/v2/architecture/eventVersions",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "version": version,
                    "custom_attributes": custom_attributes,
                    "delivery_descriptor": delivery_descriptor,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "schema_primitive_type": schema_primitive_type,
                    "schema_version_id": schema_version_id,
                    "type": type,
                    "validation_messages": validation_messages,
                },
                event_version_create_params.EventVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventVersionResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventVersionResponse:
        """
        Use this API to get a single event version by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            f"/api/v2/architecture/eventVersions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventVersionResponse,
        )

    def update(
        self,
        id: str,
        *,
        event_id: str,
        version: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        delivery_descriptor: DeliveryDescriptorParam | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        schema_primitive_type: Literal["BOOLEAN", "BYTES", "DOUBLE", "FLOAT", "INT", "LONG", "NULL", "NUMBER", "STRING"]
        | NotGiven = NOT_GIVEN,
        schema_version_id: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        validation_messages: ValidationMessagesDtoParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventVersionResponse:
        """Use this API to update an event version.

        You only need to specify the fields
        that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._patch(
            f"/api/v2/architecture/eventVersions/{id}",
            body=maybe_transform(
                {
                    "event_id": event_id,
                    "version": version,
                    "custom_attributes": custom_attributes,
                    "delivery_descriptor": delivery_descriptor,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "schema_primitive_type": schema_primitive_type,
                    "schema_version_id": schema_version_id,
                    "type": type,
                    "validation_messages": validation_messages,
                },
                event_version_update_params.EventVersionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventVersionResponse,
        )

    def list(
        self,
        *,
        custom_attributes: str | NotGiven = NOT_GIVEN,
        event_ids: List[str] | NotGiven = NOT_GIVEN,
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
    ) -> EventVersionListResponse:
        """
        Use this API to get a list of event versions that match the given parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          custom_attributes: Returns the entities that match the custom attribute filter. To filter by custom
              attribute name and value, use the format:
              `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
              by custom attribute name, use the format:
              `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
              operator for multiple custom attribute definitions (not multiple values for a
              given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
              operation. Note: the filter supports custom attribute values containing only the
              characters `[a-zA-Z0-9_\\--\\.. ]`.

          event_ids: Match only event versions of these event IDs, separated by commas.

          ids: Match only event versions with the given IDs, separated by commas.

          messaging_service_ids: Match only event versions with the given messaging service IDs, separated by
              commas.

          page_number: The page number to get.

          page_size: The number of event versions to get per page.

          state_ids: Match only event versions with the given state IDs, separated by commas.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            "/api/v2/architecture/eventVersions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "custom_attributes": custom_attributes,
                        "event_ids": event_ids,
                        "ids": ids,
                        "messaging_service_ids": messaging_service_ids,
                        "page_number": page_number,
                        "page_size": page_size,
                        "state_ids": state_ids,
                    },
                    event_version_list_params.EventVersionListParams,
                ),
            ),
            cast_to=EventVersionListResponse,
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
        """
        Use this API to delete an event version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event:update:*` ]

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
            f"/api/v2/architecture/eventVersions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def replace_messaging_service(
        self,
        id: str,
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
        Use this API to replace the messaging service association for an event version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_runtime:write` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._put(
            f"/api/v2/architecture/eventVersions/{id}/messagingServices",
            body=maybe_transform(
                {"messaging_service_ids": messaging_service_ids},
                event_version_replace_messaging_service_params.EventVersionReplaceMessagingServiceParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MessagingServiceAssociationResponse,
        )

    def update_state(
        self,
        id: str,
        *,
        state_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StateChangeRequestResponse:
        """Use this API to update the state of event version.

        You only need to specify the
        target stateId field

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event:update_state:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._patch(
            f"/api/v2/architecture/eventVersions/{id}/state",
            body=maybe_transform(
                {"state_id": state_id}, event_version_update_state_params.EventVersionUpdateStateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StateChangeRequestResponse,
        )


class AsyncEventVersionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEventVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEventVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncEventVersionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        event_id: str,
        version: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        delivery_descriptor: DeliveryDescriptorParam | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        schema_primitive_type: Literal["BOOLEAN", "BYTES", "DOUBLE", "FLOAT", "INT", "LONG", "NULL", "NUMBER", "STRING"]
        | NotGiven = NOT_GIVEN,
        schema_version_id: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        validation_messages: ValidationMessagesDtoParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventVersionResponse:
        """
        Create an event version

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._post(
            "/api/v2/architecture/eventVersions",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "version": version,
                    "custom_attributes": custom_attributes,
                    "delivery_descriptor": delivery_descriptor,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "schema_primitive_type": schema_primitive_type,
                    "schema_version_id": schema_version_id,
                    "type": type,
                    "validation_messages": validation_messages,
                },
                event_version_create_params.EventVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventVersionResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventVersionResponse:
        """
        Use this API to get a single event version by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            f"/api/v2/architecture/eventVersions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventVersionResponse,
        )

    async def update(
        self,
        id: str,
        *,
        event_id: str,
        version: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        delivery_descriptor: DeliveryDescriptorParam | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        schema_primitive_type: Literal["BOOLEAN", "BYTES", "DOUBLE", "FLOAT", "INT", "LONG", "NULL", "NUMBER", "STRING"]
        | NotGiven = NOT_GIVEN,
        schema_version_id: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        validation_messages: ValidationMessagesDtoParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventVersionResponse:
        """Use this API to update an event version.

        You only need to specify the fields
        that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._patch(
            f"/api/v2/architecture/eventVersions/{id}",
            body=await async_maybe_transform(
                {
                    "event_id": event_id,
                    "version": version,
                    "custom_attributes": custom_attributes,
                    "delivery_descriptor": delivery_descriptor,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "schema_primitive_type": schema_primitive_type,
                    "schema_version_id": schema_version_id,
                    "type": type,
                    "validation_messages": validation_messages,
                },
                event_version_update_params.EventVersionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventVersionResponse,
        )

    async def list(
        self,
        *,
        custom_attributes: str | NotGiven = NOT_GIVEN,
        event_ids: List[str] | NotGiven = NOT_GIVEN,
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
    ) -> EventVersionListResponse:
        """
        Use this API to get a list of event versions that match the given parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          custom_attributes: Returns the entities that match the custom attribute filter. To filter by custom
              attribute name and value, use the format:
              `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
              by custom attribute name, use the format:
              `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
              operator for multiple custom attribute definitions (not multiple values for a
              given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
              operation. Note: the filter supports custom attribute values containing only the
              characters `[a-zA-Z0-9_\\--\\.. ]`.

          event_ids: Match only event versions of these event IDs, separated by commas.

          ids: Match only event versions with the given IDs, separated by commas.

          messaging_service_ids: Match only event versions with the given messaging service IDs, separated by
              commas.

          page_number: The page number to get.

          page_size: The number of event versions to get per page.

          state_ids: Match only event versions with the given state IDs, separated by commas.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            "/api/v2/architecture/eventVersions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "custom_attributes": custom_attributes,
                        "event_ids": event_ids,
                        "ids": ids,
                        "messaging_service_ids": messaging_service_ids,
                        "page_number": page_number,
                        "page_size": page_size,
                        "state_ids": state_ids,
                    },
                    event_version_list_params.EventVersionListParams,
                ),
            ),
            cast_to=EventVersionListResponse,
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
        """
        Use this API to delete an event version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event:update:*` ]

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
            f"/api/v2/architecture/eventVersions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def replace_messaging_service(
        self,
        id: str,
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
        Use this API to replace the messaging service association for an event version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_runtime:write` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._put(
            f"/api/v2/architecture/eventVersions/{id}/messagingServices",
            body=await async_maybe_transform(
                {"messaging_service_ids": messaging_service_ids},
                event_version_replace_messaging_service_params.EventVersionReplaceMessagingServiceParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MessagingServiceAssociationResponse,
        )

    async def update_state(
        self,
        id: str,
        *,
        state_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StateChangeRequestResponse:
        """Use this API to update the state of event version.

        You only need to specify the
        target stateId field

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event:update_state:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._patch(
            f"/api/v2/architecture/eventVersions/{id}/state",
            body=await async_maybe_transform(
                {"state_id": state_id}, event_version_update_state_params.EventVersionUpdateStateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StateChangeRequestResponse,
        )


class EventVersionsResourceWithRawResponse:
    def __init__(self, event_versions: EventVersionsResource) -> None:
        self._event_versions = event_versions

        self.create = to_raw_response_wrapper(
            event_versions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            event_versions.retrieve,
        )
        self.update = to_raw_response_wrapper(
            event_versions.update,
        )
        self.list = to_raw_response_wrapper(
            event_versions.list,
        )
        self.delete = to_raw_response_wrapper(
            event_versions.delete,
        )
        self.replace_messaging_service = to_raw_response_wrapper(
            event_versions.replace_messaging_service,
        )
        self.update_state = to_raw_response_wrapper(
            event_versions.update_state,
        )


class AsyncEventVersionsResourceWithRawResponse:
    def __init__(self, event_versions: AsyncEventVersionsResource) -> None:
        self._event_versions = event_versions

        self.create = async_to_raw_response_wrapper(
            event_versions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            event_versions.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            event_versions.update,
        )
        self.list = async_to_raw_response_wrapper(
            event_versions.list,
        )
        self.delete = async_to_raw_response_wrapper(
            event_versions.delete,
        )
        self.replace_messaging_service = async_to_raw_response_wrapper(
            event_versions.replace_messaging_service,
        )
        self.update_state = async_to_raw_response_wrapper(
            event_versions.update_state,
        )


class EventVersionsResourceWithStreamingResponse:
    def __init__(self, event_versions: EventVersionsResource) -> None:
        self._event_versions = event_versions

        self.create = to_streamed_response_wrapper(
            event_versions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            event_versions.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            event_versions.update,
        )
        self.list = to_streamed_response_wrapper(
            event_versions.list,
        )
        self.delete = to_streamed_response_wrapper(
            event_versions.delete,
        )
        self.replace_messaging_service = to_streamed_response_wrapper(
            event_versions.replace_messaging_service,
        )
        self.update_state = to_streamed_response_wrapper(
            event_versions.update_state,
        )


class AsyncEventVersionsResourceWithStreamingResponse:
    def __init__(self, event_versions: AsyncEventVersionsResource) -> None:
        self._event_versions = event_versions

        self.create = async_to_streamed_response_wrapper(
            event_versions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            event_versions.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            event_versions.update,
        )
        self.list = async_to_streamed_response_wrapper(
            event_versions.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            event_versions.delete,
        )
        self.replace_messaging_service = async_to_streamed_response_wrapper(
            event_versions.replace_messaging_service,
        )
        self.update_state = async_to_streamed_response_wrapper(
            event_versions.update_state,
        )
