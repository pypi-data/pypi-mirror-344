# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal.types.api.v2.architecture.configuration_template import (
    SolaceQueueListResponse,
    SolaceQueueConfigurationTemplateResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSolaceQueues:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: EventPortal) -> None:
        solace_queue = client.api.v2.architecture.configuration_template.solace_queues.create()
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: EventPortal) -> None:
        solace_queue = client.api.v2.architecture.configuration_template.solace_queues.create(
            description="This is a configuration template to be used when deploying to environments",
            name="My First Configuration Template",
            type="type",
            value={
                "0": {},
                "1": {},
                "2": {},
                "3": {},
                "4": {},
                "5": {},
                "6": {},
                "7": {},
                "8": {},
                "9": {},
                "10": {},
                "11": {},
                "12": {},
                "13": {},
                "14": {},
                "15": {},
                "16": {},
                "17": {},
                "18": {},
                "19": {},
                "20": {},
                "21": {},
                "22": {},
                "23": {},
                "24": {},
                "25": {},
                "26": {},
                "27": {},
                "28": {},
                "29": {},
                "30": {},
                "31": {},
                "32": {},
                "33": {},
                "34": {},
                "35": {},
            },
        )
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solace_queue = response.parse()
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with (
            client.api.v2.architecture.configuration_template.solace_queues.with_streaming_response.create()
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solace_queue = response.parse()
            assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        solace_queue = client.api.v2.architecture.configuration_template.solace_queues.retrieve(
            "id",
        )
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solace_queue = response.parse()
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.configuration_template.solace_queues.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solace_queue = response.parse()
            assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: EventPortal) -> None:
        solace_queue = client.api.v2.architecture.configuration_template.solace_queues.update(
            id="id",
        )
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: EventPortal) -> None:
        solace_queue = client.api.v2.architecture.configuration_template.solace_queues.update(
            id="id",
            description="This is a configuration template to be used when deploying to environments",
            name="My First Configuration Template",
            type="type",
            value={
                "0": {},
                "1": {},
                "2": {},
                "3": {},
                "4": {},
                "5": {},
                "6": {},
                "7": {},
                "8": {},
                "9": {},
                "10": {},
                "11": {},
                "12": {},
                "13": {},
                "14": {},
                "15": {},
                "16": {},
                "17": {},
                "18": {},
                "19": {},
                "20": {},
                "21": {},
                "22": {},
                "23": {},
                "24": {},
                "25": {},
                "26": {},
                "27": {},
                "28": {},
                "29": {},
                "30": {},
                "31": {},
                "32": {},
                "33": {},
                "34": {},
                "35": {},
            },
        )
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solace_queue = response.parse()
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: EventPortal) -> None:
        with client.api.v2.architecture.configuration_template.solace_queues.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solace_queue = response.parse()
            assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.update(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        solace_queue = client.api.v2.architecture.configuration_template.solace_queues.list()
        assert_matches_type(SolaceQueueListResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        solace_queue = client.api.v2.architecture.configuration_template.solace_queues.list(
            ids=["string"],
            name="name",
            page_number=1,
            page_size=1,
            sort="sort",
        )
        assert_matches_type(SolaceQueueListResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solace_queue = response.parse()
        assert_matches_type(SolaceQueueListResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.configuration_template.solace_queues.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solace_queue = response.parse()
            assert_matches_type(SolaceQueueListResponse, solace_queue, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: EventPortal) -> None:
        solace_queue = client.api.v2.architecture.configuration_template.solace_queues.delete(
            "id",
        )
        assert solace_queue is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solace_queue = response.parse()
        assert solace_queue is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: EventPortal) -> None:
        with client.api.v2.architecture.configuration_template.solace_queues.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solace_queue = response.parse()
            assert solace_queue is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.delete(
                "",
            )


class TestAsyncSolaceQueues:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        solace_queue = await async_client.api.v2.architecture.configuration_template.solace_queues.create()
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEventPortal) -> None:
        solace_queue = await async_client.api.v2.architecture.configuration_template.solace_queues.create(
            description="This is a configuration template to be used when deploying to environments",
            name="My First Configuration Template",
            type="type",
            value={
                "0": {},
                "1": {},
                "2": {},
                "3": {},
                "4": {},
                "5": {},
                "6": {},
                "7": {},
                "8": {},
                "9": {},
                "10": {},
                "11": {},
                "12": {},
                "13": {},
                "14": {},
                "15": {},
                "16": {},
                "17": {},
                "18": {},
                "19": {},
                "20": {},
                "21": {},
                "22": {},
                "23": {},
                "24": {},
                "25": {},
                "26": {},
                "27": {},
                "28": {},
                "29": {},
                "30": {},
                "31": {},
                "32": {},
                "33": {},
                "34": {},
                "35": {},
            },
        )
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = (
            await async_client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.create()
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solace_queue = await response.parse()
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with (
            async_client.api.v2.architecture.configuration_template.solace_queues.with_streaming_response.create()
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solace_queue = await response.parse()
            assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        solace_queue = await async_client.api.v2.architecture.configuration_template.solace_queues.retrieve(
            "id",
        )
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = (
            await async_client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.retrieve(
                "id",
            )
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solace_queue = await response.parse()
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with (
            async_client.api.v2.architecture.configuration_template.solace_queues.with_streaming_response.retrieve(
                "id",
            )
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solace_queue = await response.parse()
            assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncEventPortal) -> None:
        solace_queue = await async_client.api.v2.architecture.configuration_template.solace_queues.update(
            id="id",
        )
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEventPortal) -> None:
        solace_queue = await async_client.api.v2.architecture.configuration_template.solace_queues.update(
            id="id",
            description="This is a configuration template to be used when deploying to environments",
            name="My First Configuration Template",
            type="type",
            value={
                "0": {},
                "1": {},
                "2": {},
                "3": {},
                "4": {},
                "5": {},
                "6": {},
                "7": {},
                "8": {},
                "9": {},
                "10": {},
                "11": {},
                "12": {},
                "13": {},
                "14": {},
                "15": {},
                "16": {},
                "17": {},
                "18": {},
                "19": {},
                "20": {},
                "21": {},
                "22": {},
                "23": {},
                "24": {},
                "25": {},
                "26": {},
                "27": {},
                "28": {},
                "29": {},
                "30": {},
                "31": {},
                "32": {},
                "33": {},
                "34": {},
                "35": {},
            },
        )
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solace_queue = await response.parse()
        assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.configuration_template.solace_queues.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solace_queue = await response.parse()
            assert_matches_type(SolaceQueueConfigurationTemplateResponse, solace_queue, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.update(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        solace_queue = await async_client.api.v2.architecture.configuration_template.solace_queues.list()
        assert_matches_type(SolaceQueueListResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        solace_queue = await async_client.api.v2.architecture.configuration_template.solace_queues.list(
            ids=["string"],
            name="name",
            page_number=1,
            page_size=1,
            sort="sort",
        )
        assert_matches_type(SolaceQueueListResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solace_queue = await response.parse()
        assert_matches_type(SolaceQueueListResponse, solace_queue, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with (
            async_client.api.v2.architecture.configuration_template.solace_queues.with_streaming_response.list()
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solace_queue = await response.parse()
            assert_matches_type(SolaceQueueListResponse, solace_queue, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncEventPortal) -> None:
        solace_queue = await async_client.api.v2.architecture.configuration_template.solace_queues.delete(
            "id",
        )
        assert solace_queue is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        solace_queue = await response.parse()
        assert solace_queue is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.configuration_template.solace_queues.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            solace_queue = await response.parse()
            assert solace_queue is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.configuration_template.solace_queues.with_raw_response.delete(
                "",
            )
