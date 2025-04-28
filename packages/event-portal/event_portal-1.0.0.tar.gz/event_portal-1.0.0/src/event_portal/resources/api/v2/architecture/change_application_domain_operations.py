# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

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
from .....types.api.v2.architecture import change_application_domain_operation_create_params
from .....types.api.v2.architecture.change_application_domain_operation_retrieve_response import (
    ChangeApplicationDomainOperationRetrieveResponse,
)

__all__ = ["ChangeApplicationDomainOperationsResource", "AsyncChangeApplicationDomainOperationsResource"]


class ChangeApplicationDomainOperationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ChangeApplicationDomainOperationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return ChangeApplicationDomainOperationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ChangeApplicationDomainOperationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return ChangeApplicationDomainOperationsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        entities: Iterable[change_application_domain_operation_create_params.Entity] | NotGiven = NOT_GIVEN,
        target_app_domain_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Use this API to execute a change application domain operation.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application_domain:move_contents:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/api/v2/architecture/changeApplicationDomainOperations",
            body=maybe_transform(
                {
                    "entities": entities,
                    "target_app_domain_id": target_app_domain_id,
                },
                change_application_domain_operation_create_params.ChangeApplicationDomainOperationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
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
    ) -> ChangeApplicationDomainOperationRetrieveResponse:
        """
        Use this API to retrieve a single change application domain operation by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

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
            f"/api/v2/architecture/changeApplicationDomainOperations/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChangeApplicationDomainOperationRetrieveResponse,
        )


class AsyncChangeApplicationDomainOperationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncChangeApplicationDomainOperationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncChangeApplicationDomainOperationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncChangeApplicationDomainOperationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncChangeApplicationDomainOperationsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        entities: Iterable[change_application_domain_operation_create_params.Entity] | NotGiven = NOT_GIVEN,
        target_app_domain_id: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Use this API to execute a change application domain operation.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application_domain:move_contents:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/api/v2/architecture/changeApplicationDomainOperations",
            body=await async_maybe_transform(
                {
                    "entities": entities,
                    "target_app_domain_id": target_app_domain_id,
                },
                change_application_domain_operation_create_params.ChangeApplicationDomainOperationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
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
    ) -> ChangeApplicationDomainOperationRetrieveResponse:
        """
        Use this API to retrieve a single change application domain operation by its ID.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

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
            f"/api/v2/architecture/changeApplicationDomainOperations/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ChangeApplicationDomainOperationRetrieveResponse,
        )


class ChangeApplicationDomainOperationsResourceWithRawResponse:
    def __init__(self, change_application_domain_operations: ChangeApplicationDomainOperationsResource) -> None:
        self._change_application_domain_operations = change_application_domain_operations

        self.create = to_raw_response_wrapper(
            change_application_domain_operations.create,
        )
        self.retrieve = to_raw_response_wrapper(
            change_application_domain_operations.retrieve,
        )


class AsyncChangeApplicationDomainOperationsResourceWithRawResponse:
    def __init__(self, change_application_domain_operations: AsyncChangeApplicationDomainOperationsResource) -> None:
        self._change_application_domain_operations = change_application_domain_operations

        self.create = async_to_raw_response_wrapper(
            change_application_domain_operations.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            change_application_domain_operations.retrieve,
        )


class ChangeApplicationDomainOperationsResourceWithStreamingResponse:
    def __init__(self, change_application_domain_operations: ChangeApplicationDomainOperationsResource) -> None:
        self._change_application_domain_operations = change_application_domain_operations

        self.create = to_streamed_response_wrapper(
            change_application_domain_operations.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            change_application_domain_operations.retrieve,
        )


class AsyncChangeApplicationDomainOperationsResourceWithStreamingResponse:
    def __init__(self, change_application_domain_operations: AsyncChangeApplicationDomainOperationsResource) -> None:
        self._change_application_domain_operations = change_application_domain_operations

        self.create = async_to_streamed_response_wrapper(
            change_application_domain_operations.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            change_application_domain_operations.retrieve,
        )
