# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal.types.api.v2.architecture import (
    ReviewResponse,
    EventAccessRequestResponse,
)
from event_portal.types.api.v2.architecture.application_versions import EventAccessRequestsListResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEventAccessRequests:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        event_access_request = client.api.v2.architecture.event_access_requests.retrieve(
            "id",
        )
        assert_matches_type(EventAccessRequestResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_access_requests.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_request = response.parse()
        assert_matches_type(EventAccessRequestResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_access_requests.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_request = response.parse()
            assert_matches_type(EventAccessRequestResponse, event_access_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.event_access_requests.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: EventPortal) -> None:
        event_access_request = client.api.v2.architecture.event_access_requests.update(
            id="id",
        )
        assert_matches_type(EventAccessRequestResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: EventPortal) -> None:
        event_access_request = client.api.v2.architecture.event_access_requests.update(
            id="id",
            comments="Comments on the request",
        )
        assert_matches_type(EventAccessRequestResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_access_requests.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_request = response.parse()
        assert_matches_type(EventAccessRequestResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_access_requests.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_request = response.parse()
            assert_matches_type(EventAccessRequestResponse, event_access_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.event_access_requests.with_raw_response.update(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        event_access_request = client.api.v2.architecture.event_access_requests.list()
        assert_matches_type(EventAccessRequestsListResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        event_access_request = client.api.v2.architecture.event_access_requests.list(
            application_ids=["string"],
            can_review=True,
            created_bys=["string"],
            event_ids=["string"],
            exclude_auto_approved_events=True,
            ids=["string"],
            page_number=0,
            page_size=0,
            relationships=["consuming"],
            review_statuses=["approved"],
            sort="sort",
            subscriptions=["string"],
        )
        assert_matches_type(EventAccessRequestsListResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_access_requests.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_request = response.parse()
        assert_matches_type(EventAccessRequestsListResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_access_requests.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_request = response.parse()
            assert_matches_type(EventAccessRequestsListResponse, event_access_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_approve(self, client: EventPortal) -> None:
        event_access_request = client.api.v2.architecture.event_access_requests.approve(
            id="id",
        )
        assert_matches_type(ReviewResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_approve_with_all_params(self, client: EventPortal) -> None:
        event_access_request = client.api.v2.architecture.event_access_requests.approve(
            id="id",
            comments="Approved",
        )
        assert_matches_type(ReviewResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_approve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_access_requests.with_raw_response.approve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_request = response.parse()
        assert_matches_type(ReviewResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_approve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_access_requests.with_streaming_response.approve(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_request = response.parse()
            assert_matches_type(ReviewResponse, event_access_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_approve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.event_access_requests.with_raw_response.approve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_decline(self, client: EventPortal) -> None:
        event_access_request = client.api.v2.architecture.event_access_requests.decline(
            id="id",
        )
        assert_matches_type(ReviewResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_decline_with_all_params(self, client: EventPortal) -> None:
        event_access_request = client.api.v2.architecture.event_access_requests.decline(
            id="id",
            comments="Approved",
        )
        assert_matches_type(ReviewResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_decline(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_access_requests.with_raw_response.decline(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_request = response.parse()
        assert_matches_type(ReviewResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_decline(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_access_requests.with_streaming_response.decline(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_request = response.parse()
            assert_matches_type(ReviewResponse, event_access_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_decline(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.event_access_requests.with_raw_response.decline(
                id="",
            )


class TestAsyncEventAccessRequests:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        event_access_request = await async_client.api.v2.architecture.event_access_requests.retrieve(
            "id",
        )
        assert_matches_type(EventAccessRequestResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_access_requests.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_request = await response.parse()
        assert_matches_type(EventAccessRequestResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_access_requests.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_request = await response.parse()
            assert_matches_type(EventAccessRequestResponse, event_access_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.event_access_requests.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncEventPortal) -> None:
        event_access_request = await async_client.api.v2.architecture.event_access_requests.update(
            id="id",
        )
        assert_matches_type(EventAccessRequestResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_access_request = await async_client.api.v2.architecture.event_access_requests.update(
            id="id",
            comments="Comments on the request",
        )
        assert_matches_type(EventAccessRequestResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_access_requests.with_raw_response.update(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_request = await response.parse()
        assert_matches_type(EventAccessRequestResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_access_requests.with_streaming_response.update(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_request = await response.parse()
            assert_matches_type(EventAccessRequestResponse, event_access_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.event_access_requests.with_raw_response.update(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        event_access_request = await async_client.api.v2.architecture.event_access_requests.list()
        assert_matches_type(EventAccessRequestsListResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_access_request = await async_client.api.v2.architecture.event_access_requests.list(
            application_ids=["string"],
            can_review=True,
            created_bys=["string"],
            event_ids=["string"],
            exclude_auto_approved_events=True,
            ids=["string"],
            page_number=0,
            page_size=0,
            relationships=["consuming"],
            review_statuses=["approved"],
            sort="sort",
            subscriptions=["string"],
        )
        assert_matches_type(EventAccessRequestsListResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_access_requests.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_request = await response.parse()
        assert_matches_type(EventAccessRequestsListResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_access_requests.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_request = await response.parse()
            assert_matches_type(EventAccessRequestsListResponse, event_access_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_approve(self, async_client: AsyncEventPortal) -> None:
        event_access_request = await async_client.api.v2.architecture.event_access_requests.approve(
            id="id",
        )
        assert_matches_type(ReviewResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_approve_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_access_request = await async_client.api.v2.architecture.event_access_requests.approve(
            id="id",
            comments="Approved",
        )
        assert_matches_type(ReviewResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_approve(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_access_requests.with_raw_response.approve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_request = await response.parse()
        assert_matches_type(ReviewResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_approve(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_access_requests.with_streaming_response.approve(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_request = await response.parse()
            assert_matches_type(ReviewResponse, event_access_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_approve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.event_access_requests.with_raw_response.approve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_decline(self, async_client: AsyncEventPortal) -> None:
        event_access_request = await async_client.api.v2.architecture.event_access_requests.decline(
            id="id",
        )
        assert_matches_type(ReviewResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_decline_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_access_request = await async_client.api.v2.architecture.event_access_requests.decline(
            id="id",
            comments="Approved",
        )
        assert_matches_type(ReviewResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_decline(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_access_requests.with_raw_response.decline(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_request = await response.parse()
        assert_matches_type(ReviewResponse, event_access_request, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_decline(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_access_requests.with_streaming_response.decline(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_request = await response.parse()
            assert_matches_type(ReviewResponse, event_access_request, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_decline(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.event_access_requests.with_raw_response.decline(
                id="",
            )
