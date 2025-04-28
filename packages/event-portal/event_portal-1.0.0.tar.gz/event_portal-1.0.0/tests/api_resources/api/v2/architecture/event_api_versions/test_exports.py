# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExports:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_async_api(self, client: EventPortal) -> None:
        export = client.api.v2.architecture.event_api_versions.exports.get_async_api(
            event_api_version_id="eventApiVersionId",
        )
        assert_matches_type(str, export, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_async_api_with_all_params(self, client: EventPortal) -> None:
        export = client.api.v2.architecture.event_api_versions.exports.get_async_api(
            event_api_version_id="eventApiVersionId",
            async_api_version="2.0.0",
            event_api_product_version_id="eventApiProductVersionId",
            format="json",
            gateway_messaging_service_ids=["string"],
            included_extensions="all",
            naming_strategies=["applicationDomainPrefix"],
            plan_id="planId",
        )
        assert_matches_type(str, export, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_async_api(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_versions.exports.with_raw_response.get_async_api(
            event_api_version_id="eventApiVersionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        export = response.parse()
        assert_matches_type(str, export, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_async_api(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_versions.exports.with_streaming_response.get_async_api(
            event_api_version_id="eventApiVersionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            export = response.parse()
            assert_matches_type(str, export, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_async_api(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `event_api_version_id` but received ''"):
            client.api.v2.architecture.event_api_versions.exports.with_raw_response.get_async_api(
                event_api_version_id="",
            )


class TestAsyncExports:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_async_api(self, async_client: AsyncEventPortal) -> None:
        export = await async_client.api.v2.architecture.event_api_versions.exports.get_async_api(
            event_api_version_id="eventApiVersionId",
        )
        assert_matches_type(str, export, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_async_api_with_all_params(self, async_client: AsyncEventPortal) -> None:
        export = await async_client.api.v2.architecture.event_api_versions.exports.get_async_api(
            event_api_version_id="eventApiVersionId",
            async_api_version="2.0.0",
            event_api_product_version_id="eventApiProductVersionId",
            format="json",
            gateway_messaging_service_ids=["string"],
            included_extensions="all",
            naming_strategies=["applicationDomainPrefix"],
            plan_id="planId",
        )
        assert_matches_type(str, export, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_async_api(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_versions.exports.with_raw_response.get_async_api(
            event_api_version_id="eventApiVersionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        export = await response.parse()
        assert_matches_type(str, export, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_async_api(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_api_versions.exports.with_streaming_response.get_async_api(
            event_api_version_id="eventApiVersionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            export = await response.parse()
            assert_matches_type(str, export, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_async_api(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `event_api_version_id` but received ''"):
            await async_client.api.v2.architecture.event_api_versions.exports.with_raw_response.get_async_api(
                event_api_version_id="",
            )
