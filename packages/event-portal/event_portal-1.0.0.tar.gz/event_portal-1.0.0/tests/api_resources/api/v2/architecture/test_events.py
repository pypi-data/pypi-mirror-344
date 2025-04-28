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
    EventResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEvents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: EventPortal) -> None:
        event = client.api.v2.architecture.events.create(
            application_domain_id="acb2j5k3mly",
            name="My First Event",
        )
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: EventPortal) -> None:
        event = client.api.v2.architecture.events.create(
            application_domain_id="acb2j5k3mly",
            name="My First Event",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            requires_approval=False,
            shared=False,
        )
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.events.with_raw_response.create(
            application_domain_id="acb2j5k3mly",
            name="My First Event",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with client.api.v2.architecture.events.with_streaming_response.create(
            application_domain_id="acb2j5k3mly",
            name="My First Event",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(EventResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        event = client.api.v2.architecture.events.retrieve(
            "id",
        )
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.events.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.events.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(EventResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.events.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: EventPortal) -> None:
        event = client.api.v2.architecture.events.update(
            id="id",
            application_domain_id="acb2j5k3mly",
            name="My First Event",
        )
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: EventPortal) -> None:
        event = client.api.v2.architecture.events.update(
            id="id",
            application_domain_id="acb2j5k3mly",
            name="My First Event",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            requires_approval=False,
            shared=False,
        )
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.events.with_raw_response.update(
            id="id",
            application_domain_id="acb2j5k3mly",
            name="My First Event",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: EventPortal) -> None:
        with client.api.v2.architecture.events.with_streaming_response.update(
            id="id",
            application_domain_id="acb2j5k3mly",
            name="My First Event",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert_matches_type(EventResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.events.with_raw_response.update(
                id="",
                application_domain_id="acb2j5k3mly",
                name="My First Event",
            )

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/events").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        event = client.api.v2.architecture.events.list()
        assert event.is_closed
        assert event.json() == {"foo": "bar"}
        assert cast(Any, event.is_closed) is True
        assert isinstance(event, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_with_all_params(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/events").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        event = client.api.v2.architecture.events.list(
            application_domain_id="applicationDomainId",
            application_domain_ids=["string"],
            broker_type="brokerType",
            custom_attributes="customAttributes",
            ids=["string"],
            name="name",
            page_number=1,
            page_size=1,
            shared=True,
            sort="sort",
        )
        assert event.is_closed
        assert event.json() == {"foo": "bar"}
        assert cast(Any, event.is_closed) is True
        assert isinstance(event, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/events").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        event = client.api.v2.architecture.events.with_raw_response.list()

        assert event.is_closed is True
        assert event.http_request.headers.get("X-Stainless-Lang") == "python"
        assert event.json() == {"foo": "bar"}
        assert isinstance(event, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/events").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        with client.api.v2.architecture.events.with_streaming_response.list() as event:
            assert not event.is_closed
            assert event.http_request.headers.get("X-Stainless-Lang") == "python"

            assert event.json() == {"foo": "bar"}
            assert cast(Any, event.is_closed) is True
            assert isinstance(event, StreamedBinaryAPIResponse)

        assert cast(Any, event.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: EventPortal) -> None:
        event = client.api.v2.architecture.events.delete(
            "id",
        )
        assert event is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.events.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = response.parse()
        assert event is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: EventPortal) -> None:
        with client.api.v2.architecture.events.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = response.parse()
            assert event is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.events.with_raw_response.delete(
                "",
            )


class TestAsyncEvents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        event = await async_client.api.v2.architecture.events.create(
            application_domain_id="acb2j5k3mly",
            name="My First Event",
        )
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event = await async_client.api.v2.architecture.events.create(
            application_domain_id="acb2j5k3mly",
            name="My First Event",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            requires_approval=False,
            shared=False,
        )
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.events.with_raw_response.create(
            application_domain_id="acb2j5k3mly",
            name="My First Event",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.events.with_streaming_response.create(
            application_domain_id="acb2j5k3mly",
            name="My First Event",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(EventResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        event = await async_client.api.v2.architecture.events.retrieve(
            "id",
        )
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.events.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.events.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(EventResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.events.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncEventPortal) -> None:
        event = await async_client.api.v2.architecture.events.update(
            id="id",
            application_domain_id="acb2j5k3mly",
            name="My First Event",
        )
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event = await async_client.api.v2.architecture.events.update(
            id="id",
            application_domain_id="acb2j5k3mly",
            name="My First Event",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            requires_approval=False,
            shared=False,
        )
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.events.with_raw_response.update(
            id="id",
            application_domain_id="acb2j5k3mly",
            name="My First Event",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert_matches_type(EventResponse, event, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.events.with_streaming_response.update(
            id="id",
            application_domain_id="acb2j5k3mly",
            name="My First Event",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert_matches_type(EventResponse, event, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.events.with_raw_response.update(
                id="",
                application_domain_id="acb2j5k3mly",
                name="My First Event",
            )

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/events").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        event = await async_client.api.v2.architecture.events.list()
        assert event.is_closed
        assert await event.json() == {"foo": "bar"}
        assert cast(Any, event.is_closed) is True
        assert isinstance(event, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/events").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        event = await async_client.api.v2.architecture.events.list(
            application_domain_id="applicationDomainId",
            application_domain_ids=["string"],
            broker_type="brokerType",
            custom_attributes="customAttributes",
            ids=["string"],
            name="name",
            page_number=1,
            page_size=1,
            shared=True,
            sort="sort",
        )
        assert event.is_closed
        assert await event.json() == {"foo": "bar"}
        assert cast(Any, event.is_closed) is True
        assert isinstance(event, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/events").mock(return_value=httpx.Response(200, json={"foo": "bar"}))

        event = await async_client.api.v2.architecture.events.with_raw_response.list()

        assert event.is_closed is True
        assert event.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await event.json() == {"foo": "bar"}
        assert isinstance(event, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/events").mock(return_value=httpx.Response(200, json={"foo": "bar"}))
        async with async_client.api.v2.architecture.events.with_streaming_response.list() as event:
            assert not event.is_closed
            assert event.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await event.json() == {"foo": "bar"}
            assert cast(Any, event.is_closed) is True
            assert isinstance(event, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, event.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncEventPortal) -> None:
        event = await async_client.api.v2.architecture.events.delete(
            "id",
        )
        assert event is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.events.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event = await response.parse()
        assert event is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.events.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event = await response.parse()
            assert event is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.events.with_raw_response.delete(
                "",
            )
