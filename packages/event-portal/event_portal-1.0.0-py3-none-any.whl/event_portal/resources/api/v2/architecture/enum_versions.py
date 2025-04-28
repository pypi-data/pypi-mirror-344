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
from .....types.api.v2.architecture import (
    enum_version_list_params,
    enum_version_create_params,
    enum_version_update_params,
    enum_version_update_state_params,
)
from .....types.api.v2.architecture.custom_attribute_param import CustomAttributeParam
from .....types.api.v2.architecture.enum_version_list_response import EnumVersionListResponse
from .....types.api.v2.architecture.state_change_request_response import StateChangeRequestResponse
from .....types.api.v2.architecture.topic_address_enum_version_response import TopicAddressEnumVersionResponse

__all__ = ["EnumVersionsResource", "AsyncEnumVersionsResource"]


class EnumVersionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> EnumVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return EnumVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EnumVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return EnumVersionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        enum_id: str,
        values: Iterable[enum_version_create_params.Value],
        version: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TopicAddressEnumVersionResponse:
        """
        Create an enumeration version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_enum:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._post(
            "/api/v2/architecture/enumVersions",
            body=maybe_transform(
                {
                    "enum_id": enum_id,
                    "values": values,
                    "version": version,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                },
                enum_version_create_params.EnumVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicAddressEnumVersionResponse,
        )

    def retrieve(
        self,
        version_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TopicAddressEnumVersionResponse:
        """
        Use this API to get a single enumeration version by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_enum:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            f"/api/v2/architecture/enumVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicAddressEnumVersionResponse,
        )

    def update(
        self,
        id: str,
        *,
        enum_id: str,
        values: Iterable[enum_version_update_params.Value],
        version: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TopicAddressEnumVersionResponse:
        """Use this API to update an enumeration version.

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
            f"/api/v2/architecture/enumVersions/{id}",
            body=maybe_transform(
                {
                    "enum_id": enum_id,
                    "values": values,
                    "version": version,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                },
                enum_version_update_params.EnumVersionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicAddressEnumVersionResponse,
        )

    def list(
        self,
        *,
        enum_ids: List[str] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EnumVersionListResponse:
        """
        Use this API to get a list of enumeration versions that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          enum_ids: Match only enumeration versions of these enumeration IDs, separated by commas.

          ids: Match only enumeration versions with the given IDs, separated by commas.

          page_number: The page number to get.

          page_size: The number of enumeration versions to get per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            "/api/v2/architecture/enumVersions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "enum_ids": enum_ids,
                        "ids": ids,
                        "page_number": page_number,
                        "page_size": page_size,
                    },
                    enum_version_list_params.EnumVersionListParams,
                ),
            ),
            cast_to=EnumVersionListResponse,
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
        """Use this API to delete an enumeration version.

        The version must not be in use by
        any events else it cannot be deleted. This also deletes the version's values.

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
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v2/architecture/enumVersions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def update_state(
        self,
        id: str,
        *,
        state_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StateChangeRequestResponse:
        """Use this API to update the state of an enumeration version.

        You only need to
        specify the target stateId field.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_enum:update_state:*` ]

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
            f"/api/v2/architecture/enumVersions/{id}/state",
            body=maybe_transform({"state_id": state_id}, enum_version_update_state_params.EnumVersionUpdateStateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StateChangeRequestResponse,
        )


class AsyncEnumVersionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncEnumVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEnumVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEnumVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncEnumVersionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        enum_id: str,
        values: Iterable[enum_version_create_params.Value],
        version: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TopicAddressEnumVersionResponse:
        """
        Create an enumeration version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_enum:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._post(
            "/api/v2/architecture/enumVersions",
            body=await async_maybe_transform(
                {
                    "enum_id": enum_id,
                    "values": values,
                    "version": version,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                },
                enum_version_create_params.EnumVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicAddressEnumVersionResponse,
        )

    async def retrieve(
        self,
        version_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TopicAddressEnumVersionResponse:
        """
        Use this API to get a single enumeration version by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_enum:get:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            f"/api/v2/architecture/enumVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicAddressEnumVersionResponse,
        )

    async def update(
        self,
        id: str,
        *,
        enum_id: str,
        values: Iterable[enum_version_update_params.Value],
        version: str,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> TopicAddressEnumVersionResponse:
        """Use this API to update an enumeration version.

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
            f"/api/v2/architecture/enumVersions/{id}",
            body=await async_maybe_transform(
                {
                    "enum_id": enum_id,
                    "values": values,
                    "version": version,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                },
                enum_version_update_params.EnumVersionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=TopicAddressEnumVersionResponse,
        )

    async def list(
        self,
        *,
        enum_ids: List[str] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EnumVersionListResponse:
        """
        Use this API to get a list of enumeration versions that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          enum_ids: Match only enumeration versions of these enumeration IDs, separated by commas.

          ids: Match only enumeration versions with the given IDs, separated by commas.

          page_number: The page number to get.

          page_size: The number of enumeration versions to get per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            "/api/v2/architecture/enumVersions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "enum_ids": enum_ids,
                        "ids": ids,
                        "page_number": page_number,
                        "page_size": page_size,
                    },
                    enum_version_list_params.EnumVersionListParams,
                ),
            ),
            cast_to=EnumVersionListResponse,
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
        """Use this API to delete an enumeration version.

        The version must not be in use by
        any events else it cannot be deleted. This also deletes the version's values.

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
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v2/architecture/enumVersions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def update_state(
        self,
        id: str,
        *,
        state_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StateChangeRequestResponse:
        """Use this API to update the state of an enumeration version.

        You only need to
        specify the target stateId field.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_enum:update_state:*` ]

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
            f"/api/v2/architecture/enumVersions/{id}/state",
            body=await async_maybe_transform(
                {"state_id": state_id}, enum_version_update_state_params.EnumVersionUpdateStateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StateChangeRequestResponse,
        )


