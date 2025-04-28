# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
from typing_extensions import Literal

import httpx

from .exports import (
    ExportsResource,
    AsyncExportsResource,
    ExportsResourceWithRawResponse,
    AsyncExportsResourceWithRawResponse,
    ExportsResourceWithStreamingResponse,
    AsyncExportsResourceWithStreamingResponse,
)
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
from ......types.api.v2.architecture import (
    event_api_version_list_params,
    event_api_version_create_params,
    event_api_version_update_params,
    event_api_version_retrieve_params,
    event_api_version_update_state_params,
    event_api_version_get_async_api_params,
)
from ......types.api.v2.architecture.custom_attribute_param import CustomAttributeParam
from ......types.api.v2.architecture.event_api_version_response import EventAPIVersionResponse
from ......types.api.v2.architecture.state_change_request_response import StateChangeRequestResponse
from ......types.api.v2.architecture.event_api_version_list_response import EventAPIVersionListResponse

__all__ = ["EventAPIVersionsResource", "AsyncEventAPIVersionsResource"]


class EventAPIVersionsResource(SyncAPIResource):
    @cached_property
    def exports(self) -> ExportsResource:
        return ExportsResource(self._client)

    @cached_property
    def with_raw_response(self) -> EventAPIVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return EventAPIVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> EventAPIVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return EventAPIVersionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        event_api_id: str,
        consumed_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        declared_event_api_product_version_ids: List[str] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        produced_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIVersionResponse:
        """
        Use this API to create an event API version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/api/v2/architecture/eventApiVersions",
            body=maybe_transform(
                {
                    "event_api_id": event_api_id,
                    "consumed_event_version_ids": consumed_event_version_ids,
                    "custom_attributes": custom_attributes,
                    "declared_event_api_product_version_ids": declared_event_api_product_version_ids,
                    "description": description,
                    "display_name": display_name,
                    "produced_event_version_ids": produced_event_version_ids,
                    "state_id": state_id,
                    "type": type,
                    "version": version,
                },
                event_api_version_create_params.EventAPIVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIVersionResponse,
        )

    def retrieve(
        self,
        version_id: str,
        *,
        include: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIVersionResponse:
        """
        Use this API to get a single event API version by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:get:*` ]

        Args:
          include: A list of additional entities to include in the response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return self._get(
            f"/api/v2/architecture/eventApiVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"include": include}, event_api_version_retrieve_params.EventAPIVersionRetrieveParams
                ),
            ),
            cast_to=EventAPIVersionResponse,
        )

    def update(
        self,
        version_id: str,
        *,
        event_api_id: str,
        consumed_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        declared_event_api_product_version_ids: List[str] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        produced_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIVersionResponse:
        """
        Use this API to update an event API version by event API version ID.You only
        need to specify the fields that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return self._patch(
            f"/api/v2/architecture/eventApiVersions/{version_id}",
            body=maybe_transform(
                {
                    "event_api_id": event_api_id,
                    "consumed_event_version_ids": consumed_event_version_ids,
                    "custom_attributes": custom_attributes,
                    "declared_event_api_product_version_ids": declared_event_api_product_version_ids,
                    "description": description,
                    "display_name": display_name,
                    "produced_event_version_ids": produced_event_version_ids,
                    "state_id": state_id,
                    "type": type,
                    "version": version,
                },
                event_api_version_update_params.EventAPIVersionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIVersionResponse,
        )

    def list(
        self,
        *,
        custom_attributes: str | NotGiven = NOT_GIVEN,
        event_api_ids: List[str] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        include: str | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIVersionListResponse:
        """
        Use this API to get a list of event API versions that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          custom_attributes: Returns the entities that match the custom attribute filter. To filter by custom
              attribute name and value, use the format:
              `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
              by custom attribute name, use the format:
              `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
              operator for multiple custom attribute definitions (not multiple values for a
              given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
              operation. Note: the filter supports custom attribute values containing only the
              characters `[a-zA-Z0-9_\\--\\.. ]`.

          event_api_ids: Match only event API versions of these event API IDs, separated by commas.

          ids: Match event API versions with the given IDs, separated by commas.

          include: A list of additional entities to include in the response.

          page_number: The page number to get results from based on the page size.

          page_size: The number of results to return in one page of results.

          state_id: Match event API versions with the given state ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/api/v2/architecture/eventApiVersions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "custom_attributes": custom_attributes,
                        "event_api_ids": event_api_ids,
                        "ids": ids,
                        "include": include,
                        "page_number": page_number,
                        "page_size": page_size,
                        "state_id": state_id,
                    },
                    event_api_version_list_params.EventAPIVersionListParams,
                ),
            ),
            cast_to=EventAPIVersionListResponse,
        )

    def delete(
        self,
        version_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Use this API to delete an event API version by event API version ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v2/architecture/eventApiVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def get_async_api(
        self,
        event_api_version_id: str,
        *,
        async_api_version: Literal["2.0.0", "2.2.0", "2.5.0"] | NotGiven = NOT_GIVEN,
        event_api_product_version_id: str | NotGiven = NOT_GIVEN,
        format: Literal["json", "yaml"] | NotGiven = NOT_GIVEN,
        gateway_messaging_service_ids: List[str] | NotGiven = NOT_GIVEN,
        included_extensions: Literal["all", "parent", "version", "none"] | NotGiven = NOT_GIVEN,
        plan_id: str | NotGiven = NOT_GIVEN,
        show_versioning: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Use this API to get the AsyncAPI specification for an event API version
        annotated with Event Portal metadata. Deprecation Date: 2025-01-20 Removal Date:
        2026-01-20 Reason: Replaced by
        /eventApiVersions/{eventApiVersionId}/exports/asyncAPI

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:generate_async_api:*` ]

        Args:
          async_api_version: The version of AsyncAPI to use.

          event_api_product_version_id: The ID of the event API Product Version to use for generating bindings.

          format: The format in which to get the AsyncAPI specification. Possible values are yaml
              and json.

          gateway_messaging_service_ids: The list IDs of gateway messaging services for generating bindings.

          included_extensions: The event portal database keys to include for each AsyncAPI object.

          plan_id: The ID of the plan to use for generating bindings.

          show_versioning: Include versions in each AsyncAPI object's name when only one version is present

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not event_api_version_id:
            raise ValueError(
                f"Expected a non-empty value for `event_api_version_id` but received {event_api_version_id!r}"
            )
        return self._get(
            f"/api/v2/architecture/eventApiVersions/{event_api_version_id}/asyncApi",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "async_api_version": async_api_version,
                        "event_api_product_version_id": event_api_product_version_id,
                        "format": format,
                        "gateway_messaging_service_ids": gateway_messaging_service_ids,
                        "included_extensions": included_extensions,
                        "plan_id": plan_id,
                        "show_versioning": show_versioning,
                    },
                    event_api_version_get_async_api_params.EventAPIVersionGetAsyncAPIParams,
                ),
            ),
            cast_to=str,
        )

    def update_state(
        self,
        version_id: str,
        *,
        event_api_id: str,
        consumed_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        declared_event_api_product_version_ids: List[str] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        produced_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StateChangeRequestResponse:
        """Use this API to update the state of an event API version.

        You only need to
        specify the state ID field with the desired state ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:update_state:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return self._patch(
            f"/api/v2/architecture/eventApiVersions/{version_id}/state",
            body=maybe_transform(
                {
                    "event_api_id": event_api_id,
                    "consumed_event_version_ids": consumed_event_version_ids,
                    "custom_attributes": custom_attributes,
                    "declared_event_api_product_version_ids": declared_event_api_product_version_ids,
                    "description": description,
                    "display_name": display_name,
                    "produced_event_version_ids": produced_event_version_ids,
                    "state_id": state_id,
                    "type": type,
                    "version": version,
                },
                event_api_version_update_state_params.EventAPIVersionUpdateStateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StateChangeRequestResponse,
        )


class AsyncEventAPIVersionsResource(AsyncAPIResource):
    @cached_property
    def exports(self) -> AsyncExportsResource:
        return AsyncExportsResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncEventAPIVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncEventAPIVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncEventAPIVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncEventAPIVersionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        event_api_id: str,
        consumed_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        declared_event_api_product_version_ids: List[str] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        produced_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIVersionResponse:
        """
        Use this API to create an event API version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/api/v2/architecture/eventApiVersions",
            body=await async_maybe_transform(
                {
                    "event_api_id": event_api_id,
                    "consumed_event_version_ids": consumed_event_version_ids,
                    "custom_attributes": custom_attributes,
                    "declared_event_api_product_version_ids": declared_event_api_product_version_ids,
                    "description": description,
                    "display_name": display_name,
                    "produced_event_version_ids": produced_event_version_ids,
                    "state_id": state_id,
                    "type": type,
                    "version": version,
                },
                event_api_version_create_params.EventAPIVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIVersionResponse,
        )

    async def retrieve(
        self,
        version_id: str,
        *,
        include: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIVersionResponse:
        """
        Use this API to get a single event API version by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:get:*` ]

        Args:
          include: A list of additional entities to include in the response.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return await self._get(
            f"/api/v2/architecture/eventApiVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"include": include}, event_api_version_retrieve_params.EventAPIVersionRetrieveParams
                ),
            ),
            cast_to=EventAPIVersionResponse,
        )

    async def update(
        self,
        version_id: str,
        *,
        event_api_id: str,
        consumed_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        declared_event_api_product_version_ids: List[str] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        produced_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIVersionResponse:
        """
        Use this API to update an event API version by event API version ID.You only
        need to specify the fields that need to be updated.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return await self._patch(
            f"/api/v2/architecture/eventApiVersions/{version_id}",
            body=await async_maybe_transform(
                {
                    "event_api_id": event_api_id,
                    "consumed_event_version_ids": consumed_event_version_ids,
                    "custom_attributes": custom_attributes,
                    "declared_event_api_product_version_ids": declared_event_api_product_version_ids,
                    "description": description,
                    "display_name": display_name,
                    "produced_event_version_ids": produced_event_version_ids,
                    "state_id": state_id,
                    "type": type,
                    "version": version,
                },
                event_api_version_update_params.EventAPIVersionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=EventAPIVersionResponse,
        )

    async def list(
        self,
        *,
        custom_attributes: str | NotGiven = NOT_GIVEN,
        event_api_ids: List[str] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        include: str | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> EventAPIVersionListResponse:
        """
        Use this API to get a list of event API versions that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          custom_attributes: Returns the entities that match the custom attribute filter. To filter by custom
              attribute name and value, use the format:
              `customAttributes=<custom-attribute-name>==<custom-attribute-value>`. To filter
              by custom attribute name, use the format:
              `customAttributes=<custom-attribute-name>`. The filter supports the `AND`
              operator for multiple custom attribute definitions (not multiple values for a
              given definition). Use `;` (`semicolon`) to separate multiple queries with `AND`
              operation. Note: the filter supports custom attribute values containing only the
              characters `[a-zA-Z0-9_\\--\\.. ]`.

          event_api_ids: Match only event API versions of these event API IDs, separated by commas.

          ids: Match event API versions with the given IDs, separated by commas.

          include: A list of additional entities to include in the response.

          page_number: The page number to get results from based on the page size.

          page_size: The number of results to return in one page of results.

          state_id: Match event API versions with the given state ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/api/v2/architecture/eventApiVersions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "custom_attributes": custom_attributes,
                        "event_api_ids": event_api_ids,
                        "ids": ids,
                        "include": include,
                        "page_number": page_number,
                        "page_size": page_size,
                        "state_id": state_id,
                    },
                    event_api_version_list_params.EventAPIVersionListParams,
                ),
            ),
            cast_to=EventAPIVersionListResponse,
        )

    async def delete(
        self,
        version_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Use this API to delete an event API version by event API version ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v2/architecture/eventApiVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def get_async_api(
        self,
        event_api_version_id: str,
        *,
        async_api_version: Literal["2.0.0", "2.2.0", "2.5.0"] | NotGiven = NOT_GIVEN,
        event_api_product_version_id: str | NotGiven = NOT_GIVEN,
        format: Literal["json", "yaml"] | NotGiven = NOT_GIVEN,
        gateway_messaging_service_ids: List[str] | NotGiven = NOT_GIVEN,
        included_extensions: Literal["all", "parent", "version", "none"] | NotGiven = NOT_GIVEN,
        plan_id: str | NotGiven = NOT_GIVEN,
        show_versioning: bool | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Use this API to get the AsyncAPI specification for an event API version
        annotated with Event Portal metadata. Deprecation Date: 2025-01-20 Removal Date:
        2026-01-20 Reason: Replaced by
        /eventApiVersions/{eventApiVersionId}/exports/asyncAPI

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:generate_async_api:*` ]

        Args:
          async_api_version: The version of AsyncAPI to use.

          event_api_product_version_id: The ID of the event API Product Version to use for generating bindings.

          format: The format in which to get the AsyncAPI specification. Possible values are yaml
              and json.

          gateway_messaging_service_ids: The list IDs of gateway messaging services for generating bindings.

          included_extensions: The event portal database keys to include for each AsyncAPI object.

          plan_id: The ID of the plan to use for generating bindings.

          show_versioning: Include versions in each AsyncAPI object's name when only one version is present

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not event_api_version_id:
            raise ValueError(
                f"Expected a non-empty value for `event_api_version_id` but received {event_api_version_id!r}"
            )
        return await self._get(
            f"/api/v2/architecture/eventApiVersions/{event_api_version_id}/asyncApi",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "async_api_version": async_api_version,
                        "event_api_product_version_id": event_api_product_version_id,
                        "format": format,
                        "gateway_messaging_service_ids": gateway_messaging_service_ids,
                        "included_extensions": included_extensions,
                        "plan_id": plan_id,
                        "show_versioning": show_versioning,
                    },
                    event_api_version_get_async_api_params.EventAPIVersionGetAsyncAPIParams,
                ),
            ),
            cast_to=str,
        )

    async def update_state(
        self,
        version_id: str,
        *,
        event_api_id: str,
        consumed_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        declared_event_api_product_version_ids: List[str] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        produced_event_version_ids: List[str] | NotGiven = NOT_GIVEN,
        state_id: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        version: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> StateChangeRequestResponse:
        """Use this API to update the state of an event API version.

        You only need to
        specify the state ID field with the desired state ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api:update_state:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not version_id:
            raise ValueError(f"Expected a non-empty value for `version_id` but received {version_id!r}")
        return await self._patch(
            f"/api/v2/architecture/eventApiVersions/{version_id}/state",
            body=await async_maybe_transform(
                {
                    "event_api_id": event_api_id,
                    "consumed_event_version_ids": consumed_event_version_ids,
                    "custom_attributes": custom_attributes,
                    "declared_event_api_product_version_ids": declared_event_api_product_version_ids,
                    "description": description,
                    "display_name": display_name,
                    "produced_event_version_ids": produced_event_version_ids,
                    "state_id": state_id,
                    "type": type,
                    "version": version,
                },
                event_api_version_update_state_params.EventAPIVersionUpdateStateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StateChangeRequestResponse,
        )


class EventAPIVersionsResourceWithRawResponse:
    def __init__(self, event_api_versions: EventAPIVersionsResource) -> None:
        self._event_api_versions = event_api_versions

        self.create = to_raw_response_wrapper(
            event_api_versions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            event_api_versions.retrieve,
        )
        self.update = to_raw_response_wrapper(
            event_api_versions.update,
        )
        self.list = to_raw_response_wrapper(
            event_api_versions.list,
        )
        self.delete = to_raw_response_wrapper(
            event_api_versions.delete,
        )
        self.get_async_api = to_raw_response_wrapper(
            event_api_versions.get_async_api,
        )
        self.update_state = to_raw_response_wrapper(
            event_api_versions.update_state,
        )

    @cached_property
    def exports(self) -> ExportsResourceWithRawResponse:
        return ExportsResourceWithRawResponse(self._event_api_versions.exports)


class AsyncEventAPIVersionsResourceWithRawResponse:
    def __init__(self, event_api_versions: AsyncEventAPIVersionsResource) -> None:
        self._event_api_versions = event_api_versions

        self.create = async_to_raw_response_wrapper(
            event_api_versions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            event_api_versions.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            event_api_versions.update,
        )
        self.list = async_to_raw_response_wrapper(
            event_api_versions.list,
        )
        self.delete = async_to_raw_response_wrapper(
            event_api_versions.delete,
        )
        self.get_async_api = async_to_raw_response_wrapper(
            event_api_versions.get_async_api,
        )
        self.update_state = async_to_raw_response_wrapper(
            event_api_versions.update_state,
        )

    @cached_property
    def exports(self) -> AsyncExportsResourceWithRawResponse:
        return AsyncExportsResourceWithRawResponse(self._event_api_versions.exports)


class EventAPIVersionsResourceWithStreamingResponse:
    def __init__(self, event_api_versions: EventAPIVersionsResource) -> None:
        self._event_api_versions = event_api_versions

        self.create = to_streamed_response_wrapper(
            event_api_versions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            event_api_versions.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            event_api_versions.update,
        )
        self.list = to_streamed_response_wrapper(
            event_api_versions.list,
        )
        self.delete = to_streamed_response_wrapper(
            event_api_versions.delete,
        )
        self.get_async_api = to_streamed_response_wrapper(
            event_api_versions.get_async_api,
        )
        self.update_state = to_streamed_response_wrapper(
            event_api_versions.update_state,
        )

    @cached_property
    def exports(self) -> ExportsResourceWithStreamingResponse:
        return ExportsResourceWithStreamingResponse(self._event_api_versions.exports)


class AsyncEventAPIVersionsResourceWithStreamingResponse:
    def __init__(self, event_api_versions: AsyncEventAPIVersionsResource) -> None:
        self._event_api_versions = event_api_versions

        self.create = async_to_streamed_response_wrapper(
            event_api_versions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            event_api_versions.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            event_api_versions.update,
        )
        self.list = async_to_streamed_response_wrapper(
            event_api_versions.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            event_api_versions.delete,
        )
        self.get_async_api = async_to_streamed_response_wrapper(
            event_api_versions.get_async_api,
        )
        self.update_state = async_to_streamed_response_wrapper(
            event_api_versions.update_state,
        )

    @cached_property
    def exports(self) -> AsyncExportsResourceWithStreamingResponse:
        return AsyncExportsResourceWithStreamingResponse(self._event_api_versions.exports)
