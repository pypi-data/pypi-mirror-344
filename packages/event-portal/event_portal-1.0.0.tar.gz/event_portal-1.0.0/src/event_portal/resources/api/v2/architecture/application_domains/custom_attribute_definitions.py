# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable
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
from ......types.api.v2.architecture.application_domains import (
    custom_attribute_definition_list_params,
    custom_attribute_definition_create_params,
    custom_attribute_definition_update_params,
)
from ......types.api.v2.architecture.validation_messages_dto_param import ValidationMessagesDtoParam
from ......types.api.v2.architecture.application_domains.custom_attribute_definition_response import (
    CustomAttributeDefinitionResponse,
)
from ......types.api.v2.architecture.application_domains.custom_attribute_definitions_response import (
    CustomAttributeDefinitionsResponse,
)

__all__ = ["CustomAttributeDefinitionsResource", "AsyncCustomAttributeDefinitionsResource"]


class CustomAttributeDefinitionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CustomAttributeDefinitionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return CustomAttributeDefinitionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CustomAttributeDefinitionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return CustomAttributeDefinitionsResourceWithStreamingResponse(self)

    def create(
        self,
        path_application_domain_id: str,
        *,
        scope: Literal["organization", "applicationDomain"],
        id: str | NotGiven = NOT_GIVEN,
        body_application_domain_id: str | NotGiven = NOT_GIVEN,
        associated_entities: Iterable[custom_attribute_definition_create_params.AssociatedEntity]
        | NotGiven = NOT_GIVEN,
        associated_entity_types: List[str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        validation_messages: ValidationMessagesDtoParam | NotGiven = NOT_GIVEN,
        value_type: Literal["STRING", "LONG_TEXT", "MULTI_STRING_VALUE"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CustomAttributeDefinitionResponse:
        """
        Use this API to create a custom attribute definition for provided application
        domain.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `custom_attribute:create:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_application_domain_id:
            raise ValueError(
                f"Expected a non-empty value for `path_application_domain_id` but received {path_application_domain_id!r}"
            )
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._post(
            f"/api/v2/architecture/applicationDomains/{path_application_domain_id}/customAttributeDefinitions",
            body=maybe_transform(
                {
                    "scope": scope,
                    "id": id,
                    "body_application_domain_id": body_application_domain_id,
                    "associated_entities": associated_entities,
                    "associated_entity_types": associated_entity_types,
                    "name": name,
                    "type": type,
                    "validation_messages": validation_messages,
                    "value_type": value_type,
                },
                custom_attribute_definition_create_params.CustomAttributeDefinitionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CustomAttributeDefinitionResponse,
        )

    def update(
        self,
        custom_attribute_id: str,
        *,
        path_application_domain_id: str,
        scope: Literal["organization", "applicationDomain"],
        id: str | NotGiven = NOT_GIVEN,
        body_application_domain_id: str | NotGiven = NOT_GIVEN,
        associated_entities: Iterable[custom_attribute_definition_update_params.AssociatedEntity]
        | NotGiven = NOT_GIVEN,
        associated_entity_types: List[str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        validation_messages: ValidationMessagesDtoParam | NotGiven = NOT_GIVEN,
        value_type: Literal["STRING", "LONG_TEXT", "MULTI_STRING_VALUE"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CustomAttributeDefinitionResponse:
        """
        Use this API to update a custom attribute definition for provided application
        domain.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `custom_attribute:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_application_domain_id:
            raise ValueError(
                f"Expected a non-empty value for `path_application_domain_id` but received {path_application_domain_id!r}"
            )
        if not custom_attribute_id:
            raise ValueError(
                f"Expected a non-empty value for `custom_attribute_id` but received {custom_attribute_id!r}"
            )
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._patch(
            f"/api/v2/architecture/applicationDomains/{path_application_domain_id}/customAttributeDefinitions/{custom_attribute_id}",
            body=maybe_transform(
                {
                    "scope": scope,
                    "id": id,
                    "body_application_domain_id": body_application_domain_id,
                    "associated_entities": associated_entities,
                    "associated_entity_types": associated_entity_types,
                    "name": name,
                    "type": type,
                    "validation_messages": validation_messages,
                    "value_type": value_type,
                },
                custom_attribute_definition_update_params.CustomAttributeDefinitionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CustomAttributeDefinitionResponse,
        )

    def list(
        self,
        application_domain_id: str,
        *,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CustomAttributeDefinitionsResponse:
        """
        Use this API to get a list of custom attribute definitions that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `custom_attribute:get:*` ]

        Args:
          page_number: The page number to get.

          page_size: The number of custom attribute definitions to get per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_domain_id:
            raise ValueError(
                f"Expected a non-empty value for `application_domain_id` but received {application_domain_id!r}"
            )
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return self._get(
            f"/api/v2/architecture/applicationDomains/{application_domain_id}/customAttributeDefinitions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "page_number": page_number,
                        "page_size": page_size,
                    },
                    custom_attribute_definition_list_params.CustomAttributeDefinitionListParams,
                ),
            ),
            cast_to=CustomAttributeDefinitionsResponse,
        )

    def delete(
        self,
        application_domain_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Use this API to delete a custom attribute definition by given application
        domain.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `custom_attribute:delete:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_domain_id:
            raise ValueError(
                f"Expected a non-empty value for `application_domain_id` but received {application_domain_id!r}"
            )
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v2/architecture/applicationDomains/{application_domain_id}/customAttributeDefinitions",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def delete_by_id(
        self,
        custom_attribute_id: str,
        *,
        application_domain_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Use this API to delete a custom attribute definition of given application
        domain.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `custom_attribute:delete:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_domain_id:
            raise ValueError(
                f"Expected a non-empty value for `application_domain_id` but received {application_domain_id!r}"
            )
        if not custom_attribute_id:
            raise ValueError(
                f"Expected a non-empty value for `custom_attribute_id` but received {custom_attribute_id!r}"
            )
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v2/architecture/applicationDomains/{application_domain_id}/customAttributeDefinitions/{custom_attribute_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncCustomAttributeDefinitionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCustomAttributeDefinitionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCustomAttributeDefinitionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCustomAttributeDefinitionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncCustomAttributeDefinitionsResourceWithStreamingResponse(self)

    async def create(
        self,
        path_application_domain_id: str,
        *,
        scope: Literal["organization", "applicationDomain"],
        id: str | NotGiven = NOT_GIVEN,
        body_application_domain_id: str | NotGiven = NOT_GIVEN,
        associated_entities: Iterable[custom_attribute_definition_create_params.AssociatedEntity]
        | NotGiven = NOT_GIVEN,
        associated_entity_types: List[str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        validation_messages: ValidationMessagesDtoParam | NotGiven = NOT_GIVEN,
        value_type: Literal["STRING", "LONG_TEXT", "MULTI_STRING_VALUE"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CustomAttributeDefinitionResponse:
        """
        Use this API to create a custom attribute definition for provided application
        domain.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `custom_attribute:create:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_application_domain_id:
            raise ValueError(
                f"Expected a non-empty value for `path_application_domain_id` but received {path_application_domain_id!r}"
            )
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._post(
            f"/api/v2/architecture/applicationDomains/{path_application_domain_id}/customAttributeDefinitions",
            body=await async_maybe_transform(
                {
                    "scope": scope,
                    "id": id,
                    "body_application_domain_id": body_application_domain_id,
                    "associated_entities": associated_entities,
                    "associated_entity_types": associated_entity_types,
                    "name": name,
                    "type": type,
                    "validation_messages": validation_messages,
                    "value_type": value_type,
                },
                custom_attribute_definition_create_params.CustomAttributeDefinitionCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CustomAttributeDefinitionResponse,
        )

    async def update(
        self,
        custom_attribute_id: str,
        *,
        path_application_domain_id: str,
        scope: Literal["organization", "applicationDomain"],
        id: str | NotGiven = NOT_GIVEN,
        body_application_domain_id: str | NotGiven = NOT_GIVEN,
        associated_entities: Iterable[custom_attribute_definition_update_params.AssociatedEntity]
        | NotGiven = NOT_GIVEN,
        associated_entity_types: List[str] | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        type: str | NotGiven = NOT_GIVEN,
        validation_messages: ValidationMessagesDtoParam | NotGiven = NOT_GIVEN,
        value_type: Literal["STRING", "LONG_TEXT", "MULTI_STRING_VALUE"] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CustomAttributeDefinitionResponse:
        """
        Use this API to update a custom attribute definition for provided application
        domain.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `custom_attribute:update:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not path_application_domain_id:
            raise ValueError(
                f"Expected a non-empty value for `path_application_domain_id` but received {path_application_domain_id!r}"
            )
        if not custom_attribute_id:
            raise ValueError(
                f"Expected a non-empty value for `custom_attribute_id` but received {custom_attribute_id!r}"
            )
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._patch(
            f"/api/v2/architecture/applicationDomains/{path_application_domain_id}/customAttributeDefinitions/{custom_attribute_id}",
            body=await async_maybe_transform(
                {
                    "scope": scope,
                    "id": id,
                    "body_application_domain_id": body_application_domain_id,
                    "associated_entities": associated_entities,
                    "associated_entity_types": associated_entity_types,
                    "name": name,
                    "type": type,
                    "validation_messages": validation_messages,
                    "value_type": value_type,
                },
                custom_attribute_definition_update_params.CustomAttributeDefinitionUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CustomAttributeDefinitionResponse,
        )

    async def list(
        self,
        application_domain_id: str,
        *,
        page_number: int | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CustomAttributeDefinitionsResponse:
        """
        Use this API to get a list of custom attribute definitions that match the given
        parameters.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `custom_attribute:get:*` ]

        Args:
          page_number: The page number to get.

          page_size: The number of custom attribute definitions to get per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_domain_id:
            raise ValueError(
                f"Expected a non-empty value for `application_domain_id` but received {application_domain_id!r}"
            )
        extra_headers = {"Accept": "application/json;charset=utf-8", **(extra_headers or {})}
        return await self._get(
            f"/api/v2/architecture/applicationDomains/{application_domain_id}/customAttributeDefinitions",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "page_number": page_number,
                        "page_size": page_size,
                    },
                    custom_attribute_definition_list_params.CustomAttributeDefinitionListParams,
                ),
            ),
            cast_to=CustomAttributeDefinitionsResponse,
        )

    async def delete(
        self,
        application_domain_id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Use this API to delete a custom attribute definition by given application
        domain.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `custom_attribute:delete:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_domain_id:
            raise ValueError(
                f"Expected a non-empty value for `application_domain_id` but received {application_domain_id!r}"
            )
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v2/architecture/applicationDomains/{application_domain_id}/customAttributeDefinitions",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def delete_by_id(
        self,
        custom_attribute_id: str,
        *,
        application_domain_id: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Use this API to delete a custom attribute definition of given application
        domain.

        <a href="https://api.solace.dev/cloud/reference/authentication">Token
        Permissions</a>: [ `custom_attribute:delete:*` ]

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not application_domain_id:
            raise ValueError(
                f"Expected a non-empty value for `application_domain_id` but received {application_domain_id!r}"
            )
        if not custom_attribute_id:
            raise ValueError(
                f"Expected a non-empty value for `custom_attribute_id` but received {custom_attribute_id!r}"
            )
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v2/architecture/applicationDomains/{application_domain_id}/customAttributeDefinitions/{custom_attribute_id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class CustomAttributeDefinitionsResourceWithRawResponse:
    def __init__(self, custom_attribute_definitions: CustomAttributeDefinitionsResource) -> None:
        self._custom_attribute_definitions = custom_attribute_definitions

        self.create = to_raw_response_wrapper(
            custom_attribute_definitions.create,
        )
        self.update = to_raw_response_wrapper(
            custom_attribute_definitions.update,
        )
        self.list = to_raw_response_wrapper(
            custom_attribute_definitions.list,
        )
        self.delete = to_raw_response_wrapper(
            custom_attribute_definitions.delete,
        )
        self.delete_by_id = to_raw_response_wrapper(
            custom_attribute_definitions.delete_by_id,
        )


class AsyncCustomAttributeDefinitionsResourceWithRawResponse:
    def __init__(self, custom_attribute_definitions: AsyncCustomAttributeDefinitionsResource) -> None:
        self._custom_attribute_definitions = custom_attribute_definitions

        self.create = async_to_raw_response_wrapper(
            custom_attribute_definitions.create,
        )
        self.update = async_to_raw_response_wrapper(
            custom_attribute_definitions.update,
        )
        self.list = async_to_raw_response_wrapper(
            custom_attribute_definitions.list,
        )
        self.delete = async_to_raw_response_wrapper(
            custom_attribute_definitions.delete,
        )
        self.delete_by_id = async_to_raw_response_wrapper(
            custom_attribute_definitions.delete_by_id,
        )


class CustomAttributeDefinitionsResourceWithStreamingResponse:
    def __init__(self, custom_attribute_definitions: CustomAttributeDefinitionsResource) -> None:
        self._custom_attribute_definitions = custom_attribute_definitions

        self.create = to_streamed_response_wrapper(
            custom_attribute_definitions.create,
        )
        self.update = to_streamed_response_wrapper(
            custom_attribute_definitions.update,
        )
        self.list = to_streamed_response_wrapper(
            custom_attribute_definitions.list,
        )
        self.delete = to_streamed_response_wrapper(
            custom_attribute_definitions.delete,
        )
        self.delete_by_id = to_streamed_response_wrapper(
            custom_attribute_definitions.delete_by_id,
        )


class AsyncCustomAttributeDefinitionsResourceWithStreamingResponse:
    def __init__(self, custom_attribute_definitions: AsyncCustomAttributeDefinitionsResource) -> None:
        self._custom_attribute_definitions = custom_attribute_definitions

        self.create = async_to_streamed_response_wrapper(
            custom_attribute_definitions.create,
        )
        self.update = async_to_streamed_response_wrapper(
            custom_attribute_definitions.update,
        )
        self.list = async_to_streamed_response_wrapper(
            custom_attribute_definitions.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            custom_attribute_definitions.delete,
        )
        self.delete_by_id = async_to_streamed_response_wrapper(
            custom_attribute_definitions.delete_by_id,
        )
