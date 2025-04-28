# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal.types.api.v2.architecture import (
    ReviewResponse,
    EventAccessReviewListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEventAccessReviews:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: EventPortal) -> None:
        event_access_review = client.api.v2.architecture.event_access_reviews.create(
            decision="approved",
        )
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: EventPortal) -> None:
        event_access_review = client.api.v2.architecture.event_access_reviews.create(
            decision="approved",
            comments="Approved",
        )
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_access_reviews.with_raw_response.create(
            decision="approved",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_review = response.parse()
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_access_reviews.with_streaming_response.create(
            decision="approved",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_review = response.parse()
            assert_matches_type(ReviewResponse, event_access_review, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        event_access_review = client.api.v2.architecture.event_access_reviews.retrieve(
            "id",
        )
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_access_reviews.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_review = response.parse()
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_access_reviews.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_review = response.parse()
            assert_matches_type(ReviewResponse, event_access_review, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.event_access_reviews.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: EventPortal) -> None:
        event_access_review = client.api.v2.architecture.event_access_reviews.update(
            id="id",
            decision="approved",
        )
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: EventPortal) -> None:
        event_access_review = client.api.v2.architecture.event_access_reviews.update(
            id="id",
            decision="approved",
            comments="Approved",
        )
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_access_reviews.with_raw_response.update(
            id="id",
            decision="approved",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_review = response.parse()
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_access_reviews.with_streaming_response.update(
            id="id",
            decision="approved",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_review = response.parse()
            assert_matches_type(ReviewResponse, event_access_review, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.event_access_reviews.with_raw_response.update(
                id="",
                decision="approved",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        event_access_review = client.api.v2.architecture.event_access_reviews.list()
        assert_matches_type(EventAccessReviewListResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        event_access_review = client.api.v2.architecture.event_access_reviews.list(
            decision="approved",
            ids=["string"],
            page_number=0,
            page_size=0,
            request_ids=["string"],
            sort="sort",
            user_id="userId",
        )
        assert_matches_type(EventAccessReviewListResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_access_reviews.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_review = response.parse()
        assert_matches_type(EventAccessReviewListResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_access_reviews.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_review = response.parse()
            assert_matches_type(EventAccessReviewListResponse, event_access_review, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: EventPortal) -> None:
        event_access_review = client.api.v2.architecture.event_access_reviews.delete(
            "id",
        )
        assert event_access_review is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_access_reviews.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_review = response.parse()
        assert event_access_review is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_access_reviews.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_review = response.parse()
            assert event_access_review is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.event_access_reviews.with_raw_response.delete(
                "",
            )


class TestAsyncEventAccessReviews:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        event_access_review = await async_client.api.v2.architecture.event_access_reviews.create(
            decision="approved",
        )
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_access_review = await async_client.api.v2.architecture.event_access_reviews.create(
            decision="approved",
            comments="Approved",
        )
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_access_reviews.with_raw_response.create(
            decision="approved",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_review = await response.parse()
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_access_reviews.with_streaming_response.create(
            decision="approved",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_review = await response.parse()
            assert_matches_type(ReviewResponse, event_access_review, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        event_access_review = await async_client.api.v2.architecture.event_access_reviews.retrieve(
            "id",
        )
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_access_reviews.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_review = await response.parse()
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_access_reviews.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_review = await response.parse()
            assert_matches_type(ReviewResponse, event_access_review, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.event_access_reviews.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncEventPortal) -> None:
        event_access_review = await async_client.api.v2.architecture.event_access_reviews.update(
            id="id",
            decision="approved",
        )
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_access_review = await async_client.api.v2.architecture.event_access_reviews.update(
            id="id",
            decision="approved",
            comments="Approved",
        )
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_access_reviews.with_raw_response.update(
            id="id",
            decision="approved",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_review = await response.parse()
        assert_matches_type(ReviewResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_access_reviews.with_streaming_response.update(
            id="id",
            decision="approved",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_review = await response.parse()
            assert_matches_type(ReviewResponse, event_access_review, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.event_access_reviews.with_raw_response.update(
                id="",
                decision="approved",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        event_access_review = await async_client.api.v2.architecture.event_access_reviews.list()
        assert_matches_type(EventAccessReviewListResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_access_review = await async_client.api.v2.architecture.event_access_reviews.list(
            decision="approved",
            ids=["string"],
            page_number=0,
            page_size=0,
            request_ids=["string"],
            sort="sort",
            user_id="userId",
        )
        assert_matches_type(EventAccessReviewListResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_access_reviews.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_review = await response.parse()
        assert_matches_type(EventAccessReviewListResponse, event_access_review, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_access_reviews.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_review = await response.parse()
            assert_matches_type(EventAccessReviewListResponse, event_access_review, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncEventPortal) -> None:
        event_access_review = await async_client.api.v2.architecture.event_access_reviews.delete(
            "id",
        )
        assert event_access_review is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_access_reviews.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_access_review = await response.parse()
        assert event_access_review is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_access_reviews.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_access_review = await response.parse()
            assert event_access_review is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.event_access_reviews.with_raw_response.delete(
                "",
            )
