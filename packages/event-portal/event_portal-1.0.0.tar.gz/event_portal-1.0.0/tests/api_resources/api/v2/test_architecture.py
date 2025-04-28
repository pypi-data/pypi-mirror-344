# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal.types.api.v2 import ArchitectureGetStatesResponse, ArchitectureGetEventPortalUsageStatsResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestArchitecture:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_delete_event_api_product_mem_association(self, client: EventPortal) -> None:
        architecture = client.api.v2.architecture.delete_event_api_product_mem_association(
            "memAssociationId",
        )
        assert architecture is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete_event_api_product_mem_association(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.with_raw_response.delete_event_api_product_mem_association(
            "memAssociationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        architecture = response.parse()
        assert architecture is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete_event_api_product_mem_association(self, client: EventPortal) -> None:
        with client.api.v2.architecture.with_streaming_response.delete_event_api_product_mem_association(
            "memAssociationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            architecture = response.parse()
            assert architecture is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete_event_api_product_mem_association(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `mem_association_id` but received ''"):
            client.api.v2.architecture.with_raw_response.delete_event_api_product_mem_association(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_event_portal_usage_stats(self, client: EventPortal) -> None:
        architecture = client.api.v2.architecture.get_event_portal_usage_stats()
        assert_matches_type(ArchitectureGetEventPortalUsageStatsResponse, architecture, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_event_portal_usage_stats(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.with_raw_response.get_event_portal_usage_stats()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        architecture = response.parse()
        assert_matches_type(ArchitectureGetEventPortalUsageStatsResponse, architecture, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_event_portal_usage_stats(self, client: EventPortal) -> None:
        with client.api.v2.architecture.with_streaming_response.get_event_portal_usage_stats() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            architecture = response.parse()
            assert_matches_type(ArchitectureGetEventPortalUsageStatsResponse, architecture, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_get_states(self, client: EventPortal) -> None:
        architecture = client.api.v2.architecture.get_states()
        assert_matches_type(ArchitectureGetStatesResponse, architecture, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_states(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.with_raw_response.get_states()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        architecture = response.parse()
        assert_matches_type(ArchitectureGetStatesResponse, architecture, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_states(self, client: EventPortal) -> None:
        with client.api.v2.architecture.with_streaming_response.get_states() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            architecture = response.parse()
            assert_matches_type(ArchitectureGetStatesResponse, architecture, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncArchitecture:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete_event_api_product_mem_association(self, async_client: AsyncEventPortal) -> None:
        architecture = await async_client.api.v2.architecture.delete_event_api_product_mem_association(
            "memAssociationId",
        )
        assert architecture is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete_event_api_product_mem_association(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.with_raw_response.delete_event_api_product_mem_association(
            "memAssociationId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        architecture = await response.parse()
        assert architecture is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete_event_api_product_mem_association(
        self, async_client: AsyncEventPortal
    ) -> None:
        async with async_client.api.v2.architecture.with_streaming_response.delete_event_api_product_mem_association(
            "memAssociationId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            architecture = await response.parse()
            assert architecture is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete_event_api_product_mem_association(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `mem_association_id` but received ''"):
            await async_client.api.v2.architecture.with_raw_response.delete_event_api_product_mem_association(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_event_portal_usage_stats(self, async_client: AsyncEventPortal) -> None:
        architecture = await async_client.api.v2.architecture.get_event_portal_usage_stats()
        assert_matches_type(ArchitectureGetEventPortalUsageStatsResponse, architecture, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_event_portal_usage_stats(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.with_raw_response.get_event_portal_usage_stats()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        architecture = await response.parse()
        assert_matches_type(ArchitectureGetEventPortalUsageStatsResponse, architecture, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_event_portal_usage_stats(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.with_streaming_response.get_event_portal_usage_stats() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            architecture = await response.parse()
            assert_matches_type(ArchitectureGetEventPortalUsageStatsResponse, architecture, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_states(self, async_client: AsyncEventPortal) -> None:
        architecture = await async_client.api.v2.architecture.get_states()
        assert_matches_type(ArchitectureGetStatesResponse, architecture, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_states(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.with_raw_response.get_states()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        architecture = await response.parse()
        assert_matches_type(ArchitectureGetStatesResponse, architecture, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_states(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.with_streaming_response.get_states() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            architecture = await response.parse()
            assert_matches_type(ArchitectureGetStatesResponse, architecture, path=["response"])

        assert cast(Any, response.is_closed) is True
