# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ....._types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
    event_access_request_list_params,
    event_access_request_update_params,
    event_access_request_approve_params,
    event_access_request_decline_params,
)
from .....types.api.v2.architecture.review_response import ReviewResponse
from .....types.api.v2.architecture.event_access_request_response import EventAccessRequestResponse
from .....types.api.v2.architecture.application_versions.event_access_requests_list_response import (
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
    ) -> EventAccessRequestResponse:
        """
        Get event access request by id

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_request:get:*` **or**
        `event_access_request:review:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/api/v2/architecture/eventAccessRequests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAccessRequestResponse,
        )

    def update(
        self,
        id: str,
        *,
        comments: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAccessRequestResponse:
        """Use this API to update an event access request.

        You only need to specify the
        fields that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_request:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            f"/api/v2/architecture/eventAccessRequests/{id}",
            body=maybe_transform(
                {"comments": comments}, event_access_request_update_params.EventAccessRequestUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAccessRequestResponse,
        )

    def list(
        self,
        *,
        application_ids: List[str] | NotGiven = NOT_GIVEN,
        can_review: bool | NotGiven = NOT_GIVEN,
        created_bys: List[str] | NotGiven = NOT_GIVEN,
        event_ids: List[str] | NotGiven = NOT_GIVEN,
        exclude_auto_approved_events: bool | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        relationships: List[Literal["consuming", "producing"]] | NotGiven = NOT_GIVEN,
        review_statuses: List[Literal["approved", "pending", "declined"]] | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        subscriptions: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAccessRequestsListResponse:
        """
        Use this API to get a list of event access requests that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_ids: Get requests with given applicationIds

          can_review: If set to true, return requests that the user can review

          created_bys: Get requests with the given createdBy user IDs

          event_ids: Get requests with given eventIds

          exclude_auto_approved_events: If set to true, exclude requests for auto-approved events

          ids: The request ids to get

          page_number: The page number to get.

          page_size: The number of requests to get per page.

          relationships: Get requests with the given relationships

          review_statuses: Get requests with the given review statuses

          sort: The sorting criteria for the returned results. You can sort the results by query
              parameter in ascending or descending order. Define the sort order using the
              following string: `fieldname:asc/desc` where:

              - `fieldname` — The field name of the query parameter to sort by.
              - `asc` — Sort the selected field name in ascending order.
              - `desc` — Sort the selected field name in descending order.

              If the direction is not specified, the default is ascending.

              You can use multiple query parameters to refine the sorting order.

          subscriptions: Get requests with the given subscriptions

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/v2/architecture/eventAccessRequests",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "application_ids": application_ids,
                        "can_review": can_review,
                        "created_bys": created_bys,
                        "event_ids": event_ids,
                        "exclude_auto_approved_events": exclude_auto_approved_events,
                        "ids": ids,
                        "page_number": page_number,
                        "page_size": page_size,
                        "relationships": relationships,
                        "review_statuses": review_statuses,
                        "sort": sort,
                        "subscriptions": subscriptions,
                    },
                    event_access_request_list_params.EventAccessRequestListParams,
                ),
            ),
            cast_to=EventAccessRequestsListResponse,
        )

    def approve(
        self,
        id: str,
        *,
        comments: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ReviewResponse:
        """Use this API to approve an event access request.

        A comment can be provided

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_request:review:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/api/v2/architecture/eventAccessRequests/{id}/approve",
            body=maybe_transform(
                {"comments": comments}, event_access_request_approve_params.EventAccessRequestApproveParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ReviewResponse,
        )

    def decline(
        self,
        id: str,
        *,
        comments: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ReviewResponse:
        """Use this API to decline an event access request.

        A comment can be provided

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_request:review:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/api/v2/architecture/eventAccessRequests/{id}/decline",
            body=maybe_transform(
                {"comments": comments}, event_access_request_decline_params.EventAccessRequestDeclineParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ReviewResponse,
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
    ) -> EventAccessRequestResponse:
        """
        Get event access request by id

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_request:get:*` **or**
        `event_access_request:review:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/api/v2/architecture/eventAccessRequests/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAccessRequestResponse,
        )

    async def update(
        self,
        id: str,
        *,
        comments: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAccessRequestResponse:
        """Use this API to update an event access request.

        You only need to specify the
        fields that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_request:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            f"/api/v2/architecture/eventAccessRequests/{id}",
            body=await async_maybe_transform(
                {"comments": comments}, event_access_request_update_params.EventAccessRequestUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAccessRequestResponse,
        )

    async def list(
        self,
        *,
        application_ids: List[str] | NotGiven = NOT_GIVEN,
        can_review: bool | NotGiven = NOT_GIVEN,
        created_bys: List[str] | NotGiven = NOT_GIVEN,
        event_ids: List[str] | NotGiven = NOT_GIVEN,
        exclude_auto_approved_events: bool | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        relationships: List[Literal["consuming", "producing"]] | NotGiven = NOT_GIVEN,
        review_statuses: List[Literal["approved", "pending", "declined"]] | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        subscriptions: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAccessRequestsListResponse:
        """
        Use this API to get a list of event access requests that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_ids: Get requests with given applicationIds

          can_review: If set to true, return requests that the user can review

          created_bys: Get requests with the given createdBy user IDs

          event_ids: Get requests with given eventIds

          exclude_auto_approved_events: If set to true, exclude requests for auto-approved events

          ids: The request ids to get

          page_number: The page number to get.

          page_size: The number of requests to get per page.

          relationships: Get requests with the given relationships

          review_statuses: Get requests with the given review statuses

          sort: The sorting criteria for the returned results. You can sort the results by query
              parameter in ascending or descending order. Define the sort order using the
              following string: `fieldname:asc/desc` where:

              - `fieldname` — The field name of the query parameter to sort by.
              - `asc` — Sort the selected field name in ascending order.
              - `desc` — Sort the selected field name in descending order.

              If the direction is not specified, the default is ascending.

              You can use multiple query parameters to refine the sorting order.

          subscriptions: Get requests with the given subscriptions

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/v2/architecture/eventAccessRequests",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "application_ids": application_ids,
                        "can_review": can_review,
                        "created_bys": created_bys,
                        "event_ids": event_ids,
                        "exclude_auto_approved_events": exclude_auto_approved_events,
                        "ids": ids,
                        "page_number": page_number,
                        "page_size": page_size,
                        "relationships": relationships,
                        "review_statuses": review_statuses,
                        "sort": sort,
                        "subscriptions": subscriptions,
                    },
                    event_access_request_list_params.EventAccessRequestListParams,
                ),
            ),
            cast_to=EventAccessRequestsListResponse,
        )

    async def approve(
        self,
        id: str,
        *,
        comments: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ReviewResponse:
        """Use this API to approve an event access request.

        A comment can be provided

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_request:review:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/api/v2/architecture/eventAccessRequests/{id}/approve",
            body=await async_maybe_transform(
                {"comments": comments}, event_access_request_approve_params.EventAccessRequestApproveParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ReviewResponse,
        )

    async def decline(
        self,
        id: str,
        *,
        comments: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ReviewResponse:
        """Use this API to decline an event access request.

        A comment can be provided

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_request:review:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/api/v2/architecture/eventAccessRequests/{id}/decline",
            body=await async_maybe_transform(
                {"comments": comments}, event_access_request_decline_params.EventAccessRequestDeclineParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ReviewResponse,
        )


class EventAccessRequestsResourceWithRawResponse:
    def __init__(self, event_access_requests: EventAccessRequestsResource) -> None:
        self._event_access_requests = event_access_requests

        self.retrieve = to_raw_response_wrapper(
            event_access_requests.retrieve,
        )
        self.update = to_raw_response_wrapper(
            event_access_requests.update,
        )
        self.list = to_raw_response_wrapper(
            event_access_requests.list,
        )
        self.approve = to_raw_response_wrapper(
            event_access_requests.approve,
        )
        self.decline = to_raw_response_wrapper(
            event_access_requests.decline,
        )


class AsyncEventAccessRequestsResourceWithRawResponse:
    def __init__(self, event_access_requests: AsyncEventAccessRequestsResource) -> None:
        self._event_access_requests = event_access_requests

        self.retrieve = async_to_raw_response_wrapper(
            event_access_requests.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            event_access_requests.update,
        )
        self.list = async_to_raw_response_wrapper(
            event_access_requests.list,
        )
        self.approve = async_to_raw_response_wrapper(
            event_access_requests.approve,
        )
        self.decline = async_to_raw_response_wrapper(
            event_access_requests.decline,
        )


class EventAccessRequestsResourceWithStreamingResponse:
    def __init__(self, event_access_requests: EventAccessRequestsResource) -> None:
        self._event_access_requests = event_access_requests

        self.retrieve = to_streamed_response_wrapper(
            event_access_requests.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            event_access_requests.update,
        )
        self.list = to_streamed_response_wrapper(
            event_access_requests.list,
        )
        self.approve = to_streamed_response_wrapper(
            event_access_requests.approve,
        )
        self.decline = to_streamed_response_wrapper(
            event_access_requests.decline,
        )


class AsyncEventAccessRequestsResourceWithStreamingResponse:
    def __init__(self, event_access_requests: AsyncEventAccessRequestsResource) -> None:
        self._event_access_requests = event_access_requests

        self.retrieve = async_to_streamed_response_wrapper(
            event_access_requests.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            event_access_requests.update,
        )
        self.list = async_to_streamed_response_wrapper(
            event_access_requests.list,
        )
        self.approve = async_to_streamed_response_wrapper(
            event_access_requests.approve,
        )
        self.decline = async_to_streamed_response_wrapper(
            event_access_requests.decline,
        )