class EnumVersionsResourceWithRawResponse:
    def __init__(self, enum_versions: EnumVersionsResource) -> None:
        self._enum_versions = enum_versions

        self.create = to_raw_response_wrapper(
            enum_versions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            enum_versions.retrieve,
        )
        self.update = to_raw_response_wrapper(
            enum_versions.update,
        )
        self.list = to_raw_response_wrapper(
            enum_versions.list,
        )
        self.delete = to_raw_response_wrapper(
            enum_versions.delete,
        )
        self.update_state = to_raw_response_wrapper(
            enum_versions.update_state,
        )


class AsyncEnumVersionsResourceWithRawResponse:
    def __init__(self, enum_versions: AsyncEnumVersionsResource) -> None:
        self._enum_versions = enum_versions

        self.create = async_to_raw_response_wrapper(
            enum_versions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            enum_versions.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            enum_versions.update,
        )
        self.list = async_to_raw_response_wrapper(
            enum_versions.list,
        )
        self.delete = async_to_raw_response_wrapper(
            enum_versions.delete,
        )
        self.update_state = async_to_raw_response_wrapper(
            enum_versions.update_state,
        )


class EnumVersionsResourceWithStreamingResponse:
    def __init__(self, enum_versions: EnumVersionsResource) -> None:
        self._enum_versions = enum_versions

        self.create = to_streamed_response_wrapper(
            enum_versions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            enum_versions.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            enum_versions.update,
        )
        self.list = to_streamed_response_wrapper(
            enum_versions.list,
        )
        self.delete = to_streamed_response_wrapper(
            enum_versions.delete,
        )
        self.update_state = to_streamed_response_wrapper(
            enum_versions.update_state,
        )


class AsyncEnumVersionsResourceWithStreamingResponse:
    def __init__(self, enum_versions: AsyncEnumVersionsResource) -> None:
        self._enum_versions = enum_versions

        self.create = async_to_streamed_response_wrapper(
            enum_versions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            enum_versions.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            enum_versions.update,
        )
        self.list = async_to_streamed_response_wrapper(
            enum_versions.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            enum_versions.delete,
        )
        self.update_state = async_to_streamed_response_wrapper(
            enum_versions.update_state,
        )
