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
    TopicDomainResponse,
    TopicDomainListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestTopicDomains:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: EventPortal) -> None:
        topic_domain = client.api.v2.architecture.topic_domains.create(
            address_levels=[
                {
                    "address_level_type": "literal",
                    "name": "root",
                }
            ],
            application_domain_id="acb2j5k3mly",
            broker_type="solace",
        )
        assert_matches_type(TopicDomainResponse, topic_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.topic_domains.with_raw_response.create(
            address_levels=[
                {
                    "address_level_type": "literal",
                    "name": "root",
                }
            ],
            application_domain_id="acb2j5k3mly",
            broker_type="solace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic_domain = response.parse()
        assert_matches_type(TopicDomainResponse, topic_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with client.api.v2.architecture.topic_domains.with_streaming_response.create(
            address_levels=[
                {
                    "address_level_type": "literal",
                    "name": "root",
                }
            ],
            application_domain_id="acb2j5k3mly",
            broker_type="solace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic_domain = response.parse()
            assert_matches_type(TopicDomainResponse, topic_domain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        topic_domain = client.api.v2.architecture.topic_domains.retrieve(
            "id",
        )
        assert_matches_type(TopicDomainResponse, topic_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.topic_domains.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic_domain = response.parse()
        assert_matches_type(TopicDomainResponse, topic_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.topic_domains.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic_domain = response.parse()
            assert_matches_type(TopicDomainResponse, topic_domain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.topic_domains.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        topic_domain = client.api.v2.architecture.topic_domains.list()
        assert_matches_type(TopicDomainListResponse, topic_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        topic_domain = client.api.v2.architecture.topic_domains.list(
            application_domain_id="applicationDomainId",
            application_domain_ids=["string"],
            broker_type="brokerType",
            ids=["string"],
            page_number=1,
            page_size=1,
        )
        assert_matches_type(TopicDomainListResponse, topic_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.topic_domains.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic_domain = response.parse()
        assert_matches_type(TopicDomainListResponse, topic_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.topic_domains.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic_domain = response.parse()
            assert_matches_type(TopicDomainListResponse, topic_domain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_delete(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.delete("/api/v2/architecture/topicDomains/id").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        topic_domain = client.api.v2.architecture.topic_domains.delete(
            "id",
        )
        assert topic_domain.is_closed
        assert topic_domain.json() == {"foo": "bar"}
        assert cast(Any, topic_domain.is_closed) is True
        assert isinstance(topic_domain, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_delete(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.delete("/api/v2/architecture/topicDomains/id").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        topic_domain = client.api.v2.architecture.topic_domains.with_raw_response.delete(
            "id",
        )

        assert topic_domain.is_closed is True
        assert topic_domain.http_request.headers.get("X-Stainless-Lang") == "python"
        assert topic_domain.json() == {"foo": "bar"}
        assert isinstance(topic_domain, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_delete(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.delete("/api/v2/architecture/topicDomains/id").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.api.v2.architecture.topic_domains.with_streaming_response.delete(
            "id",
        ) as topic_domain:
            assert not topic_domain.is_closed
            assert topic_domain.http_request.headers.get("X-Stainless-Lang") == "python"

            assert topic_domain.json() == {"foo": "bar"}
            assert cast(Any, topic_domain.is_closed) is True
            assert isinstance(topic_domain, StreamedBinaryAPIResponse)

        assert cast(Any, topic_domain.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_path_params_delete(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.topic_domains.with_raw_response.delete(
                "",
            )


class TestAsyncTopicDomains:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        topic_domain = await async_client.api.v2.architecture.topic_domains.create(
            address_levels=[
                {
                    "address_level_type": "literal",
                    "name": "root",
                }
            ],
            application_domain_id="acb2j5k3mly",
            broker_type="solace",
        )
        assert_matches_type(TopicDomainResponse, topic_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.topic_domains.with_raw_response.create(
            address_levels=[
                {
                    "address_level_type": "literal",
                    "name": "root",
                }
            ],
            application_domain_id="acb2j5k3mly",
            broker_type="solace",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic_domain = await response.parse()
        assert_matches_type(TopicDomainResponse, topic_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.topic_domains.with_streaming_response.create(
            address_levels=[
                {
                    "address_level_type": "literal",
                    "name": "root",
                }
            ],
            application_domain_id="acb2j5k3mly",
            broker_type="solace",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic_domain = await response.parse()
            assert_matches_type(TopicDomainResponse, topic_domain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        topic_domain = await async_client.api.v2.architecture.topic_domains.retrieve(
            "id",
        )
        assert_matches_type(TopicDomainResponse, topic_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.topic_domains.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic_domain = await response.parse()
        assert_matches_type(TopicDomainResponse, topic_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.topic_domains.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic_domain = await response.parse()
            assert_matches_type(TopicDomainResponse, topic_domain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.topic_domains.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        topic_domain = await async_client.api.v2.architecture.topic_domains.list()
        assert_matches_type(TopicDomainListResponse, topic_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        topic_domain = await async_client.api.v2.architecture.topic_domains.list(
            application_domain_id="applicationDomainId",
            application_domain_ids=["string"],
            broker_type="brokerType",
            ids=["string"],
            page_number=1,
            page_size=1,
        )
        assert_matches_type(TopicDomainListResponse, topic_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.topic_domains.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        topic_domain = await response.parse()
        assert_matches_type(TopicDomainListResponse, topic_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.topic_domains.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            topic_domain = await response.parse()
            assert_matches_type(TopicDomainListResponse, topic_domain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_delete(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.delete("/api/v2/architecture/topicDomains/id").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        topic_domain = await async_client.api.v2.architecture.topic_domains.delete(
            "id",
        )
        assert topic_domain.is_closed
        assert await topic_domain.json() == {"foo": "bar"}
        assert cast(Any, topic_domain.is_closed) is True
        assert isinstance(topic_domain, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_delete(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.delete("/api/v2/architecture/topicDomains/id").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        topic_domain = await async_client.api.v2.architecture.topic_domains.with_raw_response.delete(
            "id",
        )

        assert topic_domain.is_closed is True
        assert topic_domain.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await topic_domain.json() == {"foo": "bar"}
        assert isinstance(topic_domain, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_delete(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.delete("/api/v2/architecture/topicDomains/id").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.api.v2.architecture.topic_domains.with_streaming_response.delete(
            "id",
        ) as topic_domain:
            assert not topic_domain.is_closed
            assert topic_domain.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await topic_domain.json() == {"foo": "bar"}
            assert cast(Any, topic_domain.is_closed) is True
            assert isinstance(topic_domain, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, topic_domain.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_path_params_delete(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.topic_domains.with_raw_response.delete(
                "",
            )
