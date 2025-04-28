# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal.types.api.v2.architecture import (
    EnumListResponse,
    TopicAddressEnumResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEnums:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: EventPortal) -> None:
        enum = client.api.v2.architecture.enums.create(
            application_domain_id="12345678",
            name="My First Enum",
        )
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: EventPortal) -> None:
        enum = client.api.v2.architecture.enums.create(
            application_domain_id="12345678",
            name="My First Enum",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            shared=False,
        )
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.enums.with_raw_response.create(
            application_domain_id="12345678",
            name="My First Enum",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enum = response.parse()
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with client.api.v2.architecture.enums.with_streaming_response.create(
            application_domain_id="12345678",
            name="My First Enum",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enum = response.parse()
            assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        enum = client.api.v2.architecture.enums.retrieve(
            "id",
        )
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.enums.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enum = response.parse()
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.enums.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enum = response.parse()
            assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.enums.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: EventPortal) -> None:
        enum = client.api.v2.architecture.enums.update(
            id="id",
            application_domain_id="12345678",
            name="My First Enum",
        )
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: EventPortal) -> None:
        enum = client.api.v2.architecture.enums.update(
            id="id",
            application_domain_id="12345678",
            name="My First Enum",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            shared=False,
        )
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.enums.with_raw_response.update(
            id="id",
            application_domain_id="12345678",
            name="My First Enum",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enum = response.parse()
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: EventPortal) -> None:
        with client.api.v2.architecture.enums.with_streaming_response.update(
            id="id",
            application_domain_id="12345678",
            name="My First Enum",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enum = response.parse()
            assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.enums.with_raw_response.update(
                id="",
                application_domain_id="12345678",
                name="My First Enum",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        enum = client.api.v2.architecture.enums.list()
        assert_matches_type(EnumListResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        enum = client.api.v2.architecture.enums.list(
            application_domain_id="applicationDomainId",
            application_domain_ids=["string"],
            custom_attributes="customAttributes",
            ids=["string"],
            names=["string"],
            page_number=1,
            page_size=1,
            shared=True,
            sort="sort",
        )
        assert_matches_type(EnumListResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.enums.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enum = response.parse()
        assert_matches_type(EnumListResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.enums.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enum = response.parse()
            assert_matches_type(EnumListResponse, enum, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: EventPortal) -> None:
        enum = client.api.v2.architecture.enums.delete(
            "id",
        )
        assert enum is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.enums.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enum = response.parse()
        assert enum is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: EventPortal) -> None:
        with client.api.v2.architecture.enums.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enum = response.parse()
            assert enum is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.enums.with_raw_response.delete(
                "",
            )


class TestAsyncEnums:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        enum = await async_client.api.v2.architecture.enums.create(
            application_domain_id="12345678",
            name="My First Enum",
        )
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEventPortal) -> None:
        enum = await async_client.api.v2.architecture.enums.create(
            application_domain_id="12345678",
            name="My First Enum",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            shared=False,
        )
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.enums.with_raw_response.create(
            application_domain_id="12345678",
            name="My First Enum",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enum = await response.parse()
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.enums.with_streaming_response.create(
            application_domain_id="12345678",
            name="My First Enum",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enum = await response.parse()
            assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        enum = await async_client.api.v2.architecture.enums.retrieve(
            "id",
        )
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.enums.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enum = await response.parse()
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.enums.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enum = await response.parse()
            assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.enums.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncEventPortal) -> None:
        enum = await async_client.api.v2.architecture.enums.update(
            id="id",
            application_domain_id="12345678",
            name="My First Enum",
        )
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEventPortal) -> None:
        enum = await async_client.api.v2.architecture.enums.update(
            id="id",
            application_domain_id="12345678",
            name="My First Enum",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            shared=False,
        )
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.enums.with_raw_response.update(
            id="id",
            application_domain_id="12345678",
            name="My First Enum",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enum = await response.parse()
        assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.enums.with_streaming_response.update(
            id="id",
            application_domain_id="12345678",
            name="My First Enum",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enum = await response.parse()
            assert_matches_type(TopicAddressEnumResponse, enum, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.enums.with_raw_response.update(
                id="",
                application_domain_id="12345678",
                name="My First Enum",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        enum = await async_client.api.v2.architecture.enums.list()
        assert_matches_type(EnumListResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        enum = await async_client.api.v2.architecture.enums.list(
            application_domain_id="applicationDomainId",
            application_domain_ids=["string"],
            custom_attributes="customAttributes",
            ids=["string"],
            names=["string"],
            page_number=1,
            page_size=1,
            shared=True,
            sort="sort",
        )
        assert_matches_type(EnumListResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.enums.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enum = await response.parse()
        assert_matches_type(EnumListResponse, enum, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.enums.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enum = await response.parse()
            assert_matches_type(EnumListResponse, enum, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncEventPortal) -> None:
        enum = await async_client.api.v2.architecture.enums.delete(
            "id",
        )
        assert enum is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.enums.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        enum = await response.parse()
        assert enum is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.enums.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            enum = await response.parse()
            assert enum is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.enums.with_raw_response.delete(
                "",
            )
