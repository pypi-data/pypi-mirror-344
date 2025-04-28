# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

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
from ......types.api.v2.architecture.event_api_product_versions import mem_association_create_params
from ......types.api.v2.architecture.event_api_product_versions.mem_association_create_response import (
    MemAssociationCreateResponse,
)

__all__ = ["MemAssociationsResource", "AsyncMemAssociationsResource"]


class MemAssociationsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MemAssociationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return MemAssociationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MemAssociationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return MemAssociationsResourceWithStreamingResponse(self)

    def create(
        self,
        path_event_api_product_version_id: str,
        *,
        id: str | NotGiven = NOT_GIVEN,
        body_event_api_product_version_id: str | NotGiven = NOT_GIVEN,
        messaging_service_id: str | NotGiven = NOT_GIVEN,
        supported_protocols: List[
            Literal[
                "smfc",
                "smf",
                "smfs",
                "amqp",
                "amqps",
                "mqtt",
                "mqtts",
                "mqttws",
                "mqttwss",
                "secure-mqtt",
                "secure-mqttws",
                "rest",
                "rests",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MemAssociationCreateResponse:
        """
        Use this API to associate an Event API Product version and gateway messaging
        service.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_event_api_product_version_id:
            raise ValueError(
                f"Expected a non-empty value for `path_event_api_product_version_id` but received {path_event_api_product_version_id!r}"
            )
        return self._post(
            f"/api/v2/architecture/eventApiProductVersions/{path_event_api_product_version_id}/memAssociations",
            body=maybe_transform(
                {
                    "id": id,
                    "body_event_api_product_version_id": body_event_api_product_version_id,
                    "messaging_service_id": messaging_service_id,
                    "supported_protocols": supported_protocols,
                    "type": type,
                },
                mem_association_create_params.MemAssociationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemAssociationCreateResponse,
        )

    def delete(
        self,
        mem_association_id: str,
        *,
        event_api_product_version_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Use this API to disassociate an Event API Product version and gateway messaging
        service.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not event_api_product_version_id:
            raise ValueError(
                f"Expected a non-empty value for `event_api_product_version_id` but received {event_api_product_version_id!r}"
            )
        if not mem_association_id:
            raise ValueError(f"Expected a non-empty value for `mem_association_id` but received {mem_association_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v2/architecture/eventApiProductVersions/{event_api_product_version_id}/memAssociations/{mem_association_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncMemAssociationsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMemAssociationsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMemAssociationsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMemAssociationsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncMemAssociationsResourceWithStreamingResponse(self)

    async def create(
        self,
        path_event_api_product_version_id: str,
        *,
        id: str | NotGiven = NOT_GIVEN,
        body_event_api_product_version_id: str | NotGiven = NOT_GIVEN,
        messaging_service_id: str | NotGiven = NOT_GIVEN,
        supported_protocols: List[
            Literal[
                "smfc",
                "smf",
                "smfs",
                "amqp",
                "amqps",
                "mqtt",
                "mqtts",
                "mqttws",
                "mqttwss",
                "secure-mqtt",
                "secure-mqttws",
                "rest",
                "rests",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> MemAssociationCreateResponse:
        """
        Use this API to associate an Event API Product version and gateway messaging
        service.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_event_api_product_version_id:
            raise ValueError(
                f"Expected a non-empty value for `path_event_api_product_version_id` but received {path_event_api_product_version_id!r}"
            )
        return await self._post(
            f"/api/v2/architecture/eventApiProductVersions/{path_event_api_product_version_id}/memAssociations",
            body=await async_maybe_transform(
                {
                    "id": id,
                    "body_event_api_product_version_id": body_event_api_product_version_id,
                    "messaging_service_id": messaging_service_id,
                    "supported_protocols": supported_protocols,
                    "type": type,
                },
                mem_association_create_params.MemAssociationCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=MemAssociationCreateResponse,
        )

    async def delete(
        self,
        mem_association_id: str,
        *,
        event_api_product_version_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Use this API to disassociate an Event API Product version and gateway messaging
        service.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_api_product:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not event_api_product_version_id:
            raise ValueError(
                f"Expected a non-empty value for `event_api_product_version_id` but received {event_api_product_version_id!r}"
            )
        if not mem_association_id:
            raise ValueError(f"Expected a non-empty value for `mem_association_id` but received {mem_association_id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v2/architecture/eventApiProductVersions/{event_api_product_version_id}/memAssociations/{mem_association_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class MemAssociationsResourceWithRawResponse:
    def __init__(self, mem_associations: MemAssociationsResource) -> None:
        self._mem_associations = mem_associations

        self.create = to_raw_response_wrapper(
            mem_associations.create,
        )
        self.delete = to_raw_response_wrapper(
            mem_associations.delete,
        )


class AsyncMemAssociationsResourceWithRawResponse:
    def __init__(self, mem_associations: AsyncMemAssociationsResource) -> None:
        self._mem_associations = mem_associations

        self.create = async_to_raw_response_wrapper(
            mem_associations.create,
        )
        self.delete = async_to_raw_response_wrapper(
            mem_associations.delete,
        )


class MemAssociationsResourceWithStreamingResponse:
    def __init__(self, mem_associations: MemAssociationsResource) -> None:
        self._mem_associations = mem_associations

        self.create = to_streamed_response_wrapper(
            mem_associations.create,
        )
        self.delete = to_streamed_response_wrapper(
            mem_associations.delete,
        )


class AsyncMemAssociationsResourceWithStreamingResponse:
    def __init__(self, mem_associations: AsyncMemAssociationsResource) -> None:
        self._mem_associations = mem_associations

        self.create = async_to_streamed_response_wrapper(
            mem_associations.create,
        )
        self.delete = async_to_streamed_response_wrapper(
            mem_associations.delete,
        )
