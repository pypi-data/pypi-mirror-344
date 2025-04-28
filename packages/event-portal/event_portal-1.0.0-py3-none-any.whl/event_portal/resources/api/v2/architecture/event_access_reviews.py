# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
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
    event_access_review_list_params,
    event_access_review_create_params,
    event_access_review_update_params,
)
from .....types.api.v2.architecture.review_response import ReviewResponse
from .....types.api.v2.architecture.event_access_review_list_response import EventAccessReviewListResponse

__all__ = ["EventAccessReviewsResource", "AsyncEventAccessReviewsResource"]


class EventAccessReviewsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EventAccessReviewsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return EventAccessReviewsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventAccessReviewsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return EventAccessReviewsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        decision: Literal["approved", "pending", "declined"],
        comments: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ReviewResponse:
        """
        Use this API to get a create an event access review.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_review:create:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/architecture/eventAccessReviews",
            body=maybe_transform(
                {
                    "decision": decision,
                    "comments": comments,
                },
                event_access_review_create_params.EventAccessReviewCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ReviewResponse,
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
    ) -> ReviewResponse:
        """
        Get event access review by id

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_review:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/api/v2/architecture/eventAccessReviews/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ReviewResponse,
        )

    def update(
        self,
        id: str,
        *,
        decision: Literal["approved", "pending", "declined"],
        comments: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ReviewResponse:
        """
        Use this API to update an event access review.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_review:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            f"/api/v2/architecture/eventAccessReviews/{id}",
            body=maybe_transform(
                {
                    "decision": decision,
                    "comments": comments,
                },
                event_access_review_update_params.EventAccessReviewUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ReviewResponse,
        )

    def list(
        self,
        *,
        decision: Literal["approved", "pending", "declined"] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        request_ids: List[str] | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        user_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAccessReviewListResponse:
        """
        Use this API to get a list of event access reviews that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          decision: Get reviews with the given decision

          ids: The review ids to get

          page_number: The page number to get.

          page_size: The number of events to get per page.

          request_ids: The request ids to get reviews for

          sort: The sorting criteria for the returned results. You can sort the results by query
              parameter in ascending or descending order. Define the sort order using the
              following string: `fieldname:asc/desc` where:

              - `fieldname` — The field name of the query parameter to sort by.
              - `asc` — Sort the selected field name in ascending order.
              - `desc` — Sort the selected field name in descending order.

              If the direction is not specified, the default is ascending.

              You can use multiple query parameters to refine the sorting order.

          user_id: Get reviews created by the given userId

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/v2/architecture/eventAccessReviews",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "decision": decision,
                        "ids": ids,
                        "page_number": page_number,
                        "page_size": page_size,
                        "request_ids": request_ids,
                        "sort": sort,
                        "user_id": user_id,
                    },
                    event_access_review_list_params.EventAccessReviewListParams,
                ),
            ),
            cast_to=EventAccessReviewListResponse,
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
        Use this API to delete an event access review

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_review:delete:*` ]

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
            f"/api/v2/architecture/eventAccessReviews/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncEventAccessReviewsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEventAccessReviewsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEventAccessReviewsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventAccessReviewsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncEventAccessReviewsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        decision: Literal["approved", "pending", "declined"],
        comments: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ReviewResponse:
        """
        Use this API to get a create an event access review.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_review:create:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/architecture/eventAccessReviews",
            body=await async_maybe_transform(
                {
                    "decision": decision,
                    "comments": comments,
                },
                event_access_review_create_params.EventAccessReviewCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ReviewResponse,
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
    ) -> ReviewResponse:
        """
        Get event access review by id

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_review:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/api/v2/architecture/eventAccessReviews/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ReviewResponse,
        )

    async def update(
        self,
        id: str,
        *,
        decision: Literal["approved", "pending", "declined"],
        comments: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ReviewResponse:
        """
        Use this API to update an event access review.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_review:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            f"/api/v2/architecture/eventAccessReviews/{id}",
            body=await async_maybe_transform(
                {
                    "decision": decision,
                    "comments": comments,
                },
                event_access_review_update_params.EventAccessReviewUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ReviewResponse,
        )

    async def list(
        self,
        *,
        decision: Literal["approved", "pending", "declined"] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        request_ids: List[str] | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        user_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAccessReviewListResponse:
        """
        Use this API to get a list of event access reviews that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          decision: Get reviews with the given decision

          ids: The review ids to get

          page_number: The page number to get.

          page_size: The number of events to get per page.

          request_ids: The request ids to get reviews for

          sort: The sorting criteria for the returned results. You can sort the results by query
              parameter in ascending or descending order. Define the sort order using the
              following string: `fieldname:asc/desc` where:

              - `fieldname` — The field name of the query parameter to sort by.
              - `asc` — Sort the selected field name in ascending order.
              - `desc` — Sort the selected field name in descending order.

              If the direction is not specified, the default is ascending.

              You can use multiple query parameters to refine the sorting order.

          user_id: Get reviews created by the given userId

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/v2/architecture/eventAccessReviews",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "decision": decision,
                        "ids": ids,
                        "page_number": page_number,
                        "page_size": page_size,
                        "request_ids": request_ids,
                        "sort": sort,
                        "user_id": user_id,
                    },
                    event_access_review_list_params.EventAccessReviewListParams,
                ),
            ),
            cast_to=EventAccessReviewListResponse,
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
        Use this API to delete an event access review

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_access_review:delete:*` ]

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
            f"/api/v2/architecture/eventAccessReviews/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class EventAccessReviewsResourceWithRawResponse:
    def __init__(self, event_access_reviews: EventAccessReviewsResource) -> None:
        self._event_access_reviews = event_access_reviews

        self.create = to_raw_response_wrapper(
            event_access_reviews.create,
        )
        self.retrieve = to_raw_response_wrapper(
            event_access_reviews.retrieve,
        )
        self.update = to_raw_response_wrapper(
            event_access_reviews.update,
        )
        self.list = to_raw_response_wrapper(
            event_access_reviews.list,
        )
        self.delete = to_raw_response_wrapper(
            event_access_reviews.delete,
        )


class AsyncEventAccessReviewsResourceWithRawResponse:
    def __init__(self, event_access_reviews: AsyncEventAccessReviewsResource) -> None:
        self._event_access_reviews = event_access_reviews

        self.create = async_to_raw_response_wrapper(
            event_access_reviews.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            event_access_reviews.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            event_access_reviews.update,
        )
        self.list = async_to_raw_response_wrapper(
            event_access_reviews.list,
        )
        self.delete = async_to_raw_response_wrapper(
            event_access_reviews.delete,
        )


class EventAccessReviewsResourceWithStreamingResponse:
    def __init__(self, event_access_reviews: EventAccessReviewsResource) -> None:
        self._event_access_reviews = event_access_reviews

        self.create = to_streamed_response_wrapper(
            event_access_reviews.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            event_access_reviews.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            event_access_reviews.update,
        )
        self.list = to_streamed_response_wrapper(
            event_access_reviews.list,
        )
        self.delete = to_streamed_response_wrapper(
            event_access_reviews.delete,
        )


class AsyncEventAccessReviewsResourceWithStreamingResponse:
    def __init__(self, event_access_reviews: AsyncEventAccessReviewsResource) -> None:
        self._event_access_reviews = event_access_reviews

        self.create = async_to_streamed_response_wrapper(
            event_access_reviews.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            event_access_reviews.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            event_access_reviews.update,
        )
        self.list = async_to_streamed_response_wrapper(
            event_access_reviews.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            event_access_reviews.delete,
        )
