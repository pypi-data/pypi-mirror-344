# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal.types.api.v2.architecture import (
    ChangeApplicationDomainOperationRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestChangeApplicationDomainOperations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: EventPortal) -> None:
        change_application_domain_operation = client.api.v2.architecture.change_application_domain_operations.create()
        assert change_application_domain_operation is None

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: EventPortal) -> None:
        change_application_domain_operation = client.api.v2.architecture.change_application_domain_operations.create(
            entities=[
                {
                    "entity_type": "application",
                    "selected_entity_ids": ["string"],
                }
            ],
            target_app_domain_id="targetAppDomainId",
        )
        assert change_application_domain_operation is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.change_application_domain_operations.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        change_application_domain_operation = response.parse()
        assert change_application_domain_operation is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with (
            client.api.v2.architecture.change_application_domain_operations.with_streaming_response.create()
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            change_application_domain_operation = response.parse()
            assert change_application_domain_operation is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        change_application_domain_operation = client.api.v2.architecture.change_application_domain_operations.retrieve(
            "id",
        )
        assert_matches_type(
            ChangeApplicationDomainOperationRetrieveResponse, change_application_domain_operation, path=["response"]
        )

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.change_application_domain_operations.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        change_application_domain_operation = response.parse()
        assert_matches_type(
            ChangeApplicationDomainOperationRetrieveResponse, change_application_domain_operation, path=["response"]
        )

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.change_application_domain_operations.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            change_application_domain_operation = response.parse()
            assert_matches_type(
                ChangeApplicationDomainOperationRetrieveResponse, change_application_domain_operation, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.change_application_domain_operations.with_raw_response.retrieve(
                "",
            )


class TestAsyncChangeApplicationDomainOperations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        change_application_domain_operation = (
            await async_client.api.v2.architecture.change_application_domain_operations.create()
        )
        assert change_application_domain_operation is None

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEventPortal) -> None:
        change_application_domain_operation = (
            await async_client.api.v2.architecture.change_application_domain_operations.create(
                entities=[
                    {
                        "entity_type": "application",
                        "selected_entity_ids": ["string"],
                    }
                ],
                target_app_domain_id="targetAppDomainId",
            )
        )
        assert change_application_domain_operation is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = (
            await async_client.api.v2.architecture.change_application_domain_operations.with_raw_response.create()
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        change_application_domain_operation = await response.parse()
        assert change_application_domain_operation is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with (
            async_client.api.v2.architecture.change_application_domain_operations.with_streaming_response.create()
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            change_application_domain_operation = await response.parse()
            assert change_application_domain_operation is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        change_application_domain_operation = (
            await async_client.api.v2.architecture.change_application_domain_operations.retrieve(
                "id",
            )
        )
        assert_matches_type(
            ChangeApplicationDomainOperationRetrieveResponse, change_application_domain_operation, path=["response"]
        )

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = (
            await async_client.api.v2.architecture.change_application_domain_operations.with_raw_response.retrieve(
                "id",
            )
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        change_application_domain_operation = await response.parse()
        assert_matches_type(
            ChangeApplicationDomainOperationRetrieveResponse, change_application_domain_operation, path=["response"]
        )

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with (
            async_client.api.v2.architecture.change_application_domain_operations.with_streaming_response.retrieve(
                "id",
            )
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            change_application_domain_operation = await response.parse()
            assert_matches_type(
                ChangeApplicationDomainOperationRetrieveResponse, change_application_domain_operation, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.change_application_domain_operations.with_raw_response.retrieve(
                "",
            )
