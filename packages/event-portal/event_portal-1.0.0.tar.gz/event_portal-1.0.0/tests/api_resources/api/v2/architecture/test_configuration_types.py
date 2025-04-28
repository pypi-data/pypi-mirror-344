# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal.types.api.v2.architecture import (
    ConfigurationTypeListResponse,
    ConfigurationTypeRetrieveResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestConfigurationTypes:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        configuration_type = client.api.v2.architecture.configuration_types.retrieve(
            "id",
        )
        assert_matches_type(ConfigurationTypeRetrieveResponse, configuration_type, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.configuration_types.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        configuration_type = response.parse()
        assert_matches_type(ConfigurationTypeRetrieveResponse, configuration_type, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.configuration_types.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            configuration_type = response.parse()
            assert_matches_type(ConfigurationTypeRetrieveResponse, configuration_type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.configuration_types.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        configuration_type = client.api.v2.architecture.configuration_types.list()
        assert_matches_type(ConfigurationTypeListResponse, configuration_type, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        configuration_type = client.api.v2.architecture.configuration_types.list(
            associated_entity_types=["string"],
            broker_type="brokerType",
            ids=["string"],
            names=["string"],
        )
        assert_matches_type(ConfigurationTypeListResponse, configuration_type, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.configuration_types.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        configuration_type = response.parse()
        assert_matches_type(ConfigurationTypeListResponse, configuration_type, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.configuration_types.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            configuration_type = response.parse()
            assert_matches_type(ConfigurationTypeListResponse, configuration_type, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncConfigurationTypes:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        configuration_type = await async_client.api.v2.architecture.configuration_types.retrieve(
            "id",
        )
        assert_matches_type(ConfigurationTypeRetrieveResponse, configuration_type, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.configuration_types.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        configuration_type = await response.parse()
        assert_matches_type(ConfigurationTypeRetrieveResponse, configuration_type, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.configuration_types.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            configuration_type = await response.parse()
            assert_matches_type(ConfigurationTypeRetrieveResponse, configuration_type, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.configuration_types.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        configuration_type = await async_client.api.v2.architecture.configuration_types.list()
        assert_matches_type(ConfigurationTypeListResponse, configuration_type, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        configuration_type = await async_client.api.v2.architecture.configuration_types.list(
            associated_entity_types=["string"],
            broker_type="brokerType",
            ids=["string"],
            names=["string"],
        )
        assert_matches_type(ConfigurationTypeListResponse, configuration_type, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.configuration_types.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        configuration_type = await response.parse()
        assert_matches_type(ConfigurationTypeListResponse, configuration_type, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.configuration_types.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            configuration_type = await response.parse()
            assert_matches_type(ConfigurationTypeListResponse, configuration_type, path=["response"])

        assert cast(Any, response.is_closed) is True
