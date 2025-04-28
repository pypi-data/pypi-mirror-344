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
from .....types.api.v2.architecture import consumer_list_params, consumer_create_params, consumer_update_params
from .....types.api.v2.architecture.consumer_response import ConsumerResponse
from .....types.api.v2.architecture.subscription_param import SubscriptionParam
from .....types.api.v2.architecture.consumer_list_response import ConsumerListResponse

__all__ = ["ConsumersResource", "AsyncConsumersResource"]


class ConsumersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConsumersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return ConsumersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConsumersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return ConsumersResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        application_version_id: str,
        broker_type: str | NotGiven = NOT_GIVEN,
        consumer_type: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        subscriptions: Iterable[SubscriptionParam] | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        Use this API to create a consumer.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/api/v2/architecture/consumers",
            body=maybe_transform(
                {
                    "application_version_id": application_version_id,
                    "broker_type": broker_type,
                    "consumer_type": consumer_type,
                    "name": name,
                    "subscriptions": subscriptions,
                    "type": type,
                },
                consumer_create_params.ConsumerCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
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
    ) -> ConsumerResponse:
        """
        Use this API to get a single consumer by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:get:*` ]

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
            f"/api/v2/architecture/consumers/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConsumerResponse,
        )

    def update(
        self,
        id: str,
        *,
        application_version_id: str,
        broker_type: str | NotGiven = NOT_GIVEN,
        consumer_type: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        subscriptions: Iterable[SubscriptionParam] | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsumerResponse:
        """
        Use this API to update a consumer.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

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
            f"/api/v2/architecture/consumers/{id}",
            body=maybe_transform(
                {
                    "application_version_id": application_version_id,
                    "broker_type": broker_type,
                    "consumer_type": consumer_type,
                    "name": name,
                    "subscriptions": subscriptions,
                    "type": type,
                },
                consumer_update_params.ConsumerUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConsumerResponse,
        )

    def list(
        self,
        *,
        application_version_ids: List[str] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsumerListResponse:
        """
        Use this API to get a list of consumers that match the given parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_version_ids: Match only consumers with the given application version IDs, separated by
              commas.

          ids: Match only consumers with the given IDs separated by commas.

          page_number: The page number to get.

          page_size: The number of consumers to get per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            "/api/v2/architecture/consumers",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "application_version_ids": application_version_ids,
                        "ids": ids,
                        "page_number": page_number,
                        "page_size": page_size,
                    },
                    consumer_list_params.ConsumerListParams,
                ),
            ),
            cast_to=ConsumerListResponse,
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
        Use this API to delete a consumer.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

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
            f"/api/v2/architecture/consumers/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncConsumersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConsumersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConsumersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConsumersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncConsumersResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        application_version_id: str,
        broker_type: str | NotGiven = NOT_GIVEN,
        consumer_type: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        subscriptions: Iterable[SubscriptionParam] | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        Use this API to create a consumer.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/api/v2/architecture/consumers",
            body=await async_maybe_transform(
                {
                    "application_version_id": application_version_id,
                    "broker_type": broker_type,
                    "consumer_type": consumer_type,
                    "name": name,
                    "subscriptions": subscriptions,
                    "type": type,
                },
                consumer_create_params.ConsumerCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
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
    ) -> ConsumerResponse:
        """
        Use this API to get a single consumer by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:get:*` ]

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
            f"/api/v2/architecture/consumers/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConsumerResponse,
        )

    async def update(
        self,
        id: str,
        *,
        application_version_id: str,
        broker_type: str | NotGiven = NOT_GIVEN,
        consumer_type: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        subscriptions: Iterable[SubscriptionParam] | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsumerResponse:
        """
        Use this API to update a consumer.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

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
            f"/api/v2/architecture/consumers/{id}",
            body=await async_maybe_transform(
                {
                    "application_version_id": application_version_id,
                    "broker_type": broker_type,
                    "consumer_type": consumer_type,
                    "name": name,
                    "subscriptions": subscriptions,
                    "type": type,
                },
                consumer_update_params.ConsumerUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConsumerResponse,
        )

    async def list(
        self,
        *,
        application_version_ids: List[str] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConsumerListResponse:
        """
        Use this API to get a list of consumers that match the given parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_version_ids: Match only consumers with the given application version IDs, separated by
              commas.

          ids: Match only consumers with the given IDs separated by commas.

          page_number: The page number to get.

          page_size: The number of consumers to get per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            "/api/v2/architecture/consumers",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "application_version_ids": application_version_ids,
                        "ids": ids,
                        "page_number": page_number,
                        "page_size": page_size,
                    },
                    consumer_list_params.ConsumerListParams,
                ),
            ),
            cast_to=ConsumerListResponse,
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
        Use this API to delete a consumer.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

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
            f"/api/v2/architecture/consumers/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class ConsumersResourceWithRawResponse:
    def __init__(self, consumers: ConsumersResource) -> None:
        self._consumers = consumers

        self.create = to_custom_raw_response_wrapper(
            consumers.create,
            BinaryAPIResponse,
        )
        self.retrieve = to_raw_response_wrapper(
            consumers.retrieve,
        )
        self.update = to_raw_response_wrapper(
            consumers.update,
        )
        self.list = to_raw_response_wrapper(
            consumers.list,
        )
        self.delete = to_raw_response_wrapper(
            consumers.delete,
        )


class AsyncConsumersResourceWithRawResponse:
    def __init__(self, consumers: AsyncConsumersResource) -> None:
        self._consumers = consumers

        self.create = async_to_custom_raw_response_wrapper(
            consumers.create,
            AsyncBinaryAPIResponse,
        )
        self.retrieve = async_to_raw_response_wrapper(
            consumers.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            consumers.update,
        )
        self.list = async_to_raw_response_wrapper(
            consumers.list,
        )
        self.delete = async_to_raw_response_wrapper(
            consumers.delete,
        )


class ConsumersResourceWithStreamingResponse:
    def __init__(self, consumers: ConsumersResource) -> None:
        self._consumers = consumers

        self.create = to_custom_streamed_response_wrapper(
            consumers.create,
            StreamedBinaryAPIResponse,
        )
        self.retrieve = to_streamed_response_wrapper(
            consumers.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            consumers.update,
        )
        self.list = to_streamed_response_wrapper(
            consumers.list,
        )
        self.delete = to_streamed_response_wrapper(
            consumers.delete,
        )


class AsyncConsumersResourceWithStreamingResponse:
    def __init__(self, consumers: AsyncConsumersResource) -> None:
        self._consumers = consumers

        self.create = async_to_custom_streamed_response_wrapper(
            consumers.create,
            AsyncStreamedBinaryAPIResponse,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            consumers.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            consumers.update,
        )
        self.list = async_to_streamed_response_wrapper(
            consumers.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            consumers.delete,
        )
