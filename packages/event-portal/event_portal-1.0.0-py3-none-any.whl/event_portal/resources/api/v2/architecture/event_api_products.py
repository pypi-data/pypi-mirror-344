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
    event_api_product_list_params,
    event_api_product_create_params,
    event_api_product_update_params,
)
from .....types.api.v2.architecture.custom_attribute_param import CustomAttributeParam
from .....types.api.v2.architecture.event_api_product_response import EventAPIProductResponse
from .....types.api.v2.architecture.event_api_product_list_response import EventAPIProductListResponse

__all__ = ["EventAPIProductsResource", "AsyncEventAPIProductsResource"]


class EventAPIProductsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EventAPIProductsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return EventAPIProductsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventAPIProductsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return EventAPIProductsResourceWithStreamingResponse(self)

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
    ) -> EventAPIProductResponse:
        """
        Use this API to create an Event API Product.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:create:*` ]

        Args:
          broker_type: The type of the broker used for the event API product

          name: The name of the event API product

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/architecture/eventApiProducts",
            body=maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "broker_type": broker_type,
                    "custom_attributes": custom_attributes,
                    "name": name,
                    "shared": shared,
                },
                event_api_product_create_params.EventAPIProductCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIProductResponse,
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
    ) -> EventAPIProductResponse:
        """
        Use this API to get a single Event API Product by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/api/v2/architecture/eventApiProducts/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIProductResponse,
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
    ) -> EventAPIProductResponse:
        """Use this API to update an Event API Product.

        You only need to specify the fields
        that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update:*` ]

        Args:
          broker_type: The type of the broker used for the event API product

          name: The name of the event API product

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._patch(
            f"/api/v2/architecture/eventApiProducts/{id}",
            body=maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "broker_type": broker_type,
                    "custom_attributes": custom_attributes,
                    "name": name,
                    "shared": shared,
                },
                event_api_product_update_params.EventAPIProductUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIProductResponse,
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
    ) -> EventAPIProductListResponse:
        """
        Use this API to get a list of Event API Products that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_domain_id: Match only Event API Products in the given application domain.

          application_domain_ids: Match only Event API Products in the given application domains.

          broker_type: Match only Event API Products with the given broken type.

          custom_attributes: Returns the entities that match the custom attribute filter. To filter by custom
              attribute name and value, use the format:
              `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
              by custom attribute name, use the format:
              `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
              operator for multiple custom attribute definitions (not multiple values for a
              given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
              operation. Note: the filter supports custom attribute values containing only the
              characters `[a-zA-Z0-9_\\--\\.. ]`.

          ids: Match only Event API Products with the given IDs separated by commas.

          name: Name of the Event API Product to match on.

          page_number: The page number to get.

          page_size: The number of Event API Products to get per page.

          shared: Match only with shared or unshared Event API Products.

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
            "/api/v2/architecture/eventApiProducts",
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
                    event_api_product_list_params.EventAPIProductListParams,
                ),
            ),
            cast_to=EventAPIProductListResponse,
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
        Use this API to delete an Event API Product.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:delete:*` ]

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
            f"/api/v2/architecture/eventApiProducts/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncEventAPIProductsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEventAPIProductsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEventAPIProductsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventAPIProductsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncEventAPIProductsResourceWithStreamingResponse(self)

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
    ) -> EventAPIProductResponse:
        """
        Use this API to create an Event API Product.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:create:*` ]

        Args:
          broker_type: The type of the broker used for the event API product

          name: The name of the event API product

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/architecture/eventApiProducts",
            body=await async_maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "broker_type": broker_type,
                    "custom_attributes": custom_attributes,
                    "name": name,
                    "shared": shared,
                },
                event_api_product_create_params.EventAPIProductCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIProductResponse,
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
    ) -> EventAPIProductResponse:
        """
        Use this API to get a single Event API Product by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/api/v2/architecture/eventApiProducts/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIProductResponse,
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
    ) -> EventAPIProductResponse:
        """Use this API to update an Event API Product.

        You only need to specify the fields
        that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update:*` ]

        Args:
          broker_type: The type of the broker used for the event API product

          name: The name of the event API product

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._patch(
            f"/api/v2/architecture/eventApiProducts/{id}",
            body=await async_maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "broker_type": broker_type,
                    "custom_attributes": custom_attributes,
                    "name": name,
                    "shared": shared,
                },
                event_api_product_update_params.EventAPIProductUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIProductResponse,
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
    ) -> EventAPIProductListResponse:
        """
        Use this API to get a list of Event API Products that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_domain_id: Match only Event API Products in the given application domain.

          application_domain_ids: Match only Event API Products in the given application domains.

          broker_type: Match only Event API Products with the given broken type.

          custom_attributes: Returns the entities that match the custom attribute filter. To filter by custom
              attribute name and value, use the format:
              `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
              by custom attribute name, use the format:
              `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
              operator for multiple custom attribute definitions (not multiple values for a
              given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
              operation. Note: the filter supports custom attribute values containing only the
              characters `[a-zA-Z0-9_\\--\\.. ]`.

          ids: Match only Event API Products with the given IDs separated by commas.

          name: Name of the Event API Product to match on.

          page_number: The page number to get.

          page_size: The number of Event API Products to get per page.

          shared: Match only with shared or unshared Event API Products.

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
            "/api/v2/architecture/eventApiProducts",
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
                    event_api_product_list_params.EventAPIProductListParams,
                ),
            ),
            cast_to=EventAPIProductListResponse,
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
        Use this API to delete an Event API Product.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:delete:*` ]

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
            f"/api/v2/architecture/eventApiProducts/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class EventAPIProductsResourceWithRawResponse:
    def __init__(self, event_api_products: EventAPIProductsResource) -> None:
        self._event_api_products = event_api_products

        self.create = to_raw_response_wrapper(
            event_api_products.create,
        )
        self.retrieve = to_raw_response_wrapper(
            event_api_products.retrieve,
        )
        self.update = to_raw_response_wrapper(
            event_api_products.update,
        )
        self.list = to_raw_response_wrapper(
            event_api_products.list,
        )
        self.delete = to_raw_response_wrapper(
            event_api_products.delete,
        )


class AsyncEventAPIProductsResourceWithRawResponse:
    def __init__(self, event_api_products: AsyncEventAPIProductsResource) -> None:
        self._event_api_products = event_api_products

        self.create = async_to_raw_response_wrapper(
            event_api_products.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            event_api_products.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            event_api_products.update,
        )
        self.list = async_to_raw_response_wrapper(
            event_api_products.list,
        )
        self.delete = async_to_raw_response_wrapper(
            event_api_products.delete,
        )


class EventAPIProductsResourceWithStreamingResponse:
    def __init__(self, event_api_products: EventAPIProductsResource) -> None:
        self._event_api_products = event_api_products

        self.create = to_streamed_response_wrapper(
            event_api_products.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            event_api_products.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            event_api_products.update,
        )
        self.list = to_streamed_response_wrapper(
            event_api_products.list,
        )
        self.delete = to_streamed_response_wrapper(
            event_api_products.delete,
        )


class AsyncEventAPIProductsResourceWithStreamingResponse:
    def __init__(self, event_api_products: AsyncEventAPIProductsResource) -> None:
        self._event_api_products = event_api_products

        self.create = async_to_streamed_response_wrapper(
            event_api_products.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            event_api_products.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            event_api_products.update,
        )
        self.list = async_to_streamed_response_wrapper(
            event_api_products.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            event_api_products.delete,
        )
