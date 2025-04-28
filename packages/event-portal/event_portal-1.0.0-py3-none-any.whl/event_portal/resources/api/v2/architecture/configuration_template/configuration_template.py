# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ......_compat import cached_property
from .solace_queues import (
    SolaceQueuesResource,
    AsyncSolaceQueuesResource,
    SolaceQueuesResourceWithRawResponse,
    AsyncSolaceQueuesResourceWithRawResponse,
    SolaceQueuesResourceWithStreamingResponse,
    AsyncSolaceQueuesResourceWithStreamingResponse,
)
from ......_resource import SyncAPIResource, AsyncAPIResource
from .solace_client_profile_names import (
    SolaceClientProfileNamesResource,
    AsyncSolaceClientProfileNamesResource,
    SolaceClientProfileNamesResourceWithRawResponse,
    AsyncSolaceClientProfileNamesResourceWithRawResponse,
    SolaceClientProfileNamesResourceWithStreamingResponse,
    AsyncSolaceClientProfileNamesResourceWithStreamingResponse,
)

__all__ = ["ConfigurationTemplateResource", "AsyncConfigurationTemplateResource"]


class ConfigurationTemplateResource(SyncAPIResource):
    @cached_property
    def solace_client_profile_names(self) -> SolaceClientProfileNamesResource:
        return SolaceClientProfileNamesResource(self._client)

    @cached_property
    def solace_queues(self) -> SolaceQueuesResource:
        return SolaceQueuesResource(self._client)

    @cached_property
    def with_raw_response(self) -> ConfigurationTemplateResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return ConfigurationTemplateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConfigurationTemplateResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return ConfigurationTemplateResourceWithStreamingResponse(self)


class AsyncConfigurationTemplateResource(AsyncAPIResource):
    @cached_property
    def solace_client_profile_names(self) -> AsyncSolaceClientProfileNamesResource:
        return AsyncSolaceClientProfileNamesResource(self._client)

    @cached_property
    def solace_queues(self) -> AsyncSolaceQueuesResource:
        return AsyncSolaceQueuesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncConfigurationTemplateResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConfigurationTemplateResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConfigurationTemplateResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncConfigurationTemplateResourceWithStreamingResponse(self)


class ConfigurationTemplateResourceWithRawResponse:
    def __init__(self, configuration_template: ConfigurationTemplateResource) -> None:
        self._configuration_template = configuration_template

    @cached_property
    def solace_client_profile_names(self) -> SolaceClientProfileNamesResourceWithRawResponse:
        return SolaceClientProfileNamesResourceWithRawResponse(self._configuration_template.solace_client_profile_names)

    @cached_property
    def solace_queues(self) -> SolaceQueuesResourceWithRawResponse:
        return SolaceQueuesResourceWithRawResponse(self._configuration_template.solace_queues)


class AsyncConfigurationTemplateResourceWithRawResponse:
    def __init__(self, configuration_template: AsyncConfigurationTemplateResource) -> None:
        self._configuration_template = configuration_template

    @cached_property
    def solace_client_profile_names(self) -> AsyncSolaceClientProfileNamesResourceWithRawResponse:
        return AsyncSolaceClientProfileNamesResourceWithRawResponse(
            self._configuration_template.solace_client_profile_names
        )

    @cached_property
    def solace_queues(self) -> AsyncSolaceQueuesResourceWithRawResponse:
        return AsyncSolaceQueuesResourceWithRawResponse(self._configuration_template.solace_queues)


class ConfigurationTemplateResourceWithStreamingResponse:
    def __init__(self, configuration_template: ConfigurationTemplateResource) -> None:
        self._configuration_template = configuration_template

    @cached_property
    def solace_client_profile_names(self) -> SolaceClientProfileNamesResourceWithStreamingResponse:
        return SolaceClientProfileNamesResourceWithStreamingResponse(
            self._configuration_template.solace_client_profile_names
        )

    @cached_property
    def solace_queues(self) -> SolaceQueuesResourceWithStreamingResponse:
        return SolaceQueuesResourceWithStreamingResponse(self._configuration_template.solace_queues)


class AsyncConfigurationTemplateResourceWithStreamingResponse:
    def __init__(self, configuration_template: AsyncConfigurationTemplateResource) -> None:
        self._configuration_template = configuration_template

    @cached_property
    def solace_client_profile_names(self) -> AsyncSolaceClientProfileNamesResourceWithStreamingResponse:
        return AsyncSolaceClientProfileNamesResourceWithStreamingResponse(
            self._configuration_template.solace_client_profile_names
        )

    @cached_property
    def solace_queues(self) -> AsyncSolaceQueuesResourceWithStreamingResponse:
        return AsyncSolaceQueuesResourceWithStreamingResponse(self._configuration_template.solace_queues)
