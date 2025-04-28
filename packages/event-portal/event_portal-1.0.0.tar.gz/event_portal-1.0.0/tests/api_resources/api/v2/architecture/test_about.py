# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from event_portal import EventPortal, AsyncEventPortal
from event_portal._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAbout:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_applications(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/about/applications").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        about = client.api.v2.architecture.about.list_applications()
        assert about.is_closed
        assert about.json() == {"foo": "bar"}
        assert cast(Any, about.is_closed) is True
        assert isinstance(about, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_list_applications_with_all_params(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/about/applications").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        about = client.api.v2.architecture.about.list_applications(
            ids=["string"],
            name_contains="nameContains",
            page_number=1,
            page_size=1,
            sort="sort",
        )
        assert about.is_closed
        assert about.json() == {"foo": "bar"}
        assert cast(Any, about.is_closed) is True
        assert isinstance(about, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_list_applications(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/about/applications").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        about = client.api.v2.architecture.about.with_raw_response.list_applications()

        assert about.is_closed is True
        assert about.http_request.headers.get("X-Stainless-Lang") == "python"
        assert about.json() == {"foo": "bar"}
        assert isinstance(about, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_list_applications(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/about/applications").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.api.v2.architecture.about.with_streaming_response.list_applications() as about:
            assert not about.is_closed
            assert about.http_request.headers.get("X-Stainless-Lang") == "python"

            assert about.json() == {"foo": "bar"}
            assert cast(Any, about.is_closed) is True
            assert isinstance(about, StreamedBinaryAPIResponse)

        assert cast(Any, about.is_closed) is True


class TestAsyncAbout:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list_applications(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/about/applications").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        about = await async_client.api.v2.architecture.about.list_applications()
        assert about.is_closed
        assert await about.json() == {"foo": "bar"}
        assert cast(Any, about.is_closed) is True
        assert isinstance(about, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_list_applications_with_all_params(
        self, async_client: AsyncEventPortal, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/api/v2/architecture/about/applications").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        about = await async_client.api.v2.architecture.about.list_applications(
            ids=["string"],
            name_contains="nameContains",
            page_number=1,
            page_size=1,
            sort="sort",
        )
        assert about.is_closed
        assert await about.json() == {"foo": "bar"}
        assert cast(Any, about.is_closed) is True
        assert isinstance(about, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_list_applications(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/about/applications").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        about = await async_client.api.v2.architecture.about.with_raw_response.list_applications()

        assert about.is_closed is True
        assert about.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await about.json() == {"foo": "bar"}
        assert isinstance(about, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_list_applications(
        self, async_client: AsyncEventPortal, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/api/v2/architecture/about/applications").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.api.v2.architecture.about.with_streaming_response.list_applications() as about:
            assert not about.is_closed
            assert about.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await about.json() == {"foo": "bar"}
            assert cast(Any, about.is_closed) is True
            assert isinstance(about, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, about.is_closed) is True
