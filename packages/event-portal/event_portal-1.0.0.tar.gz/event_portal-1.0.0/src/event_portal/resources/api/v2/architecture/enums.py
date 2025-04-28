# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable

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
from .....types.api.v2.architecture import enum_list_params, enum_create_params, enum_update_params
from .....types.api.v2.architecture.enum_list_response import EnumListResponse
from .....types.api.v2.architecture.custom_attribute_param import CustomAttributeParam
from .....types.api.v2.architecture.topic_address_enum_response import TopicAddressEnumResponse

__all__ = ["EnumsResource", "AsyncEnumsResource"]


class EnumsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EnumsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return EnumsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EnumsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return EnumsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        application_domain_id: str,
        name: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TopicAddressEnumResponse:
        """An enumeration is a bounded variable with a limited set of literal values.

        Use
        this API to create an enumeration to define acceptable values for a level in a
        topic address or topic domain.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_enum:create:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._post(
            "/api/v2/architecture/enums",
            body=maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "name": name,
                    "custom_attributes": custom_attributes,
                    "shared": shared,
                },
                enum_create_params.EnumCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicAddressEnumResponse,
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
    ) -> TopicAddressEnumResponse:
        """
        Use this API to get a single enumeration by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_enum:get:*` ]

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
            f"/api/v2/architecture/enums/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicAddressEnumResponse,
        )

    def update(
        self,
        id: str,
        *,
        application_domain_id: str,
        name: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TopicAddressEnumResponse:
        """Use this API to update an enumeration object.

        You only need to specify the
        fields that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_enum:update:*` ]

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
            f"/api/v2/architecture/enums/{id}",
            body=maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "name": name,
                    "custom_attributes": custom_attributes,
                    "shared": shared,
                },
                enum_update_params.EnumUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicAddressEnumResponse,
        )

    def list(
        self,
        *,
        application_domain_id: str | NotGiven = NOT_GIVEN,
        application_domain_ids: List[str] | NotGiven = NOT_GIVEN,
        custom_attributes: str | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        names: List[str] | NotGiven = NOT_GIVEN,
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
    ) -> EnumListResponse:
        """
        Use this API to get a list of enumerations based on certain criteria.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_domain_id: The application domain ID of the enumerations.

          application_domain_ids: Match only enumerations in the given application domain ids.

          custom_attributes: Returns the entities that match the custom attribute filter. To filter by custom
              attribute name and value, use the format:
              `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
              by custom attribute name, use the format:
              `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
              operator for multiple custom attribute definitions (not multiple values for a
              given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
              operation. Note: the filter supports custom attribute values containing only the
              characters `[a-zA-Z0-9_\\--\\.. ]`.

          ids: The IDs of the enumerations.

          names: The names of the enumerations.

          page_number: The page number to get.

          page_size: The number of enumerations to get per page.

          shared: Match only with shared or unshared enumerations.

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
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            "/api/v2/architecture/enums",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "application_domain_id": application_domain_id,
                        "application_domain_ids": application_domain_ids,
                        "custom_attributes": custom_attributes,
                        "ids": ids,
                        "names": names,
                        "page_number": page_number,
                        "page_size": page_size,
                        "shared": shared,
                        "sort": sort,
                    },
                    enum_list_params.EnumListParams,
                ),
            ),
            cast_to=EnumListResponse,
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
        """Use this API to delete an enumeration.

        The enumeration must not have any
        versions or else it cannot be deleted.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_enum:delete:*` ]

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
            f"/api/v2/architecture/enums/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncEnumsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEnumsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEnumsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEnumsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncEnumsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        application_domain_id: str,
        name: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TopicAddressEnumResponse:
        """An enumeration is a bounded variable with a limited set of literal values.

        Use
        this API to create an enumeration to define acceptable values for a level in a
        topic address or topic domain.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_enum:create:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._post(
            "/api/v2/architecture/enums",
            body=await async_maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "name": name,
                    "custom_attributes": custom_attributes,
                    "shared": shared,
                },
                enum_create_params.EnumCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicAddressEnumResponse,
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
    ) -> TopicAddressEnumResponse:
        """
        Use this API to get a single enumeration by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_enum:get:*` ]

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
            f"/api/v2/architecture/enums/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicAddressEnumResponse,
        )

    async def update(
        self,
        id: str,
        *,
        application_domain_id: str,
        name: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        shared: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TopicAddressEnumResponse:
        """Use this API to update an enumeration object.

        You only need to specify the
        fields that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_enum:update:*` ]

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
            f"/api/v2/architecture/enums/{id}",
            body=await async_maybe_transform(
                {
                    "application_domain_id": application_domain_id,
                    "name": name,
                    "custom_attributes": custom_attributes,
                    "shared": shared,
                },
                enum_update_params.EnumUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicAddressEnumResponse,
        )

    async def list(
        self,
        *,
        application_domain_id: str | NotGiven = NOT_GIVEN,
        application_domain_ids: List[str] | NotGiven = NOT_GIVEN,
        custom_attributes: str | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        names: List[str] | NotGiven = NOT_GIVEN,
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
    ) -> EnumListResponse:
        """
        Use this API to get a list of enumerations based on certain criteria.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          application_domain_id: The application domain ID of the enumerations.

          application_domain_ids: Match only enumerations in the given application domain ids.

          custom_attributes: Returns the entities that match the custom attribute filter. To filter by custom
              attribute name and value, use the format:
              `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
              by custom attribute name, use the format:
              `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
              operator for multiple custom attribute definitions (not multiple values for a
              given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
              operation. Note: the filter supports custom attribute values containing only the
              characters `[a-zA-Z0-9_\\--\\.. ]`.

          ids: The IDs of the enumerations.

          names: The names of the enumerations.

          page_number: The page number to get.

          page_size: The number of enumerations to get per page.

          shared: Match only with shared or unshared enumerations.

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
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            "/api/v2/architecture/enums",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "application_domain_id": application_domain_id,
                        "application_domain_ids": application_domain_ids,
                        "custom_attributes": custom_attributes,
                        "ids": ids,
                        "names": names,
                        "page_number": page_number,
                        "page_size": page_size,
                        "shared": shared,
                        "sort": sort,
                    },
                    enum_list_params.EnumListParams,
                ),
            ),
            cast_to=EnumListResponse,
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
        """Use this API to delete an enumeration.

        The enumeration must not have any
        versions or else it cannot be deleted.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_enum:delete:*` ]

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
            f"/api/v2/architecture/enums/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class EnumsResourceWithRawResponse:
    def __init__(self, enums: EnumsResource) -> None:
        self._enums = enums

        self.create = to_raw_response_wrapper(
            enums.create,
        )
        self.retrieve = to_raw_response_wrapper(
            enums.retrieve,
        )
        self.update = to_raw_response_wrapper(
            enums.update,
        )
        self.list = to_raw_response_wrapper(
            enums.list,
        )
        self.delete = to_raw_response_wrapper(
            enums.delete,
        )


class AsyncEnumsResourceWithRawResponse:
    def __init__(self, enums: AsyncEnumsResource) -> None:
        self._enums = enums

        self.create = async_to_raw_response_wrapper(
            enums.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            enums.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            enums.update,
        )
        self.list = async_to_raw_response_wrapper(
            enums.list,
        )
        self.delete = async_to_raw_response_wrapper(
            enums.delete,
        )


class EnumsResourceWithStreamingResponse:
    def __init__(self, enums: EnumsResource) -> None:
        self._enums = enums

        self.create = to_streamed_response_wrapper(
            enums.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            enums.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            enums.update,
        )
        self.list = to_streamed_response_wrapper(
            enums.list,
        )
        self.delete = to_streamed_response_wrapper(
            enums.delete,
        )


class AsyncEnumsResourceWithStreamingResponse:
    def __init__(self, enums: AsyncEnumsResource) -> None:
        self._enums = enums

        self.create = async_to_streamed_response_wrapper(
            enums.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            enums.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            enums.update,
        )
        self.list = async_to_streamed_response_wrapper(
            enums.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            enums.delete,
        )
