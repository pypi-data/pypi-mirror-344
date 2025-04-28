# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)
from event_portal.types.api.v2.architecture import (
    ConsumerResponse,
    ConsumerListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestConsumers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.post("/api/v2/architecture/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        consumer = client.api.v2.architecture.consumers.create(
            application_version_id="acb2j5k3mly",
        )
        assert consumer.is_closed
        assert consumer.json() == {"foo": "bar"}
        assert cast(Any, consumer.is_closed) is True
        assert isinstance(consumer, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_create_with_all_params(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.post("/api/v2/architecture/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        consumer = client.api.v2.architecture.consumers.create(
            application_version_id="acb2j5k3mly",
            broker_type="solace",
            consumer_type="eventQueue",
            name="My First Consumer",
            subscriptions=[
                {
                    "subscription_type": "topic",
                    "value": "solace/cloud",
                }
            ],
            type="type",
        )
        assert consumer.is_closed
        assert consumer.json() == {"foo": "bar"}
        assert cast(Any, consumer.is_closed) is True
        assert isinstance(consumer, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_create(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.post("/api/v2/architecture/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        consumer = client.api.v2.architecture.consumers.with_raw_response.create(
            application_version_id="acb2j5k3mly",
        )

        assert consumer.is_closed is True
        assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert consumer.json() == {"foo": "bar"}
        assert isinstance(consumer, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_create(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.post("/api/v2/architecture/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.api.v2.architecture.consumers.with_streaming_response.create(
            application_version_id="acb2j5k3mly",
        ) as consumer:
            assert not consumer.is_closed
            assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert consumer.json() == {"foo": "bar"}
            assert cast(Any, consumer.is_closed) is True
            assert isinstance(consumer, StreamedBinaryAPIResponse)

        assert cast(Any, consumer.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        consumer = client.api.v2.architecture.consumers.retrieve(
            "id",
        )
        assert_matches_type(ConsumerResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.consumers.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        consumer = response.parse()
        assert_matches_type(ConsumerResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.consumers.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            consumer = response.parse()
            assert_matches_type(ConsumerResponse, consumer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.consumers.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: EventPortal) -> None:
        consumer = client.api.v2.architecture.consumers.update(
            id="id",
            application_version_id="acb2j5k3mly",
        )
        assert_matches_type(ConsumerResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: EventPortal) -> None:
        consumer = client.api.v2.architecture.consumers.update(
            id="id",
            application_version_id="acb2j5k3mly",
            broker_type="solace",
            consumer_type="eventQueue",
            name="My First Consumer",
            subscriptions=[
                {
                    "subscription_type": "topic",
                    "value": "solace/cloud",
                }
            ],
            type="type",
        )
        assert_matches_type(ConsumerResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.consumers.with_raw_response.update(
            id="id",
            application_version_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        consumer = response.parse()
        assert_matches_type(ConsumerResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: EventPortal) -> None:
        with client.api.v2.architecture.consumers.with_streaming_response.update(
            id="id",
            application_version_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            consumer = response.parse()
            assert_matches_type(ConsumerResponse, consumer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.consumers.with_raw_response.update(
                id="",
                application_version_id="acb2j5k3mly",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        consumer = client.api.v2.architecture.consumers.list()
        assert_matches_type(ConsumerListResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        consumer = client.api.v2.architecture.consumers.list(
            application_version_ids=["string"],
            ids=["string"],
            page_number=1,
            page_size=1,
        )
        assert_matches_type(ConsumerListResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.consumers.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        consumer = response.parse()
        assert_matches_type(ConsumerListResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.consumers.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            consumer = response.parse()
            assert_matches_type(ConsumerListResponse, consumer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: EventPortal) -> None:
        consumer = client.api.v2.architecture.consumers.delete(
            "id",
        )
        assert consumer is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.consumers.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        consumer = response.parse()
        assert consumer is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: EventPortal) -> None:
        with client.api.v2.architecture.consumers.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            consumer = response.parse()
            assert consumer is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.consumers.with_raw_response.delete(
                "",
            )


class TestAsyncConsumers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.post("/api/v2/architecture/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        consumer = await async_client.api.v2.architecture.consumers.create(
            application_version_id="acb2j5k3mly",
        )
        assert consumer.is_closed
        assert await consumer.json() == {"foo": "bar"}
        assert cast(Any, consumer.is_closed) is True
        assert isinstance(consumer, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_create_with_all_params(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.post("/api/v2/architecture/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        consumer = await async_client.api.v2.architecture.consumers.create(
            application_version_id="acb2j5k3mly",
            broker_type="solace",
            consumer_type="eventQueue",
            name="My First Consumer",
            subscriptions=[
                {
                    "subscription_type": "topic",
                    "value": "solace/cloud",
                }
            ],
            type="type",
        )
        assert consumer.is_closed
        assert await consumer.json() == {"foo": "bar"}
        assert cast(Any, consumer.is_closed) is True
        assert isinstance(consumer, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_create(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.post("/api/v2/architecture/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        consumer = await async_client.api.v2.architecture.consumers.with_raw_response.create(
            application_version_id="acb2j5k3mly",
        )

        assert consumer.is_closed is True
        assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await consumer.json() == {"foo": "bar"}
        assert isinstance(consumer, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_create(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.post("/api/v2/architecture/consumers").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.api.v2.architecture.consumers.with_streaming_response.create(
            application_version_id="acb2j5k3mly",
        ) as consumer:
            assert not consumer.is_closed
            assert consumer.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await consumer.json() == {"foo": "bar"}
            assert cast(Any, consumer.is_closed) is True
            assert isinstance(consumer, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, consumer.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        consumer = await async_client.api.v2.architecture.consumers.retrieve(
            "id",
        )
        assert_matches_type(ConsumerResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.consumers.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        consumer = await response.parse()
        assert_matches_type(ConsumerResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.consumers.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            consumer = await response.parse()
            assert_matches_type(ConsumerResponse, consumer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.consumers.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncEventPortal) -> None:
        consumer = await async_client.api.v2.architecture.consumers.update(
            id="id",
            application_version_id="acb2j5k3mly",
        )
        assert_matches_type(ConsumerResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEventPortal) -> None:
        consumer = await async_client.api.v2.architecture.consumers.update(
            id="id",
            application_version_id="acb2j5k3mly",
            broker_type="solace",
            consumer_type="eventQueue",
            name="My First Consumer",
            subscriptions=[
                {
                    "subscription_type": "topic",
                    "value": "solace/cloud",
                }
            ],
            type="type",
        )
        assert_matches_type(ConsumerResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.consumers.with_raw_response.update(
            id="id",
            application_version_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        consumer = await response.parse()
        assert_matches_type(ConsumerResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.consumers.with_streaming_response.update(
            id="id",
            application_version_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            consumer = await response.parse()
            assert_matches_type(ConsumerResponse, consumer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.consumers.with_raw_response.update(
                id="",
                application_version_id="acb2j5k3mly",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        consumer = await async_client.api.v2.architecture.consumers.list()
        assert_matches_type(ConsumerListResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        consumer = await async_client.api.v2.architecture.consumers.list(
            application_version_ids=["string"],
            ids=["string"],
            page_number=1,
            page_size=1,
        )
        assert_matches_type(ConsumerListResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.consumers.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        consumer = await response.parse()
        assert_matches_type(ConsumerListResponse, consumer, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.consumers.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            consumer = await response.parse()
            assert_matches_type(ConsumerListResponse, consumer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncEventPortal) -> None:
        consumer = await async_client.api.v2.architecture.consumers.delete(
            "id",
        )
        assert consumer is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.consumers.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        consumer = await response.parse()
        assert consumer is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.consumers.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            consumer = await response.parse()
            assert consumer is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.consumers.with_raw_response.delete(
                "",
            )
