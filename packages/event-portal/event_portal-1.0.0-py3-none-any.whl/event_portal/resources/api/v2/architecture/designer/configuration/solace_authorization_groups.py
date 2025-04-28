# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List
from typing_extensions import Literal

import httpx

from ......._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ......._utils import maybe_transform, async_maybe_transform
from ......._compat import cached_property
from ......._resource import SyncAPIResource, AsyncAPIResource
from ......._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ......._base_client import make_request_options
from .......types.api.v2.architecture.designer.configuration import (
    solace_authorization_group_list_params,
    solace_authorization_group_create_params,
)
from .......types.api.v2.architecture.designer.configuration.configuration_response import ConfigurationResponse
from .......types.api.v2.architecture.designer.configuration.configurations_response import ConfigurationsResponse

__all__ = ["SolaceAuthorizationGroupsResource", "AsyncSolaceAuthorizationGroupsResource"]


class SolaceAuthorizationGroupsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SolaceAuthorizationGroupsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return SolaceAuthorizationGroupsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SolaceAuthorizationGroupsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return SolaceAuthorizationGroupsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        context_id: str,
        entity_id: str,
        context_type: Literal["EVENT_BROKER"] | NotGiven = NOT_GIVEN,
        template_id: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        value: Dict[str, object] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigurationResponse:
        """
        Create an LDAP authorization group configuration for event broker connections in
        an application in Event Portal.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

        Args:
          context_id: The unique identifier of the runtime service the configuration is for.

          entity_id: The unique identifier of the designer entity the configuration is for.

          context_type: The type of runtime service the configuration is for.

          template_id: The unique identifier of the configuration template.

          value: The configuration value in JSON format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._post(
            "/api/v2/architecture/designer/configuration/solaceAuthorizationGroups",
            body=maybe_transform(
                {
                    "context_id": context_id,
                    "entity_id": entity_id,
                    "context_type": context_type,
                    "template_id": template_id,
                    "type": type,
                    "value": value,
                },
                solace_authorization_group_create_params.SolaceAuthorizationGroupCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigurationResponse,
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
    ) -> ConfigurationResponse:
        """
        Get a specific LDAP authorization group configuration for event broker
        connections from an application in Event Portal.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:get:*` ]

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
            f"/api/v2/architecture/designer/configuration/solaceAuthorizationGroups/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigurationResponse,
        )

    def list(
        self,
        *,
        entity_ids: List[str] | NotGiven = NOT_GIVEN,
        event_broker_ids: List[str] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigurationsResponse:
        """
        Get a list of LDAP authorization group configurations for event broker
        connections from an application in Event Portal.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          entity_ids: The unique identifiers of designer entities, separated by commas, to retrieve
              authorization group configurations from.

          event_broker_ids: The unique identifiers of the event brokers, separated by commas, to retrieve
              authorization group configurations from.

          ids: The unique identifiers of the authorization group configurations to retrieve,
              separated by commas.

          page_number: The page number to retrieve.

          page_size: The number of LDAP authorization group configurations to return per page.

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
            "/api/v2/architecture/designer/configuration/solaceAuthorizationGroups",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "entity_ids": entity_ids,
                        "event_broker_ids": event_broker_ids,
                        "ids": ids,
                        "page_number": page_number,
                        "page_size": page_size,
                        "sort": sort,
                    },
                    solace_authorization_group_list_params.SolaceAuthorizationGroupListParams,
                ),
            ),
            cast_to=ConfigurationsResponse,
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
        Delete an LDAP authorization group configuration for event broker connections
        from an application in Event Portal. You can’t undo this operation.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

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
            f"/api/v2/architecture/designer/configuration/solaceAuthorizationGroups/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncSolaceAuthorizationGroupsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSolaceAuthorizationGroupsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSolaceAuthorizationGroupsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSolaceAuthorizationGroupsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncSolaceAuthorizationGroupsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        context_id: str,
        entity_id: str,
        context_type: Literal["EVENT_BROKER"] | NotGiven = NOT_GIVEN,
        template_id: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        value: Dict[str, object] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigurationResponse:
        """
        Create an LDAP authorization group configuration for event broker connections in
        an application in Event Portal.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

        Args:
          context_id: The unique identifier of the runtime service the configuration is for.

          entity_id: The unique identifier of the designer entity the configuration is for.

          context_type: The type of runtime service the configuration is for.

          template_id: The unique identifier of the configuration template.

          value: The configuration value in JSON format.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._post(
            "/api/v2/architecture/designer/configuration/solaceAuthorizationGroups",
            body=await async_maybe_transform(
                {
                    "context_id": context_id,
                    "entity_id": entity_id,
                    "context_type": context_type,
                    "template_id": template_id,
                    "type": type,
                    "value": value,
                },
                solace_authorization_group_create_params.SolaceAuthorizationGroupCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigurationResponse,
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
    ) -> ConfigurationResponse:
        """
        Get a specific LDAP authorization group configuration for event broker
        connections from an application in Event Portal.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:get:*` ]

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
            f"/api/v2/architecture/designer/configuration/solaceAuthorizationGroups/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ConfigurationResponse,
        )

    async def list(
        self,
        *,
        entity_ids: List[str] | NotGiven = NOT_GIVEN,
        event_broker_ids: List[str] | NotGiven = NOT_GIVEN,
        ids: List[str] | NotGiven = NOT_GIVEN,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        sort: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ConfigurationsResponse:
        """
        Get a list of LDAP authorization group configurations for event broker
        connections from an application in Event Portal.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `event_designer:access` ]

        Args:
          entity_ids: The unique identifiers of designer entities, separated by commas, to retrieve
              authorization group configurations from.

          event_broker_ids: The unique identifiers of the event brokers, separated by commas, to retrieve
              authorization group configurations from.

          ids: The unique identifiers of the authorization group configurations to retrieve,
              separated by commas.

          page_number: The page number to retrieve.

          page_size: The number of LDAP authorization group configurations to return per page.

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
            "/api/v2/architecture/designer/configuration/solaceAuthorizationGroups",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "entity_ids": entity_ids,
                        "event_broker_ids": event_broker_ids,
                        "ids": ids,
                        "page_number": page_number,
                        "page_size": page_size,
                        "sort": sort,
                    },
                    solace_authorization_group_list_params.SolaceAuthorizationGroupListParams,
                ),
            ),
            cast_to=ConfigurationsResponse,
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
        Delete an LDAP authorization group configuration for event broker connections
        from an application in Event Portal. You can’t undo this operation.

        Your token must have one of the permissions listed in the Token Permissions.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `application:update:*` ]

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
            f"/api/v2/architecture/designer/configuration/solaceAuthorizationGroups/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class SolaceAuthorizationGroupsResourceWithRawResponse:
    def __init__(self, solace_authorization_groups: SolaceAuthorizationGroupsResource) -> None:
        self._solace_authorization_groups = solace_authorization_groups

        self.create = to_raw_response_wrapper(
            solace_authorization_groups.create,
        )
        self.retrieve = to_raw_response_wrapper(
            solace_authorization_groups.retrieve,
        )
        self.list = to_raw_response_wrapper(
            solace_authorization_groups.list,
        )
        self.delete = to_raw_response_wrapper(
            solace_authorization_groups.delete,
        )


class AsyncSolaceAuthorizationGroupsResourceWithRawResponse:
    def __init__(self, solace_authorization_groups: AsyncSolaceAuthorizationGroupsResource) -> None:
        self._solace_authorization_groups = solace_authorization_groups

        self.create = async_to_raw_response_wrapper(
            solace_authorization_groups.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            solace_authorization_groups.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            solace_authorization_groups.list,
        )
        self.delete = async_to_raw_response_wrapper(
            solace_authorization_groups.delete,
        )


class SolaceAuthorizationGroupsResourceWithStreamingResponse:
    def __init__(self, solace_authorization_groups: SolaceAuthorizationGroupsResource) -> None:
        self._solace_authorization_groups = solace_authorization_groups

        self.create = to_streamed_response_wrapper(
            solace_authorization_groups.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            solace_authorization_groups.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            solace_authorization_groups.list,
        )
        self.delete = to_streamed_response_wrapper(
            solace_authorization_groups.delete,
        )


class AsyncSolaceAuthorizationGroupsResourceWithStreamingResponse:
    def __init__(self, solace_authorization_groups: AsyncSolaceAuthorizationGroupsResource) -> None:
        self._solace_authorization_groups = solace_authorization_groups

        self.create = async_to_streamed_response_wrapper(
            solace_authorization_groups.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            solace_authorization_groups.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            solace_authorization_groups.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            solace_authorization_groups.delete,
        )
