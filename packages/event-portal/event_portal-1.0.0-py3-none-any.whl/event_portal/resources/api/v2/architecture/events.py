# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ....._utils import maybe_transform, async_maybe_transform
from ....._compat import cached_property
from ....._resource import SyncAPIResource, AsyncAPIResource
from ....._response import (
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
from ....._base_client import make_request_options
from .....types.api.v2.architecture import event_list_params, event_create_params, event_update_params
from .....types.api.v2.architecture.event_response import EventResponse
from .....types.api.v2.architecture.custom_attribute_param import CustomAttributeParam

__all__ = ["EventsResource", "AsyncEventsResource"]


class EventsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EventsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return EventsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return EventsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        application_domain_id: str,
        name: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        requires_approval: bool | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventResponse:
        """
        Events are the primary building block of an event-driven architecture.
        Applications publish and subscribe to events and events reference schemas. In
        the Event Portal, an event is a type of event as opposed to a specific event
        instance.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event:create:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._post(
            "/api/v2/architecture/events",
            body=maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "name": name,
                    "custom_attributes": custom_attributes,
                    "requires_approval": requires_approval,
                    "shared": shared,
                },
                event_create_params.EventCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventResponse,
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
    ) -> EventResponse:
        """
        Use this API to get a single event by its ID.

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
            f"/api/v2/architecture/events/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventResponse,
        )

    def update(
        self,
        id: str,
        *,
        application_domain_id: str,
        name: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        requires_approval: bool | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventResponse:
        """Use this API to update an event.

        You only need to specify the fields that need
        to be updated.

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
            f"/api/v2/architecture/events/{id}",
            body=maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "name": name,
                    "custom_attributes": custom_attributes,
                    "requires_approval": requires_approval,
                    "shared": shared,
                },
                event_update_params.EventUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventResponse,
        )

    def list(
        self,
        *,
        application_domain_id: str | NotGiven = NOT_GIVEN,
        application_domain_ids: List[str] | NotGiven = NOT_GIVEN,
        broker_type: str | NotGiven = NOT_GIVEN,
        custom_attributes: str | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        Use this API to get a list of events that match the given parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_domain_id: Match only events in the given application domain.

          application_domain_ids: Match only events in the given application domain ids.

          broker_type: Match only events with the given broker type

          custom_attributes: Returns the entities that match the custom attribute filter. To filter by custom
              attribute name and value, use the format:
              `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
              by custom attribute name, use the format:
              `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
              operator for multiple custom attribute definitions (not multiple values for a
              given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
              operation. Note: the filter supports custom attribute values containing only the
              characters `[a-zA-Z0-9_\\--\\.. ]`.

          ids: Match only events with the given IDs separated by commas.

          name: Name of the event to match on.

          page_number: The page number to get.

          page_size: The number of events to get per page.

          shared: Match only with shared or unshared events.

          sort: The sorting criteria for the returned results. You can sort the results by query
              parameter in ascending or descending order. Define the sort order using the
              following string: `fieldname:asc/desc` where:

              - `fieldname` — The field name of the query parameter to sort by.
              - `asc` — Sort the selected field name in ascending order.
              - `desc` — Sort the selected field name in descending order.

              If the direction is not specified, the default is ascending.

              You can use multiple query parameters to refine the sorting order.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._get(
            "/api/v2/architecture/events",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "application_domain_id": application_domain_id,
                        "application_domain_ids": application_domain_ids,
                        "broker_type": broker_type,
                        "custom_attributes": custom_attributes,
                        "ids": ids,
                        "name": name,
                        "page_number": page_number,
                        "page_size": page_size,
                        "shared": shared,
                        "sort": sort,
                    },
                    event_list_params.EventListParams,
                ),
            ),
            cast_to=BinaryAPIResponse,
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
        Use this API to delete an event.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event:delete:*` ]

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
            f"/api/v2/architecture/events/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncEventsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEventsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEventsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncEventsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        application_domain_id: str,
        name: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        requires_approval: bool | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventResponse:
        """
        Events are the primary building block of an event-driven architecture.
        Applications publish and subscribe to events and events reference schemas. In
        the Event Portal, an event is a type of event as opposed to a specific event
        instance.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event:create:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._post(
            "/api/v2/architecture/events",
            body=await async_maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "name": name,
                    "custom_attributes": custom_attributes,
                    "requires_approval": requires_approval,
                    "shared": shared,
                },
                event_create_params.EventCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventResponse,
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
    ) -> EventResponse:
        """
        Use this API to get a single event by its ID.

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
            f"/api/v2/architecture/events/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventResponse,
        )

    async def update(
        self,
        id: str,
        *,
        application_domain_id: str,
        name: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        requires_approval: bool | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventResponse:
        """Use this API to update an event.

        You only need to specify the fields that need
        to be updated.

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
            f"/api/v2/architecture/events/{id}",
            body=await async_maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "name": name,
                    "custom_attributes": custom_attributes,
                    "requires_approval": requires_approval,
                    "shared": shared,
                },
                event_update_params.EventUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventResponse,
        )

    async def list(
        self,
        *,
        application_domain_id: str | NotGiven = NOT_GIVEN,
        application_domain_ids: List[str] | NotGiven = NOT_GIVEN,
        broker_type: str | NotGiven = NOT_GIVEN,
        custom_attributes: str | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        Use this API to get a list of events that match the given parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_domain_id: Match only events in the given application domain.

          application_domain_ids: Match only events in the given application domain ids.

          broker_type: Match only events with the given broker type

          custom_attributes: Returns the entities that match the custom attribute filter. To filter by custom
              attribute name and value, use the format:
              `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
              by custom attribute name, use the format:
              `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
              operator for multiple custom attribute definitions (not multiple values for a
              given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
              operation. Note: the filter supports custom attribute values containing only the
              characters `[a-zA-Z0-9_\\--\\.. ]`.

          ids: Match only events with the given IDs separated by commas.

          name: Name of the event to match on.

          page_number: The page number to get.

          page_size: The number of events to get per page.

          shared: Match only with shared or unshared events.

          sort: The sorting criteria for the returned results. You can sort the results by query
              parameter in ascending or descending order. Define the sort order using the
              following string: `fieldname:asc/desc` where:

              - `fieldname` — The field name of the query parameter to sort by.
              - `asc` — Sort the selected field name in ascending order.
              - `desc` — Sort the selected field name in descending order.

              If the direction is not specified, the default is ascending.

              You can use multiple query parameters to refine the sorting order.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._get(
            "/api/v2/architecture/events",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "application_domain_id": application_domain_id,
                        "application_domain_ids": application_domain_ids,
                        "broker_type": broker_type,
                        "custom_attributes": custom_attributes,
                        "ids": ids,
                        "name": name,
                        "page_number": page_number,
                        "page_size": page_size,
                        "shared": shared,
                        "sort": sort,
                    },
                    event_list_params.EventListParams,
                ),
            ),
            cast_to=AsyncBinaryAPIResponse,
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
        Use this API to delete an event.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event:delete:*` ]

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
            f"/api/v2/architecture/events/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class EventsResourceWithRawResponse:
    def __init__(self, events: EventsResource) -> None:
        self._events = events

        self.create = to_raw_response_wrapper(
            events.create,
        )
        self.retrieve = to_raw_response_wrapper(
            events.retrieve,
        )
        self.update = to_raw_response_wrapper(
            events.update,
        )
        self.list = to_custom_raw_response_wrapper(
            events.list,
            BinaryAPIResponse,
        )
        self.delete = to_raw_response_wrapper(
            events.delete,
        )


class AsyncEventsResourceWithRawResponse:
    def __init__(self, events: AsyncEventsResource) -> None:
        self._events = events

        self.create = async_to_raw_response_wrapper(
            events.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            events.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            events.update,
        )
        self.list = async_to_custom_raw_response_wrapper(
            events.list,
            AsyncBinaryAPIResponse,
        )
        self.delete = async_to_raw_response_wrapper(
            events.delete,
        )


class EventsResourceWithStreamingResponse:
    def __init__(self, events: EventsResource) -> None:
        self._events = events

        self.create = to_streamed_response_wrapper(
            events.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            events.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            events.update,
        )
        self.list = to_custom_streamed_response_wrapper(
            events.list,
            StreamedBinaryAPIResponse,
        )
        self.delete = to_streamed_response_wrapper(
            events.delete,
        )


class AsyncEventsResourceWithStreamingResponse:
    def __init__(self, events: AsyncEventsResource) -> None:
        self._events = events

        self.create = async_to_streamed_response_wrapper(
            events.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            events.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            events.update,
        )
        self.list = async_to_custom_streamed_response_wrapper(
            events.list,
            AsyncStreamedBinaryAPIResponse,
        )
        self.delete = async_to_streamed_response_wrapper(
            events.delete,
        )
