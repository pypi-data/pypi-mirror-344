# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List

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
from .....types.api.v2.architecture import configuration_type_list_params
from .....types.api.v2.architecture.configuration_type_list_response import ConfigurationTypeListResponse
from .....types.api.v2.architecture.configuration_type_retrieve_response import ConfigurationTypeRetrieveResponse

__all__ = ["ConfigurationTypesResource", "AsyncConfigurationTypesResource"]


class ConfigurationTypesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ConfigurationTypesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return ConfigurationTypesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConfigurationTypesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return ConfigurationTypesResourceWithStreamingResponse(self)

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
    ) -> ConfigurationTypeRetrieveResponse:
        """
        Use this API to get a single configuration type by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_configuration:read` ]

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
            f"/api/v2/architecture/configurationTypes/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigurationTypeRetrieveResponse,
        )

    def list(
        self,
        *,
        associated_entity_types: List[str] | NotGiven = NOT_GIVEN,
        broker_type: str | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        names: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigurationTypeListResponse:
        """
        Use this API to get a list of configuration types that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_configuration:read` ]

        Args:
          associated_entity_types: Match only configuration types with the given associated entity type values
              separated by commas.

          broker_type: Match only configuration types with the given broker type.

          ids: Match only configuration types with the given IDs separated by commas.

          names: Match only configuration types with the given names separated by commas.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            "/api/v2/architecture/configurationTypes",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "associated_entity_types": associated_entity_types,
                        "broker_type": broker_type,
                        "ids": ids,
                        "names": names,
                    },
                    configuration_type_list_params.ConfigurationTypeListParams,
                ),
            ),
            cast_to=ConfigurationTypeListResponse,
        )


class AsyncConfigurationTypesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncConfigurationTypesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConfigurationTypesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConfigurationTypesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncConfigurationTypesResourceWithStreamingResponse(self)

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
    ) -> ConfigurationTypeRetrieveResponse:
        """
        Use this API to get a single configuration type by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_configuration:read` ]

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
            f"/api/v2/architecture/configurationTypes/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigurationTypeRetrieveResponse,
        )

    async def list(
        self,
        *,
        associated_entity_types: List[str] | NotGiven = NOT_GIVEN,
        broker_type: str | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        names: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigurationTypeListResponse:
        """
        Use this API to get a list of configuration types that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `ep_configuration:read` ]

        Args:
          associated_entity_types: Match only configuration types with the given associated entity type values
              separated by commas.

          broker_type: Match only configuration types with the given broker type.

          ids: Match only configuration types with the given IDs separated by commas.

          names: Match only configuration types with the given names separated by commas.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            "/api/v2/architecture/configurationTypes",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "associated_entity_types": associated_entity_types,
                        "broker_type": broker_type,
                        "ids": ids,
                        "names": names,
                    },
                    configuration_type_list_params.ConfigurationTypeListParams,
                ),
            ),
            cast_to=ConfigurationTypeListResponse,
        )


class ConfigurationTypesResourceWithRawResponse:
    def __init__(self, configuration_types: ConfigurationTypesResource) -> None:
        self._configuration_types = configuration_types

        self.retrieve = to_raw_response_wrapper(
            configuration_types.retrieve,
        )
        self.list = to_raw_response_wrapper(
            configuration_types.list,
        )


class AsyncConfigurationTypesResourceWithRawResponse:
    def __init__(self, configuration_types: AsyncConfigurationTypesResource) -> None:
        self._configuration_types = configuration_types

        self.retrieve = async_to_raw_response_wrapper(
            configuration_types.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            configuration_types.list,
        )


class ConfigurationTypesResourceWithStreamingResponse:
    def __init__(self, configuration_types: ConfigurationTypesResource) -> None:
        self._configuration_types = configuration_types

        self.retrieve = to_streamed_response_wrapper(
            configuration_types.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            configuration_types.list,
        )


class AsyncConfigurationTypesResourceWithStreamingResponse:
    def __init__(self, configuration_types: AsyncConfigurationTypesResource) -> None:
        self._configuration_types = configuration_types

        self.retrieve = async_to_streamed_response_wrapper(
            configuration_types.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            configuration_types.list,
        )
