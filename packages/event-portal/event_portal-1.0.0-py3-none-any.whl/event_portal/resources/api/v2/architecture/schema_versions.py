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
    schema_version_list_params,
    schema_version_create_params,
    schema_version_update_params,
    schema_version_update_state_params,
)
from .....types.api.v2.architecture.custom_attribute_param import CustomAttributeParam
from .....types.api.v2.architecture.schema_version_response import SchemaVersionResponse
from .....types.api.v2.architecture.schema_version_list_response import SchemaVersionListResponse
from .....types.api.v2.architecture.state_change_request_response import StateChangeRequestResponse

__all__ = ["SchemaVersionsResource", "AsyncSchemaVersionsResource"]


class SchemaVersionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SchemaVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return SchemaVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SchemaVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return SchemaVersionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        schema_id: str,
        version: str,
        content: str | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        schema_version_references: Iterable[schema_version_create_params.SchemaVersionReference] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchemaVersionResponse:
        """
        Creates a schema version

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `schema:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._post(
            "/api/v2/architecture/schemaVersions",
            body=maybe_transform(
                {
                    "schema_id": schema_id,
                    "version": version,
                    "content": content,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "schema_version_references": schema_version_references,
                },
                schema_version_create_params.SchemaVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchemaVersionResponse,
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
    ) -> SchemaVersionResponse:
        """
        Use this API to get a single schema version by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `schema:get:*` ]

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
            f"/api/v2/architecture/schemaVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchemaVersionResponse,
        )

    def update(
        self,
        id: str,
        *,
        schema_id: str,
        version: str,
        content: str | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        schema_version_references: Iterable[schema_version_update_params.SchemaVersionReference] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchemaVersionResponse:
        """
        Use this API to update a schema version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `schema:update:*` ]

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
            f"/api/v2/architecture/schemaVersions/{id}",
            body=maybe_transform(
                {
                    "schema_id": schema_id,
                    "version": version,
                    "content": content,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "schema_version_references": schema_version_references,
                },
                schema_version_update_params.SchemaVersionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchemaVersionResponse,
        )

    def list(
        self,
        *,
        custom_attributes: str | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        schema_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchemaVersionListResponse:
        """
        Use this API to get a list of schema versions that match the given parameters.

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

          ids: Match only schema versions with the given IDs, separated by commas.

          page_number: The page number to get.

          page_size: The number of schema versions to get per page.

          schema_ids: Match only schema versions of these schema IDs, separated by commas.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            "/api/v2/architecture/schemaVersions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "custom_attributes": custom_attributes,
                        "ids": ids,
                        "page_number": page_number,
                        "page_size": page_size,
                        "schema_ids": schema_ids,
                    },
                    schema_version_list_params.SchemaVersionListParams,
                ),
            ),
            cast_to=SchemaVersionListResponse,
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
        Use this API to delete a schema version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `schema:update:*` ]

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
            f"/api/v2/architecture/schemaVersions/{id}",
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
        """
        Use this API to update the state of a schema version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `schema:update_state:*` ]

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
            f"/api/v2/architecture/schemaVersions/{id}/state",
            body=maybe_transform(
                {"state_id": state_id}, schema_version_update_state_params.SchemaVersionUpdateStateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StateChangeRequestResponse,
        )


class AsyncSchemaVersionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSchemaVersionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSchemaVersionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSchemaVersionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncSchemaVersionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        schema_id: str,
        version: str,
        content: str | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        schema_version_references: Iterable[schema_version_create_params.SchemaVersionReference] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchemaVersionResponse:
        """
        Creates a schema version

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `schema:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._post(
            "/api/v2/architecture/schemaVersions",
            body=await async_maybe_transform(
                {
                    "schema_id": schema_id,
                    "version": version,
                    "content": content,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "schema_version_references": schema_version_references,
                },
                schema_version_create_params.SchemaVersionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchemaVersionResponse,
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
    ) -> SchemaVersionResponse:
        """
        Use this API to get a single schema version by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `schema:get:*` ]

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
            f"/api/v2/architecture/schemaVersions/{version_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchemaVersionResponse,
        )

    async def update(
        self,
        id: str,
        *,
        schema_id: str,
        version: str,
        content: str | NotGiven = NOT_GIVEN,
        custom_attributes: Iterable[CustomAttributeParam] | NotGiven = NOT_GIVEN,
        description: str | NotGiven = NOT_GIVEN,
        display_name: str | NotGiven = NOT_GIVEN,
        end_of_life_date: str | NotGiven = NOT_GIVEN,
        schema_version_references: Iterable[schema_version_update_params.SchemaVersionReference] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchemaVersionResponse:
        """
        Use this API to update a schema version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `schema:update:*` ]

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
            f"/api/v2/architecture/schemaVersions/{id}",
            body=await async_maybe_transform(
                {
                    "schema_id": schema_id,
                    "version": version,
                    "content": content,
                    "custom_attributes": custom_attributes,
                    "description": description,
                    "display_name": display_name,
                    "end_of_life_date": end_of_life_date,
                    "schema_version_references": schema_version_references,
                },
                schema_version_update_params.SchemaVersionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=SchemaVersionResponse,
        )

    async def list(
        self,
        *,
        custom_attributes: str | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        schema_ids: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SchemaVersionListResponse:
        """
        Use this API to get a list of schema versions that match the given parameters.

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

          ids: Match only schema versions with the given IDs, separated by commas.

          page_number: The page number to get.

          page_size: The number of schema versions to get per page.

          schema_ids: Match only schema versions of these schema IDs, separated by commas.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            "/api/v2/architecture/schemaVersions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "custom_attributes": custom_attributes,
                        "ids": ids,
                        "page_number": page_number,
                        "page_size": page_size,
                        "schema_ids": schema_ids,
                    },
                    schema_version_list_params.SchemaVersionListParams,
                ),
            ),
            cast_to=SchemaVersionListResponse,
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
        Use this API to delete a schema version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `schema:update:*` ]

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
            f"/api/v2/architecture/schemaVersions/{id}",
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
        """
        Use this API to update the state of a schema version.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `schema:update_state:*` ]

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
            f"/api/v2/architecture/schemaVersions/{id}/state",
            body=await async_maybe_transform(
                {"state_id": state_id}, schema_version_update_state_params.SchemaVersionUpdateStateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=StateChangeRequestResponse,
        )


class SchemaVersionsResourceWithRawResponse:
    def __init__(self, schema_versions: SchemaVersionsResource) -> None:
        self._schema_versions = schema_versions

        self.create = to_raw_response_wrapper(
            schema_versions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            schema_versions.retrieve,
        )
        self.update = to_raw_response_wrapper(
            schema_versions.update,
        )
        self.list = to_raw_response_wrapper(
            schema_versions.list,
        )
        self.delete = to_raw_response_wrapper(
            schema_versions.delete,
        )
        self.update_state = to_raw_response_wrapper(
            schema_versions.update_state,
        )


class AsyncSchemaVersionsResourceWithRawResponse:
    def __init__(self, schema_versions: AsyncSchemaVersionsResource) -> None:
        self._schema_versions = schema_versions

        self.create = async_to_raw_response_wrapper(
            schema_versions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            schema_versions.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            schema_versions.update,
        )
        self.list = async_to_raw_response_wrapper(
            schema_versions.list,
        )
        self.delete = async_to_raw_response_wrapper(
            schema_versions.delete,
        )
        self.update_state = async_to_raw_response_wrapper(
            schema_versions.update_state,
        )


class SchemaVersionsResourceWithStreamingResponse:
    def __init__(self, schema_versions: SchemaVersionsResource) -> None:
        self._schema_versions = schema_versions

        self.create = to_streamed_response_wrapper(
            schema_versions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            schema_versions.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            schema_versions.update,
        )
        self.list = to_streamed_response_wrapper(
            schema_versions.list,
        )
        self.delete = to_streamed_response_wrapper(
            schema_versions.delete,
        )
        self.update_state = to_streamed_response_wrapper(
            schema_versions.update_state,
        )


class AsyncSchemaVersionsResourceWithStreamingResponse:
    def __init__(self, schema_versions: AsyncSchemaVersionsResource) -> None:
        self._schema_versions = schema_versions

        self.create = async_to_streamed_response_wrapper(
            schema_versions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            schema_versions.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            schema_versions.update,
        )
        self.list = async_to_streamed_response_wrapper(
            schema_versions.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            schema_versions.delete,
        )
        self.update_state = async_to_streamed_response_wrapper(
            schema_versions.update_state,
        )
