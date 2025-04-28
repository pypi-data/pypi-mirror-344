# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal.types.api.v2.architecture import ApplicationVersionEventAccessRequestsResponse
from event_portal.types.api.v2.architecture.application_versions import (
    EventAccessRequestsListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEventAccessRequests:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: EventPortal) -> None:
        event_access_request = client.api.v2.architecture.application_versions.event_access_requests.create(
            "applicationVersionId",
        )
        assert_matches_type(EventAccessRequestsListResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_versions.event_access_requests.with_raw_response.create(
            "applicationVersionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_request = response.parse()
        assert_matches_type(EventAccessRequestsListResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_versions.event_access_requests.with_streaming_response.create(
            "applicationVersionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_request = response.parse()
            assert_matches_type(EventAccessRequestsListResponse, event_access_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create(self, client: EventPortal) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_version_id` but received ''"
        ):
            client.api.v2.architecture.application_versions.event_access_requests.with_raw_response.create(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        event_access_request = client.api.v2.architecture.application_versions.event_access_requests.list(
            application_version_id="applicationVersionId",
        )
        assert_matches_type(ApplicationVersionEventAccessRequestsResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        event_access_request = client.api.v2.architecture.application_versions.event_access_requests.list(
            application_version_id="applicationVersionId",
            review_statuses=["string"],
        )
        assert_matches_type(ApplicationVersionEventAccessRequestsResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_versions.event_access_requests.with_raw_response.list(
            application_version_id="applicationVersionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_request = response.parse()
        assert_matches_type(ApplicationVersionEventAccessRequestsResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_versions.event_access_requests.with_streaming_response.list(
            application_version_id="applicationVersionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_request = response.parse()
            assert_matches_type(ApplicationVersionEventAccessRequestsResponse, event_access_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: EventPortal) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_version_id` but received ''"
        ):
            client.api.v2.architecture.application_versions.event_access_requests.with_raw_response.list(
                application_version_id="",
            )


class TestAsyncEventAccessRequests:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        event_access_request = await async_client.api.v2.architecture.application_versions.event_access_requests.create(
            "applicationVersionId",
        )
        assert_matches_type(EventAccessRequestsListResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = (
            await async_client.api.v2.architecture.application_versions.event_access_requests.with_raw_response.create(
                "applicationVersionId",
            )
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_request = await response.parse()
        assert_matches_type(EventAccessRequestsListResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with (
            async_client.api.v2.architecture.application_versions.event_access_requests.with_streaming_response.create(
                "applicationVersionId",
            )
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_request = await response.parse()
            assert_matches_type(EventAccessRequestsListResponse, event_access_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_version_id` but received ''"
        ):
            await async_client.api.v2.architecture.application_versions.event_access_requests.with_raw_response.create(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        event_access_request = await async_client.api.v2.architecture.application_versions.event_access_requests.list(
            application_version_id="applicationVersionId",
        )
        assert_matches_type(ApplicationVersionEventAccessRequestsResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_access_request = await async_client.api.v2.architecture.application_versions.event_access_requests.list(
            application_version_id="applicationVersionId",
            review_statuses=["string"],
        )
        assert_matches_type(ApplicationVersionEventAccessRequestsResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = (
            await async_client.api.v2.architecture.application_versions.event_access_requests.with_raw_response.list(
                application_version_id="applicationVersionId",
            )
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_request = await response.parse()
        assert_matches_type(ApplicationVersionEventAccessRequestsResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with (
            async_client.api.v2.architecture.application_versions.event_access_requests.with_streaming_response.list(
                application_version_id="applicationVersionId",
            )
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_request = await response.parse()
            assert_matches_type(ApplicationVersionEventAccessRequestsResponse, event_access_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_version_id` but received ''"
        ):
            await async_client.api.v2.architecture.application_versions.event_access_requests.with_raw_response.list(
                application_version_id="",
            )
