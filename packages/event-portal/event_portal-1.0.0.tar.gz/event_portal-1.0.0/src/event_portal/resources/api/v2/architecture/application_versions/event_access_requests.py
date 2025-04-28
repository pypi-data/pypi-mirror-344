# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

import httpx

from ......_types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
from ......types.api.v2.architecture.application_versions import event_access_request_list_params
from ......types.api.v2.architecture.application_version_event_access_requests_response import (
    ApplicationVersionEventAccessRequestsResponse,
)
from ......types.api.v2.architecture.application_versions.event_access_requests_list_response import (
    EventAccessRequestsListResponse,
)

__all__ = ["EventAccessRequestsResource", "AsyncEventAccessRequestsResource"]


class EventAccessRequestsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EventAccessRequestsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return EventAccessRequestsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventAccessRequestsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return EventAccessRequestsResourceWithStreamingResponse(self)

    def create(
        self,
        application_version_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAccessRequestsListResponse:
        """
        Create missing event access requests for application version id and send
        notifications to reviewers

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` **and**
        `event_access_request:create:*` ]

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
        return self._post(
            f"/api/v2/architecture/applicationVersions/{application_version_id}/eventAccessRequests",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAccessRequestsListResponse,
        )

    def list(
        self,
        application_version_id: str,
        *,
        review_statuses: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVersionEventAccessRequestsResponse:
        """
        Get event access requests by application version id

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:get:*` ]

        Args:
          review_statuses: Get requests with the given review statuses

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
            f"/api/v2/architecture/applicationVersions/{application_version_id}/eventAccessRequests",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"review_statuses": review_statuses}, event_access_request_list_params.EventAccessRequestListParams
                ),
            ),
            cast_to=ApplicationVersionEventAccessRequestsResponse,
        )


class AsyncEventAccessRequestsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEventAccessRequestsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEventAccessRequestsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventAccessRequestsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncEventAccessRequestsResourceWithStreamingResponse(self)

    async def create(
        self,
        application_version_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAccessRequestsListResponse:
        """
        Create missing event access requests for application version id and send
        notifications to reviewers

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` **and**
        `event_access_request:create:*` ]

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
        return await self._post(
            f"/api/v2/architecture/applicationVersions/{application_version_id}/eventAccessRequests",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAccessRequestsListResponse,
        )

    async def list(
        self,
        application_version_id: str,
        *,
        review_statuses: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ApplicationVersionEventAccessRequestsResponse:
        """
        Get event access requests by application version id

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:get:*` ]

        Args:
          review_statuses: Get requests with the given review statuses

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
            f"/api/v2/architecture/applicationVersions/{application_version_id}/eventAccessRequests",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"review_statuses": review_statuses}, event_access_request_list_params.EventAccessRequestListParams
                ),
            ),
            cast_to=ApplicationVersionEventAccessRequestsResponse,
        )


class EventAccessRequestsResourceWithRawResponse:
    def __init__(self, event_access_requests: EventAccessRequestsResource) -> None:
        self._event_access_requests = event_access_requests

        self.create = to_raw_response_wrapper(
            event_access_requests.create,
        )
        self.list = to_raw_response_wrapper(
            event_access_requests.list,
        )


class AsyncEventAccessRequestsResourceWithRawResponse:
    def __init__(self, event_access_requests: AsyncEventAccessRequestsResource) -> None:
        self._event_access_requests = event_access_requests

        self.create = async_to_raw_response_wrapper(
            event_access_requests.create,
        )
        self.list = async_to_raw_response_wrapper(
            event_access_requests.list,
        )


class EventAccessRequestsResourceWithStreamingResponse:
    def __init__(self, event_access_requests: EventAccessRequestsResource) -> None:
        self._event_access_requests = event_access_requests

        self.create = to_streamed_response_wrapper(
            event_access_requests.create,
        )
        self.list = to_streamed_response_wrapper(
            event_access_requests.list,
        )


class AsyncEventAccessRequestsResourceWithStreamingResponse:
    def __init__(self, event_access_requests: AsyncEventAccessRequestsResource) -> None:
        self._event_access_requests = event_access_requests

        self.create = async_to_streamed_response_wrapper(
            event_access_requests.create,
        )
        self.list = async_to_streamed_response_wrapper(
            event_access_requests.list,
        )
