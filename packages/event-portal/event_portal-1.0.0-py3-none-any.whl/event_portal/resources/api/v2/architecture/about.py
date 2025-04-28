# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

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
    to_custom_raw_response_wrapper,
    to_custom_streamed_response_wrapper,
    async_to_custom_raw_response_wrapper,
    async_to_custom_streamed_response_wrapper,
)
from ....._base_client import make_request_options
from .....types.api.v2.architecture import about_list_applications_params

__all__ = ["AboutResource", "AsyncAboutResource"]


class AboutResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AboutResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AboutResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AboutResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AboutResourceWithStreamingResponse(self)

    def list_applications(
        self,
        *,
        ids: List[str] | NotGiven = NOT_GIVEN,
        name_contains: str | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BinaryAPIResponse:
        """
        Use this API to get a list of basic information for all applications.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:get_info:*` ]

        Args:
          ids: The unique identifiers of the applications to retrieve, separated by commas.

          page_number: The page number to retrieve.

          page_size: The number of items to return per page.

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
            "/api/v2/architecture/about/applications",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "name_contains": name_contains,
                        "page_number": page_number,
                        "page_size": page_size,
                        "sort": sort,
                    },
                    about_list_applications_params.AboutListApplicationsParams,
                ),
            ),
            cast_to=BinaryAPIResponse,
        )


class AsyncAboutResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAboutResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAboutResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAboutResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncAboutResourceWithStreamingResponse(self)

    async def list_applications(
        self,
        *,
        ids: List[str] | NotGiven = NOT_GIVEN,
        name_contains: str | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncBinaryAPIResponse:
        """
        Use this API to get a list of basic information for all applications.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:get_info:*` ]

        Args:
          ids: The unique identifiers of the applications to retrieve, separated by commas.

          page_number: The page number to retrieve.

          page_size: The number of items to return per page.

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
            "/api/v2/architecture/about/applications",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "name_contains": name_contains,
                        "page_number": page_number,
                        "page_size": page_size,
                        "sort": sort,
                    },
                    about_list_applications_params.AboutListApplicationsParams,
                ),
            ),
            cast_to=AsyncBinaryAPIResponse,
        )


class AboutResourceWithRawResponse:
    def __init__(self, about: AboutResource) -> None:
        self._about = about

        self.list_applications = to_custom_raw_response_wrapper(
            about.list_applications,
            BinaryAPIResponse,
        )


class AsyncAboutResourceWithRawResponse:
    def __init__(self, about: AsyncAboutResource) -> None:
        self._about = about

        self.list_applications = async_to_custom_raw_response_wrapper(
            about.list_applications,
            AsyncBinaryAPIResponse,
        )


class AboutResourceWithStreamingResponse:
    def __init__(self, about: AboutResource) -> None:
        self._about = about

        self.list_applications = to_custom_streamed_response_wrapper(
            about.list_applications,
            StreamedBinaryAPIResponse,
        )


class AsyncAboutResourceWithStreamingResponse:
    def __init__(self, about: AsyncAboutResource) -> None:
        self._about = about

        self.list_applications = async_to_custom_streamed_response_wrapper(
            about.list_applications,
            AsyncStreamedBinaryAPIResponse,
        )
