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
from .....types.api.v2.architecture import event_api_list_params, event_api_create_params, event_api_update_params
from .....types.api.v2.architecture.event_api_response import EventAPIResponse
from .....types.api.v2.architecture.custom_attribute_param import CustomAttributeParam
from .....types.api.v2.architecture.event_api_list_response import EventAPIListResponse

__all__ = ["EventAPIsResource", "AsyncEventAPIsResource"]


class EventAPIsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EventAPIsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return EventAPIsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventAPIsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return EventAPIsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        application_domain_id: str | NotGiven = NOT_GIVEN,
        broker_type: Literal["kafka", "solace"] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIResponse:
        """
        Use this API to create an event API.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:create:*` ]

        Args:
          broker_type: The type of the broker used for the event API

          name: The name of the event api.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/architecture/eventApis",
            body=maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "broker_type": broker_type,
                    "custom_attributes": custom_attributes,
                    "name": name,
                    "shared": shared,
                },
                event_api_create_params.EventAPICreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIResponse,
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
    ) -> EventAPIResponse:
        """
        Use this API to get a single event API by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/api/v2/architecture/eventApis/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIResponse,
        )

    def update(
        self,
        id: str,
        *,
        application_domain_id: str | NotGiven = NOT_GIVEN,
        broker_type: Literal["kafka", "solace"] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIResponse:
        """Use this API to update an event API.

        You only need to specify the fields that
        need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:update:*` ]

        Args:
          broker_type: The type of the broker used for the event API

          name: The name of the event api.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            f"/api/v2/architecture/eventApis/{id}",
            body=maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "broker_type": broker_type,
                    "custom_attributes": custom_attributes,
                    "name": name,
                    "shared": shared,
                },
                event_api_update_params.EventAPIUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIResponse,
        )

    def list(
        self,
        *,
        application_domain_id: str | NotGiven = NOT_GIVEN,
        application_domain_ids: List[str] | NotGiven = NOT_GIVEN,
        available_within_application_domain_ids: bool | NotGiven = NOT_GIVEN,
        broker_type: str | NotGiven = NOT_GIVEN,
        custom_attributes: str | NotGiven = NOT_GIVEN,
        event_api_version_ids: List[str] | NotGiven = NOT_GIVEN,
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
    ) -> EventAPIListResponse:
        """
        Use this API to get a list of event APIs that match the given parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_domain_id: Match only event APIs in the given application domain.

          application_domain_ids: Match only event APIs in the given application domains.

          available_within_application_domain_ids: Additionally match any shared event APIs in any application domain.

          broker_type: Match only event APIs with the given broker type.

          custom_attributes: Returns the entities that match the custom attribute filter. To filter by custom
              attribute name and value, use the format:
              `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
              by custom attribute name, use the format:
              `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
              operator for multiple custom attribute definitions (not multiple values for a
              given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
              operation. Note: the filter supports custom attribute values containing only the
              characters `[a-zA-Z0-9_\\--\\.. ]`.

          event_api_version_ids: Match only event APIs in the given event API version ids.

          ids: Match only event APIs with the given IDs separated by commas.

          name: Name of the event API to match on.

          page_number: The page number to get.

          page_size: The number of event APIs to get per page.

          shared: Match only with shared or unshared event APIs.

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
            "/api/v2/architecture/eventApis",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "application_domain_id": application_domain_id,
                        "application_domain_ids": application_domain_ids,
                        "available_within_application_domain_ids": available_within_application_domain_ids,
                        "broker_type": broker_type,
                        "custom_attributes": custom_attributes,
                        "event_api_version_ids": event_api_version_ids,
                        "ids": ids,
                        "name": name,
                        "page_number": page_number,
                        "page_size": page_size,
                        "shared": shared,
                        "sort": sort,
                    },
                    event_api_list_params.EventAPIListParams,
                ),
            ),
            cast_to=EventAPIListResponse,
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
        Use this API to delete an event API.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:delete:*` ]

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
            f"/api/v2/architecture/eventApis/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncEventAPIsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEventAPIsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEventAPIsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventAPIsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncEventAPIsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        application_domain_id: str | NotGiven = NOT_GIVEN,
        broker_type: Literal["kafka", "solace"] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIResponse:
        """
        Use this API to create an event API.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:create:*` ]

        Args:
          broker_type: The type of the broker used for the event API

          name: The name of the event api.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/architecture/eventApis",
            body=await async_maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "broker_type": broker_type,
                    "custom_attributes": custom_attributes,
                    "name": name,
                    "shared": shared,
                },
                event_api_create_params.EventAPICreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIResponse,
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
    ) -> EventAPIResponse:
        """
        Use this API to get a single event API by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/api/v2/architecture/eventApis/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIResponse,
        )

    async def update(
        self,
        id: str,
        *,
        application_domain_id: str | NotGiven = NOT_GIVEN,
        broker_type: Literal["kafka", "solace"] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIResponse:
        """Use this API to update an event API.

        You only need to specify the fields that
        need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:update:*` ]

        Args:
          broker_type: The type of the broker used for the event API

          name: The name of the event api.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            f"/api/v2/architecture/eventApis/{id}",
            body=await async_maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "broker_type": broker_type,
                    "custom_attributes": custom_attributes,
                    "name": name,
                    "shared": shared,
                },
                event_api_update_params.EventAPIUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIResponse,
        )

    async def list(
        self,
        *,
        application_domain_id: str | NotGiven = NOT_GIVEN,
        application_domain_ids: List[str] | NotGiven = NOT_GIVEN,
        available_within_application_domain_ids: bool | NotGiven = NOT_GIVEN,
        broker_type: str | NotGiven = NOT_GIVEN,
        custom_attributes: str | NotGiven = NOT_GIVEN,
        event_api_version_ids: List[str] | NotGiven = NOT_GIVEN,
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
    ) -> EventAPIListResponse:
        """
        Use this API to get a list of event APIs that match the given parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_domain_id: Match only event APIs in the given application domain.

          application_domain_ids: Match only event APIs in the given application domains.

          available_within_application_domain_ids: Additionally match any shared event APIs in any application domain.

          broker_type: Match only event APIs with the given broker type.

          custom_attributes: Returns the entities that match the custom attribute filter. To filter by custom
              attribute name and value, use the format:
              `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
              by custom attribute name, use the format:
              `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
              operator for multiple custom attribute definitions (not multiple values for a
              given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
              operation. Note: the filter supports custom attribute values containing only the
              characters `[a-zA-Z0-9_\\--\\.. ]`.

          event_api_version_ids: Match only event APIs in the given event API version ids.

          ids: Match only event APIs with the given IDs separated by commas.

          name: Name of the event API to match on.

          page_number: The page number to get.

          page_size: The number of event APIs to get per page.

          shared: Match only with shared or unshared event APIs.

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
            "/api/v2/architecture/eventApis",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "application_domain_id": application_domain_id,
                        "application_domain_ids": application_domain_ids,
                        "available_within_application_domain_ids": available_within_application_domain_ids,
                        "broker_type": broker_type,
                        "custom_attributes": custom_attributes,
                        "event_api_version_ids": event_api_version_ids,
                        "ids": ids,
                        "name": name,
                        "page_number": page_number,
                        "page_size": page_size,
                        "shared": shared,
                        "sort": sort,
                    },
                    event_api_list_params.EventAPIListParams,
                ),
            ),
            cast_to=EventAPIListResponse,
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
        Use this API to delete an event API.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:delete:*` ]

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
            f"/api/v2/architecture/eventApis/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class EventAPIsResourceWithRawResponse:
    def __init__(self, event_apis: EventAPIsResource) -> None:
        self._event_apis = event_apis

        self.create = to_raw_response_wrapper(
            event_apis.create,
        )
        self.retrieve = to_raw_response_wrapper(
            event_apis.retrieve,
        )
        self.update = to_raw_response_wrapper(
            event_apis.update,
        )
        self.list = to_raw_response_wrapper(
            event_apis.list,
        )
        self.delete = to_raw_response_wrapper(
            event_apis.delete,
        )


class AsyncEventAPIsResourceWithRawResponse:
    def __init__(self, event_apis: AsyncEventAPIsResource) -> None:
        self._event_apis = event_apis

        self.create = async_to_raw_response_wrapper(
            event_apis.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            event_apis.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            event_apis.update,
        )
        self.list = async_to_raw_response_wrapper(
            event_apis.list,
        )
        self.delete = async_to_raw_response_wrapper(
            event_apis.delete,
        )


class EventAPIsResourceWithStreamingResponse:
    def __init__(self, event_apis: EventAPIsResource) -> None:
        self._event_apis = event_apis

        self.create = to_streamed_response_wrapper(
            event_apis.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            event_apis.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            event_apis.update,
        )
        self.list = to_streamed_response_wrapper(
            event_apis.list,
        )
        self.delete = to_streamed_response_wrapper(
            event_apis.delete,
        )


class AsyncEventAPIsResourceWithStreamingResponse:
    def __init__(self, event_apis: AsyncEventAPIsResource) -> None:
        self._event_apis = event_apis

        self.create = async_to_streamed_response_wrapper(
            event_apis.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            event_apis.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            event_apis.update,
        )
        self.list = async_to_streamed_response_wrapper(
            event_apis.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            event_apis.delete,
        )
