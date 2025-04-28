# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ......_types import NOT_GIVEN, Body, Query, Headers, NotGiven
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
from ......types.api.v2.architecture.application_versions import export_get_async_api_params

__all__ = ["ExportsResource", "AsyncExportsResource"]


class ExportsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ExportsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return ExportsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ExportsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return ExportsResourceWithStreamingResponse(self)

    def get_async_api(
        self,
        application_version_id: str,
        *,
        async_api_version: Literal["2.0.0", "2.2.0", "2.5.0"] | NotGiven = NOT_GIVEN,
        context_id: str | NotGiven = NOT_GIVEN,
        context_type: Literal["eventBroker", "eventMesh"] | NotGiven = NOT_GIVEN,
        expand: Literal[
            "declaredSubscribedEvents",
            "attractedEvents",
            "servers",
            "serverBindings",
            "declaredSubscribedEventBindings",
            "attractedEventBindings",
        ]
        | NotGiven = NOT_GIVEN,
        format: Literal["json", "yaml"] | NotGiven = NOT_GIVEN,
        included_extensions: Literal["all", "parent", "version", "none"] | NotGiven = NOT_GIVEN,
        naming_strategies: List[Literal["applicationDomainPrefix", "majorVersionSuffix"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Use this API to get the AsyncAPI specification for an application version
        annotated with Event Portal metadata.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:generate_async_api:*` ]

        Args:
          async_api_version: The version of AsyncAPI to use.

          context_id: Applies bindings from subscribed events that are published in this event broker
              or event mesh.

          context_type: The context of which events are attracted from.

          expand: A comma separated list of sections of the asyncapi document to include.

          format: The format in which to get the AsyncAPI specification. Possible values are yaml
              and json.

          included_extensions: The event portal database keys to include for each AsyncAPI object.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_version_id:
            raise ValueError(
                f"Expected a non-empty value for `application_version_id` but received {application_version_id!r}"
            )
        return self._get(
            f"/api/v2/architecture/applicationVersions/{application_version_id}/exports/asyncApi",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "async_api_version": async_api_version,
                        "context_id": context_id,
                        "context_type": context_type,
                        "expand": expand,
                        "format": format,
                        "included_extensions": included_extensions,
                        "naming_strategies": naming_strategies,
                    },
                    export_get_async_api_params.ExportGetAsyncAPIParams,
                ),
            ),
            cast_to=str,
        )


class AsyncExportsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncExportsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncExportsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncExportsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncExportsResourceWithStreamingResponse(self)

    async def get_async_api(
        self,
        application_version_id: str,
        *,
        async_api_version: Literal["2.0.0", "2.2.0", "2.5.0"] | NotGiven = NOT_GIVEN,
        context_id: str | NotGiven = NOT_GIVEN,
        context_type: Literal["eventBroker", "eventMesh"] | NotGiven = NOT_GIVEN,
        expand: Literal[
            "declaredSubscribedEvents",
            "attractedEvents",
            "servers",
            "serverBindings",
            "declaredSubscribedEventBindings",
            "attractedEventBindings",
        ]
        | NotGiven = NOT_GIVEN,
        format: Literal["json", "yaml"] | NotGiven = NOT_GIVEN,
        included_extensions: Literal["all", "parent", "version", "none"] | NotGiven = NOT_GIVEN,
        naming_strategies: List[Literal["applicationDomainPrefix", "majorVersionSuffix"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> str:
        """
        Use this API to get the AsyncAPI specification for an application version
        annotated with Event Portal metadata.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:generate_async_api:*` ]

        Args:
          async_api_version: The version of AsyncAPI to use.

          context_id: Applies bindings from subscribed events that are published in this event broker
              or event mesh.

          context_type: The context of which events are attracted from.

          expand: A comma separated list of sections of the asyncapi document to include.

          format: The format in which to get the AsyncAPI specification. Possible values are yaml
              and json.

          included_extensions: The event portal database keys to include for each AsyncAPI object.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_version_id:
            raise ValueError(
                f"Expected a non-empty value for `application_version_id` but received {application_version_id!r}"
            )
        return await self._get(
            f"/api/v2/architecture/applicationVersions/{application_version_id}/exports/asyncApi",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "async_api_version": async_api_version,
                        "context_id": context_id,
                        "context_type": context_type,
                        "expand": expand,
                        "format": format,
                        "included_extensions": included_extensions,
                        "naming_strategies": naming_strategies,
                    },
                    export_get_async_api_params.ExportGetAsyncAPIParams,
                ),
            ),
            cast_to=str,
        )


class ExportsResourceWithRawResponse:
    def __init__(self, exports: ExportsResource) -> None:
        self._exports = exports

        self.get_async_api = to_raw_response_wrapper(
            exports.get_async_api,
        )


class AsyncExportsResourceWithRawResponse:
    def __init__(self, exports: AsyncExportsResource) -> None:
        self._exports = exports

        self.get_async_api = async_to_raw_response_wrapper(
            exports.get_async_api,
        )


class ExportsResourceWithStreamingResponse:
    def __init__(self, exports: ExportsResource) -> None:
        self._exports = exports

        self.get_async_api = to_streamed_response_wrapper(
            exports.get_async_api,
        )


class AsyncExportsResourceWithStreamingResponse:
    def __init__(self, exports: AsyncExportsResource) -> None:
        self._exports = exports

        self.get_async_api = async_to_streamed_response_wrapper(
            exports.get_async_api,
        )
