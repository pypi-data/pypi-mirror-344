# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ......._compat import cached_property
from .solace_queues import (
    SolaceQueuesResource,
    AsyncSolaceQueuesResource,
    SolaceQueuesResourceWithRawResponse,
    AsyncSolaceQueuesResourceWithRawResponse,
    SolaceQueuesResourceWithStreamingResponse,
    AsyncSolaceQueuesResourceWithStreamingResponse,
)
from ......._resource import SyncAPIResource, AsyncAPIResource
from .solace_client_usernames import (
    SolaceClientUsernamesResource,
    AsyncSolaceClientUsernamesResource,
    SolaceClientUsernamesResourceWithRawResponse,
    AsyncSolaceClientUsernamesResourceWithRawResponse,
    SolaceClientUsernamesResourceWithStreamingResponse,
    AsyncSolaceClientUsernamesResourceWithStreamingResponse,
)
from .solace_authorization_groups import (
    SolaceAuthorizationGroupsResource,
    AsyncSolaceAuthorizationGroupsResource,
    SolaceAuthorizationGroupsResourceWithRawResponse,
    AsyncSolaceAuthorizationGroupsResourceWithRawResponse,
    SolaceAuthorizationGroupsResourceWithStreamingResponse,
    AsyncSolaceAuthorizationGroupsResourceWithStreamingResponse,
)
from .solace_client_profile_names import (
    SolaceClientProfileNamesResource,
    AsyncSolaceClientProfileNamesResource,
    SolaceClientProfileNamesResourceWithRawResponse,
    AsyncSolaceClientProfileNamesResourceWithRawResponse,
    SolaceClientProfileNamesResourceWithStreamingResponse,
    AsyncSolaceClientProfileNamesResourceWithStreamingResponse,
)

__all__ = ["ConfigurationResource", "AsyncConfigurationResource"]


class ConfigurationResource(SyncAPIResource):
    @cached_property
    def solace_authorization_groups(self) -> SolaceAuthorizationGroupsResource:
        return SolaceAuthorizationGroupsResource(self._client)

    @cached_property
    def solace_client_profile_names(self) -> SolaceClientProfileNamesResource:
        return SolaceClientProfileNamesResource(self._client)

    @cached_property
    def solace_client_usernames(self) -> SolaceClientUsernamesResource:
        return SolaceClientUsernamesResource(self._client)

    @cached_property
    def solace_queues(self) -> SolaceQueuesResource:
        return SolaceQueuesResource(self._client)

    @cached_property
    def with_raw_response(self) -> ConfigurationResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return ConfigurationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ConfigurationResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return ConfigurationResourceWithStreamingResponse(self)


class AsyncConfigurationResource(AsyncAPIResource):
    @cached_property
    def solace_authorization_groups(self) -> AsyncSolaceAuthorizationGroupsResource:
        return AsyncSolaceAuthorizationGroupsResource(self._client)

    @cached_property
    def solace_client_profile_names(self) -> AsyncSolaceClientProfileNamesResource:
        return AsyncSolaceClientProfileNamesResource(self._client)

    @cached_property
    def solace_client_usernames(self) -> AsyncSolaceClientUsernamesResource:
        return AsyncSolaceClientUsernamesResource(self._client)

    @cached_property
    def solace_queues(self) -> AsyncSolaceQueuesResource:
        return AsyncSolaceQueuesResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncConfigurationResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncConfigurationResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncConfigurationResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncConfigurationResourceWithStreamingResponse(self)


