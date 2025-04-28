# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal.types.api.v2.architecture.event_api_product_versions import (
    MemAssociationCreateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMemAssociations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: EventPortal) -> None:
        mem_association = client.api.v2.architecture.event_api_product_versions.mem_associations.create(
            path_event_api_product_version_id="eventApiProductVersionId",
        )
        assert_matches_type(MemAssociationCreateResponse, mem_association, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: EventPortal) -> None:
        mem_association = client.api.v2.architecture.event_api_product_versions.mem_associations.create(
            path_event_api_product_version_id="eventApiProductVersionId",
            id="id",
            body_event_api_product_version_id="eventApiProductVersionId",
            messaging_service_id="messagingServiceId",
            supported_protocols=["smfc"],
            type="type",
        )
        assert_matches_type(MemAssociationCreateResponse, mem_association, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_product_versions.mem_associations.with_raw_response.create(
            path_event_api_product_version_id="eventApiProductVersionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mem_association = response.parse()
        assert_matches_type(MemAssociationCreateResponse, mem_association, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_product_versions.mem_associations.with_streaming_response.create(
            path_event_api_product_version_id="eventApiProductVersionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mem_association = response.parse()
            assert_matches_type(MemAssociationCreateResponse, mem_association, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create(self, client: EventPortal) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `path_event_api_product_version_id` but received ''"
        ):
            client.api.v2.architecture.event_api_product_versions.mem_associations.with_raw_response.create(
                path_event_api_product_version_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: EventPortal) -> None:
        mem_association = client.api.v2.architecture.event_api_product_versions.mem_associations.delete(
            mem_association_id="memAssociationId",
            event_api_product_version_id="eventApiProductVersionId",
        )
        assert mem_association is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_product_versions.mem_associations.with_raw_response.delete(
            mem_association_id="memAssociationId",
            event_api_product_version_id="eventApiProductVersionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mem_association = response.parse()
        assert mem_association is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_product_versions.mem_associations.with_streaming_response.delete(
            mem_association_id="memAssociationId",
            event_api_product_version_id="eventApiProductVersionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mem_association = response.parse()
            assert mem_association is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: EventPortal) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `event_api_product_version_id` but received ''"
        ):
            client.api.v2.architecture.event_api_product_versions.mem_associations.with_raw_response.delete(
                mem_association_id="memAssociationId",
                event_api_product_version_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `mem_association_id` but received ''"):
            client.api.v2.architecture.event_api_product_versions.mem_associations.with_raw_response.delete(
                mem_association_id="",
                event_api_product_version_id="eventApiProductVersionId",
            )


class TestAsyncMemAssociations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        mem_association = await async_client.api.v2.architecture.event_api_product_versions.mem_associations.create(
            path_event_api_product_version_id="eventApiProductVersionId",
        )
        assert_matches_type(MemAssociationCreateResponse, mem_association, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEventPortal) -> None:
        mem_association = await async_client.api.v2.architecture.event_api_product_versions.mem_associations.create(
            path_event_api_product_version_id="eventApiProductVersionId",
            id="id",
            body_event_api_product_version_id="eventApiProductVersionId",
            messaging_service_id="messagingServiceId",
            supported_protocols=["smfc"],
            type="type",
        )
        assert_matches_type(MemAssociationCreateResponse, mem_association, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = (
            await async_client.api.v2.architecture.event_api_product_versions.mem_associations.with_raw_response.create(
                path_event_api_product_version_id="eventApiProductVersionId",
            )
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mem_association = await response.parse()
        assert_matches_type(MemAssociationCreateResponse, mem_association, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with (
            async_client.api.v2.architecture.event_api_product_versions.mem_associations.with_streaming_response.create(
                path_event_api_product_version_id="eventApiProductVersionId",
            )
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mem_association = await response.parse()
            assert_matches_type(MemAssociationCreateResponse, mem_association, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `path_event_api_product_version_id` but received ''"
        ):
            await async_client.api.v2.architecture.event_api_product_versions.mem_associations.with_raw_response.create(
                path_event_api_product_version_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncEventPortal) -> None:
        mem_association = await async_client.api.v2.architecture.event_api_product_versions.mem_associations.delete(
            mem_association_id="memAssociationId",
            event_api_product_version_id="eventApiProductVersionId",
        )
        assert mem_association is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEventPortal) -> None:
        response = (
            await async_client.api.v2.architecture.event_api_product_versions.mem_associations.with_raw_response.delete(
                mem_association_id="memAssociationId",
                event_api_product_version_id="eventApiProductVersionId",
            )
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        mem_association = await response.parse()
        assert mem_association is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEventPortal) -> None:
        async with (
            async_client.api.v2.architecture.event_api_product_versions.mem_associations.with_streaming_response.delete(
                mem_association_id="memAssociationId",
                event_api_product_version_id="eventApiProductVersionId",
            )
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            mem_association = await response.parse()
            assert mem_association is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `event_api_product_version_id` but received ''"
        ):
            await async_client.api.v2.architecture.event_api_product_versions.mem_associations.with_raw_response.delete(
                mem_association_id="memAssociationId",
                event_api_product_version_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `mem_association_id` but received ''"):
            await async_client.api.v2.architecture.event_api_product_versions.mem_associations.with_raw_response.delete(
                mem_association_id="",
                event_api_product_version_id="eventApiProductVersionId",
            )
