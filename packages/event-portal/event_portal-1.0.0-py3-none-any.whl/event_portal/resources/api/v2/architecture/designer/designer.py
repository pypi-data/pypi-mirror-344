# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from ......_compat import cached_property
from ......_resource import SyncAPIResource, AsyncAPIResource
from .configuration.configuration import (
    ConfigurationResource,
    AsyncConfigurationResource,
    ConfigurationResourceWithRawResponse,
    AsyncConfigurationResourceWithRawResponse,
    ConfigurationResourceWithStreamingResponse,
    AsyncConfigurationResourceWithStreamingResponse,
)

__all__ = ["DesignerResource", "AsyncDesignerResource"]


class DesignerResource(SyncAPIResource):
    @cached_property
    def configuration(self) -> ConfigurationResource:
        return ConfigurationResource(self._client)

    @cached_property
    def with_raw_response(self) -> DesignerResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return DesignerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DesignerResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return DesignerResourceWithStreamingResponse(self)


class AsyncDesignerResource(AsyncAPIResource):
    @cached_property
    def configuration(self) -> AsyncConfigurationResource:
        return AsyncConfigurationResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncDesignerResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDesignerResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDesignerResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ghaithdallaali/event-portal-python#with_streaming_response
        """
        return AsyncDesignerResourceWithStreamingResponse(self)


class DesignerResourceWithRawResponse:
    def __init__(self, designer: DesignerResource) -> None:
        self._designer = designer

    @cached_property
    def configuration(self) -> ConfigurationResourceWithRawResponse:
        return ConfigurationResourceWithRawResponse(self._designer.configuration)


class AsyncDesignerResourceWithRawResponse:
    def __init__(self, designer: AsyncDesignerResource) -> None:
        self._designer = designer

    @cached_property
    def configuration(self) -> AsyncConfigurationResourceWithRawResponse:
        return AsyncConfigurationResourceWithRawResponse(self._designer.configuration)


class DesignerResourceWithStreamingResponse:
    def __init__(self, designer: DesignerResource) -> None:
        self._designer = designer

    @cached_property
    def configuration(self) -> ConfigurationResourceWithStreamingResponse:
        return ConfigurationResourceWithStreamingResponse(self._designer.configuration)


class AsyncDesignerResourceWithStreamingResponse:
    def __init__(self, designer: AsyncDesignerResource) -> None:
        self._designer = designer

    @cached_property
    def configuration(self) -> AsyncConfigurationResourceWithStreamingResponse:
        return AsyncConfigurationResourceWithStreamingResponse(self._designer.configuration)
