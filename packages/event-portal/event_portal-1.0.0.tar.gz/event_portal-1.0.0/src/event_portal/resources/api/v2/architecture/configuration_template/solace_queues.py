# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List

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
from ......_base_client import make_request_options
from ......types.api.v2.architecture.configuration_template import (
    solace_queue_list_params,
    solace_queue_create_params,
    solace_queue_update_params,
)
from ......types.api.v2.architecture.configuration_template.solace_queue_list_response import SolaceQueueListResponse
from ......types.api.v2.architecture.configuration_template.solace_queue_configuration_template_response import (
    SolaceQueueConfigurationTemplateResponse,
)

__all__ = ["SolaceQueuesResource", "AsyncSolaceQueuesResource"]


class SolaceQueuesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SolaceQueuesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return SolaceQueuesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SolaceQueuesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return SolaceQueuesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        description: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        value: Dict[str, object] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SolaceQueueConfigurationTemplateResponse:
        """
        Create a Solace queue configuration template to provide queue properties to
        Solace event brokers.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_configuration_template:create:*` ]

        Args:
          value: The configuration template in JSON format

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/architecture/configurationTemplate/solaceQueues",
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "type": type,
                    "value": value,
                },
                solace_queue_create_params.SolaceQueueCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SolaceQueueConfigurationTemplateResponse,
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
    ) -> SolaceQueueConfigurationTemplateResponse:
        """
        Get a Solace queue configuration template by its identifier.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_configuration_template:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/api/v2/architecture/configurationTemplate/solaceQueues/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SolaceQueueConfigurationTemplateResponse,
        )

    def update(
        self,
        id: str,
        *,
        description: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        value: Dict[str, object] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SolaceQueueConfigurationTemplateResponse:
        """
        Update a Solace queue configuration template.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_configuration_template:update:*` ]

        Args:
          value: The configuration template in JSON format

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            f"/api/v2/architecture/configurationTemplate/solaceQueues/{id}",
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "type": type,
                    "value": value,
                },
                solace_queue_update_params.SolaceQueueUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SolaceQueueConfigurationTemplateResponse,
        )

    def list(
        self,
        *,
        ids: List[str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SolaceQueueListResponse:
        """
        Get a list of Solace queue configuration templates that match the specified
        parameters.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          ids: The unique identifiers of the Solace queue configuration templates to retrieve,
              separated by commas.

          name: The name of the Solace queue configuration template to match.

          page_number: The page number to retrieve.

          page_size: The number of Solace queue configuration templates to return per page.

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
        return self._get(
            "/api/v2/architecture/configurationTemplate/solaceQueues",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "ids": ids,
                        "name": name,
                        "page_number": page_number,
                        "page_size": page_size,
                        "sort": sort,
                    },
                    solace_queue_list_params.SolaceQueueListParams,
                ),
            ),
            cast_to=SolaceQueueListResponse,
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
        Delete a Solace queue configuration template.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_configuration_template:delete:*` ]

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
            f"/api/v2/architecture/configurationTemplate/solaceQueues/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncSolaceQueuesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSolaceQueuesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSolaceQueuesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSolaceQueuesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncSolaceQueuesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        description: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        value: Dict[str, object] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SolaceQueueConfigurationTemplateResponse:
        """
        Create a Solace queue configuration template to provide queue properties to
        Solace event brokers.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_configuration_template:create:*` ]

        Args:
          value: The configuration template in JSON format

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/architecture/configurationTemplate/solaceQueues",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "type": type,
                    "value": value,
                },
                solace_queue_create_params.SolaceQueueCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SolaceQueueConfigurationTemplateResponse,
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
    ) -> SolaceQueueConfigurationTemplateResponse:
        """
        Get a Solace queue configuration template by its identifier.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_configuration_template:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/api/v2/architecture/configurationTemplate/solaceQueues/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SolaceQueueConfigurationTemplateResponse,
        )

    async def update(
        self,
        id: str,
        *,
        description: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        value: Dict[str, object] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SolaceQueueConfigurationTemplateResponse:
        """
        Update a Solace queue configuration template.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_configuration_template:update:*` ]

        Args:
          value: The configuration template in JSON format

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            f"/api/v2/architecture/configurationTemplate/solaceQueues/{id}",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "type": type,
                    "value": value,
                },
                solace_queue_update_params.SolaceQueueUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SolaceQueueConfigurationTemplateResponse,
        )

    async def list(
        self,
        *,
        ids: List[str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SolaceQueueListResponse:
        """
        Get a list of Solace queue configuration templates that match the specified
        parameters.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          ids: The unique identifiers of the Solace queue configuration templates to retrieve,
              separated by commas.

          name: The name of the Solace queue configuration template to match.

          page_number: The page number to retrieve.

          page_size: The number of Solace queue configuration templates to return per page.

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
        return await self._get(
            "/api/v2/architecture/configurationTemplate/solaceQueues",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "ids": ids,
                        "name": name,
                        "page_number": page_number,
                        "page_size": page_size,
                        "sort": sort,
                    },
                    solace_queue_list_params.SolaceQueueListParams,
                ),
            ),
            cast_to=SolaceQueueListResponse,
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
        Delete a Solace queue configuration template.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_configuration_template:delete:*` ]

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
            f"/api/v2/architecture/configurationTemplate/solaceQueues/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class SolaceQueuesResourceWithRawResponse:
    def __init__(self, solace_queues: SolaceQueuesResource) -> None:
        self._solace_queues = solace_queues

        self.create = to_raw_response_wrapper(
            solace_queues.create,
        )
        self.retrieve = to_raw_response_wrapper(
            solace_queues.retrieve,
        )
        self.update = to_raw_response_wrapper(
            solace_queues.update,
        )
        self.list = to_raw_response_wrapper(
            solace_queues.list,
        )
        self.delete = to_raw_response_wrapper(
            solace_queues.delete,
        )


class AsyncSolaceQueuesResourceWithRawResponse:
    def __init__(self, solace_queues: AsyncSolaceQueuesResource) -> None:
        self._solace_queues = solace_queues

        self.create = async_to_raw_response_wrapper(
            solace_queues.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            solace_queues.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            solace_queues.update,
        )
        self.list = async_to_raw_response_wrapper(
            solace_queues.list,
        )
        self.delete = async_to_raw_response_wrapper(
            solace_queues.delete,
        )


class SolaceQueuesResourceWithStreamingResponse:
    def __init__(self, solace_queues: SolaceQueuesResource) -> None:
        self._solace_queues = solace_queues

        self.create = to_streamed_response_wrapper(
            solace_queues.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            solace_queues.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            solace_queues.update,
        )
        self.list = to_streamed_response_wrapper(
            solace_queues.list,
        )
        self.delete = to_streamed_response_wrapper(
            solace_queues.delete,
        )


class AsyncSolaceQueuesResourceWithStreamingResponse:
    def __init__(self, solace_queues: AsyncSolaceQueuesResource) -> None:
        self._solace_queues = solace_queues

        self.create = async_to_streamed_response_wrapper(
            solace_queues.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            solace_queues.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            solace_queues.update,
        )
        self.list = async_to_streamed_response_wrapper(
            solace_queues.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            solace_queues.delete,
        )
