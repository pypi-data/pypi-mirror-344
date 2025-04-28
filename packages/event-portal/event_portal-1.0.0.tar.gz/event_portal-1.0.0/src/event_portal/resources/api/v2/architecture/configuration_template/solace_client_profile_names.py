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
    solace_client_profile_name_list_params,
    solace_client_profile_name_create_params,
    solace_client_profile_name_update_params,
)
from ......types.api.v2.architecture.configuration_template.solace_client_profile_name_list_response import (
    SolaceClientProfileNameListResponse,
)
from ......types.api.v2.architecture.configuration_template.solace_client_profile_name_configuration_template_response import (
    SolaceClientProfileNameConfigurationTemplateResponse,
)

__all__ = ["SolaceClientProfileNamesResource", "AsyncSolaceClientProfileNamesResource"]


class SolaceClientProfileNamesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SolaceClientProfileNamesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return SolaceClientProfileNamesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SolaceClientProfileNamesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return SolaceClientProfileNamesResourceWithStreamingResponse(self)

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
    ) -> SolaceClientProfileNameConfigurationTemplateResponse:
        """
        Create a client profile name configuration template to provide the client
        profile name for an application.

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
            "/api/v2/architecture/configurationTemplate/solaceClientProfileNames",
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "type": type,
                    "value": value,
                },
                solace_client_profile_name_create_params.SolaceClientProfileNameCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SolaceClientProfileNameConfigurationTemplateResponse,
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
    ) -> SolaceClientProfileNameConfigurationTemplateResponse:
        """
        Get a client profile name configuration template by its identifier.

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
            f"/api/v2/architecture/configurationTemplate/solaceClientProfileNames/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SolaceClientProfileNameConfigurationTemplateResponse,
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
    ) -> SolaceClientProfileNameConfigurationTemplateResponse:
        """
        Update a client profile name configuration template.

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
            f"/api/v2/architecture/configurationTemplate/solaceClientProfileNames/{id}",
            body=maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "type": type,
                    "value": value,
                },
                solace_client_profile_name_update_params.SolaceClientProfileNameUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SolaceClientProfileNameConfigurationTemplateResponse,
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
    ) -> SolaceClientProfileNameListResponse:
        """
        Get a list of client profile name configuration templates that match the
        specified parameters.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          ids: The unique identifiers of the client profile name configuration templates to
              retrieve, separated by commas.

          name: The name of the client profile name configuration template to match.

          page_number: The page number to retrieve.

          page_size: The number of client profile name configuration templates to return per page.

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
            "/api/v2/architecture/configurationTemplate/solaceClientProfileNames",
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
                    solace_client_profile_name_list_params.SolaceClientProfileNameListParams,
                ),
            ),
            cast_to=SolaceClientProfileNameListResponse,
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
        Delete a client profile name configuration template.

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
            f"/api/v2/architecture/configurationTemplate/solaceClientProfileNames/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncSolaceClientProfileNamesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSolaceClientProfileNamesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSolaceClientProfileNamesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSolaceClientProfileNamesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncSolaceClientProfileNamesResourceWithStreamingResponse(self)

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
    ) -> SolaceClientProfileNameConfigurationTemplateResponse:
        """
        Create a client profile name configuration template to provide the client
        profile name for an application.

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
            "/api/v2/architecture/configurationTemplate/solaceClientProfileNames",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "type": type,
                    "value": value,
                },
                solace_client_profile_name_create_params.SolaceClientProfileNameCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SolaceClientProfileNameConfigurationTemplateResponse,
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
    ) -> SolaceClientProfileNameConfigurationTemplateResponse:
        """
        Get a client profile name configuration template by its identifier.

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
            f"/api/v2/architecture/configurationTemplate/solaceClientProfileNames/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SolaceClientProfileNameConfigurationTemplateResponse,
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
    ) -> SolaceClientProfileNameConfigurationTemplateResponse:
        """
        Update a client profile name configuration template.

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
            f"/api/v2/architecture/configurationTemplate/solaceClientProfileNames/{id}",
            body=await async_maybe_transform(
                {
                    "description": description,
                    "name": name,
                    "type": type,
                    "value": value,
                },
                solace_client_profile_name_update_params.SolaceClientProfileNameUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SolaceClientProfileNameConfigurationTemplateResponse,
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
    ) -> SolaceClientProfileNameListResponse:
        """
        Get a list of client profile name configuration templates that match the
        specified parameters.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          ids: The unique identifiers of the client profile name configuration templates to
              retrieve, separated by commas.

          name: The name of the client profile name configuration template to match.

          page_number: The page number to retrieve.

          page_size: The number of client profile name configuration templates to return per page.

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
            "/api/v2/architecture/configurationTemplate/solaceClientProfileNames",
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
                    solace_client_profile_name_list_params.SolaceClientProfileNameListParams,
                ),
            ),
            cast_to=SolaceClientProfileNameListResponse,
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
        Delete a client profile name configuration template.

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
            f"/api/v2/architecture/configurationTemplate/solaceClientProfileNames/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class SolaceClientProfileNamesResourceWithRawResponse:
    def __init__(self, solace_client_profile_names: SolaceClientProfileNamesResource) -> None:
        self._solace_client_profile_names = solace_client_profile_names

        self.create = to_raw_response_wrapper(
            solace_client_profile_names.create,
        )
        self.retrieve = to_raw_response_wrapper(
            solace_client_profile_names.retrieve,
        )
        self.update = to_raw_response_wrapper(
            solace_client_profile_names.update,
        )
        self.list = to_raw_response_wrapper(
            solace_client_profile_names.list,
        )
        self.delete = to_raw_response_wrapper(
            solace_client_profile_names.delete,
        )


class AsyncSolaceClientProfileNamesResourceWithRawResponse:
    def __init__(self, solace_client_profile_names: AsyncSolaceClientProfileNamesResource) -> None:
        self._solace_client_profile_names = solace_client_profile_names

        self.create = async_to_raw_response_wrapper(
            solace_client_profile_names.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            solace_client_profile_names.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            solace_client_profile_names.update,
        )
        self.list = async_to_raw_response_wrapper(
            solace_client_profile_names.list,
        )
        self.delete = async_to_raw_response_wrapper(
            solace_client_profile_names.delete,
        )


class SolaceClientProfileNamesResourceWithStreamingResponse:
    def __init__(self, solace_client_profile_names: SolaceClientProfileNamesResource) -> None:
        self._solace_client_profile_names = solace_client_profile_names

        self.create = to_streamed_response_wrapper(
            solace_client_profile_names.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            solace_client_profile_names.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            solace_client_profile_names.update,
        )
        self.list = to_streamed_response_wrapper(
            solace_client_profile_names.list,
        )
        self.delete = to_streamed_response_wrapper(
            solace_client_profile_names.delete,
        )


class AsyncSolaceClientProfileNamesResourceWithStreamingResponse:
    def __init__(self, solace_client_profile_names: AsyncSolaceClientProfileNamesResource) -> None:
        self._solace_client_profile_names = solace_client_profile_names

        self.create = async_to_streamed_response_wrapper(
            solace_client_profile_names.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            solace_client_profile_names.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            solace_client_profile_names.update,
        )
        self.list = async_to_streamed_response_wrapper(
            solace_client_profile_names.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            solace_client_profile_names.delete,
        )
