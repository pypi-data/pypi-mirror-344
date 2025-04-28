# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
from .....types.api.v2.architecture import topic_domain_list_params, topic_domain_create_params
from .....types.api.v2.architecture.address_level_param import AddressLevelParam
from .....types.api.v2.architecture.topic_domain_response import TopicDomainResponse
from .....types.api.v2.architecture.topic_domain_list_response import TopicDomainListResponse

__all__ = ["TopicDomainsResource", "AsyncTopicDomainsResource"]


class TopicDomainsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> TopicDomainsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return TopicDomainsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> TopicDomainsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return TopicDomainsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        address_levels: Iterable[AddressLevelParam],
        application_domain_id: str,
        broker_type: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TopicDomainResponse:
        """
        Topic Domains govern the format of topic addresses within an application domain

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `topic_domain:create:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._post(
            "/api/v2/architecture/topicDomains",
            body=maybe_transform(
                {
                    "address_levels": address_levels,
                    "application_domain_id": application_domain_id,
                    "broker_type": broker_type,
                },
                topic_domain_create_params.TopicDomainCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicDomainResponse,
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
    ) -> TopicDomainResponse:
        """
        Use this API to get a single topic domain by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `topic_domain:get:*` ]

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
            f"/api/v2/architecture/topicDomains/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicDomainResponse,
        )

    def list(
        self,
        *,
        application_domain_id: str | NotGiven = NOT_GIVEN,
        application_domain_ids: List[str] | NotGiven = NOT_GIVEN,
        broker_type: str | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TopicDomainListResponse:
        """
        Use this API to get a list of topic domains that match the given parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_domain_ids: Match only topic domains with the given application domain ids separated by
              commas.

          broker_type: Match only topic domains with the given brokerType.

          ids: Match only topic domains with the given IDs separated by commas.

          page_number: The page number to get.

          page_size: The number of topic domains to get per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            "/api/v2/architecture/topicDomains",
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
                        "ids": ids,
                        "page_number": page_number,
                        "page_size": page_size,
                    },
                    topic_domain_list_params.TopicDomainListParams,
                ),
            ),
            cast_to=TopicDomainListResponse,
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
    ) -> BinaryAPIResponse:
        """
        Use this API to delete a topic domain.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `topic_domain:delete:*` ]

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
            f"/api/v2/architecture/topicDomains/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncTopicDomainsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncTopicDomainsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncTopicDomainsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncTopicDomainsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncTopicDomainsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        address_levels: Iterable[AddressLevelParam],
        application_domain_id: str,
        broker_type: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TopicDomainResponse:
        """
        Topic Domains govern the format of topic addresses within an application domain

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `topic_domain:create:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._post(
            "/api/v2/architecture/topicDomains",
            body=await async_maybe_transform(
                {
                    "address_levels": address_levels,
                    "application_domain_id": application_domain_id,
                    "broker_type": broker_type,
                },
                topic_domain_create_params.TopicDomainCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicDomainResponse,
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
    ) -> TopicDomainResponse:
        """
        Use this API to get a single topic domain by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `topic_domain:get:*` ]

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
            f"/api/v2/architecture/topicDomains/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicDomainResponse,
        )

    async def list(
        self,
        *,
        application_domain_id: str | NotGiven = NOT_GIVEN,
        application_domain_ids: List[str] | NotGiven = NOT_GIVEN,
        broker_type: str | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TopicDomainListResponse:
        """
        Use this API to get a list of topic domains that match the given parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_domain_ids: Match only topic domains with the given application domain ids separated by
              commas.

          broker_type: Match only topic domains with the given brokerType.

          ids: Match only topic domains with the given IDs separated by commas.

          page_number: The page number to get.

          page_size: The number of topic domains to get per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            "/api/v2/architecture/topicDomains",
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
                        "ids": ids,
                        "page_number": page_number,
                        "page_size": page_size,
                    },
                    topic_domain_list_params.TopicDomainListParams,
                ),
            ),
            cast_to=TopicDomainListResponse,
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
    ) -> AsyncBinaryAPIResponse:
        """
        Use this API to delete a topic domain.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `topic_domain:delete:*` ]

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
            f"/api/v2/architecture/topicDomains/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class TopicDomainsResourceWithRawResponse:
    def __init__(self, topic_domains: TopicDomainsResource) -> None:
        self._topic_domains = topic_domains

        self.create = to_raw_response_wrapper(
            topic_domains.create,
        )
        self.retrieve = to_raw_response_wrapper(
            topic_domains.retrieve,
        )
        self.list = to_raw_response_wrapper(
            topic_domains.list,
        )
        self.delete = to_custom_raw_response_wrapper(
            topic_domains.delete,
            BinaryAPIResponse,
        )


class AsyncTopicDomainsResourceWithRawResponse:
    def __init__(self, topic_domains: AsyncTopicDomainsResource) -> None:
        self._topic_domains = topic_domains

        self.create = async_to_raw_response_wrapper(
            topic_domains.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            topic_domains.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            topic_domains.list,
        )
        self.delete = async_to_custom_raw_response_wrapper(
            topic_domains.delete,
            AsyncBinaryAPIResponse,
        )


class TopicDomainsResourceWithStreamingResponse:
    def __init__(self, topic_domains: TopicDomainsResource) -> None:
        self._topic_domains = topic_domains

        self.create = to_streamed_response_wrapper(
            topic_domains.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            topic_domains.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            topic_domains.list,
        )
        self.delete = to_custom_streamed_response_wrapper(
            topic_domains.delete,
            StreamedBinaryAPIResponse,
        )


class AsyncTopicDomainsResourceWithStreamingResponse:
    def __init__(self, topic_domains: AsyncTopicDomainsResource) -> None:
        self._topic_domains = topic_domains

        self.create = async_to_streamed_response_wrapper(
            topic_domains.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            topic_domains.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            topic_domains.list,
        )
        self.delete = async_to_custom_streamed_response_wrapper(
            topic_domains.delete,
            AsyncStreamedBinaryAPIResponse,
        )