class ConfigurationResourceWithRawResponse:
    def __init__(self, configuration: ConfigurationResource) -> None:
        self._configuration = configuration

    @cached_property
    def solace_authorization_groups(self) -> SolaceAuthorizationGroupsResourceWithRawResponse:
        return SolaceAuthorizationGroupsResourceWithRawResponse(self._configuration.solace_authorization_groups)

    @cached_property
    def solace_client_profile_names(self) -> SolaceClientProfileNamesResourceWithRawResponse:
        return SolaceClientProfileNamesResourceWithRawResponse(self._configuration.solace_client_profile_names)

    @cached_property
    def solace_client_usernames(self) -> SolaceClientUsernamesResourceWithRawResponse:
        return SolaceClientUsernamesResourceWithRawResponse(self._configuration.solace_client_usernames)

    @cached_property
    def solace_queues(self) -> SolaceQueuesResourceWithRawResponse:
        return SolaceQueuesResourceWithRawResponse(self._configuration.solace_queues)


class AsyncConfigurationResourceWithRawResponse:
    def __init__(self, configuration: AsyncConfigurationResource) -> None:
        self._configuration = configuration

    @cached_property
    def solace_authorization_groups(self) -> AsyncSolaceAuthorizationGroupsResourceWithRawResponse:
        return AsyncSolaceAuthorizationGroupsResourceWithRawResponse(self._configuration.solace_authorization_groups)

    @cached_property
    def solace_client_profile_names(self) -> AsyncSolaceClientProfileNamesResourceWithRawResponse:
        return AsyncSolaceClientProfileNamesResourceWithRawResponse(self._configuration.solace_client_profile_names)

    @cached_property
    def solace_client_usernames(self) -> AsyncSolaceClientUsernamesResourceWithRawResponse:
        return AsyncSolaceClientUsernamesResourceWithRawResponse(self._configuration.solace_client_usernames)

    @cached_property
    def solace_queues(self) -> AsyncSolaceQueuesResourceWithRawResponse:
        return AsyncSolaceQueuesResourceWithRawResponse(self._configuration.solace_queues)


class ConfigurationResourceWithStreamingResponse:
    def __init__(self, configuration: ConfigurationResource) -> None:
        self._configuration = configuration

    @cached_property
    def solace_authorization_groups(self) -> SolaceAuthorizationGroupsResourceWithStreamingResponse:
        return SolaceAuthorizationGroupsResourceWithStreamingResponse(self._configuration.solace_authorization_groups)

    @cached_property
    def solace_client_profile_names(self) -> SolaceClientProfileNamesResourceWithStreamingResponse:
        return SolaceClientProfileNamesResourceWithStreamingResponse(self._configuration.solace_client_profile_names)

    @cached_property
    def solace_client_usernames(self) -> SolaceClientUsernamesResourceWithStreamingResponse:
        return SolaceClientUsernamesResourceWithStreamingResponse(self._configuration.solace_client_usernames)

    @cached_property
    def solace_queues(self) -> SolaceQueuesResourceWithStreamingResponse:
        return SolaceQueuesResourceWithStreamingResponse(self._configuration.solace_queues)


class AsyncConfigurationResourceWithStreamingResponse:
    def __init__(self, configuration: AsyncConfigurationResource) -> None:
        self._configuration = configuration

    @cached_property
    def solace_authorization_groups(self) -> AsyncSolaceAuthorizationGroupsResourceWithStreamingResponse:
        return AsyncSolaceAuthorizationGroupsResourceWithStreamingResponse(
            self._configuration.solace_authorization_groups
        )

    @cached_property
    def solace_client_profile_names(self) -> AsyncSolaceClientProfileNamesResourceWithStreamingResponse:
        return AsyncSolaceClientProfileNamesResourceWithStreamingResponse(
            self._configuration.solace_client_profile_names
        )

    @cached_property
    def solace_client_usernames(self) -> AsyncSolaceClientUsernamesResourceWithStreamingResponse:
        return AsyncSolaceClientUsernamesResourceWithStreamingResponse(self._configuration.solace_client_usernames)

    @cached_property
    def solace_queues(self) -> AsyncSolaceQueuesResourceWithStreamingResponse:
        return AsyncSolaceQueuesResourceWithStreamingResponse(self._configuration.solace_queues)
