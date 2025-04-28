# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal.types.api.v2.architecture.application_domains import (
    CustomAttributeDefinitionResponse,
    CustomAttributeDefinitionsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestCustomAttributeDefinitions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: EventPortal) -> None:
        custom_attribute_definition = client.api.v2.architecture.custom_attribute_definitions.create(
            scope="organization",
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: EventPortal) -> None:
        custom_attribute_definition = client.api.v2.architecture.custom_attribute_definitions.create(
            scope="organization",
            id="id",
            application_domain_id="applicationDomainId",
            associated_entities=[
                {
                    "application_domain_ids": ["string"],
                    "entity_type": "entityType",
                }
            ],
            associated_entity_types=['["event","application"]'],
            name="colour",
            type="type",
            validation_messages={
                "errors": [
                    {
                        "context": {
                            "entity_names": ["string"],
                            "entity_type": "entityType",
                            "ids": ["string"],
                        },
                        "message": "message",
                        "message_key": "messageKey",
                    }
                ],
                "warnings": [
                    {
                        "context": {
                            "entity_names": ["string"],
                            "entity_type": "entityType",
                            "ids": ["string"],
                        },
                        "message": "message",
                        "message_key": "messageKey",
                    }
                ],
            },
            value_type="STRING",
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.custom_attribute_definitions.with_raw_response.create(
            scope="organization",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = response.parse()
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with client.api.v2.architecture.custom_attribute_definitions.with_streaming_response.create(
            scope="organization",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = response.parse()
            assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        custom_attribute_definition = client.api.v2.architecture.custom_attribute_definitions.retrieve(
            "id",
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.custom_attribute_definitions.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = response.parse()
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.custom_attribute_definitions.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = response.parse()
            assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.custom_attribute_definitions.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: EventPortal) -> None:
        custom_attribute_definition = client.api.v2.architecture.custom_attribute_definitions.update(
            path_id="id",
            scope="organization",
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: EventPortal) -> None:
        custom_attribute_definition = client.api.v2.architecture.custom_attribute_definitions.update(
            path_id="id",
            scope="organization",
            body_id="id",
            application_domain_id="applicationDomainId",
            associated_entities=[
                {
                    "application_domain_ids": ["string"],
                    "entity_type": "entityType",
                }
            ],
            associated_entity_types=['["event","application"]'],
            name="colour",
            type="type",
            validation_messages={
                "errors": [
                    {
                        "context": {
                            "entity_names": ["string"],
                            "entity_type": "entityType",
                            "ids": ["string"],
                        },
                        "message": "message",
                        "message_key": "messageKey",
                    }
                ],
                "warnings": [
                    {
                        "context": {
                            "entity_names": ["string"],
                            "entity_type": "entityType",
                            "ids": ["string"],
                        },
                        "message": "message",
                        "message_key": "messageKey",
                    }
                ],
            },
            value_type="STRING",
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.custom_attribute_definitions.with_raw_response.update(
            path_id="id",
            scope="organization",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = response.parse()
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: EventPortal) -> None:
        with client.api.v2.architecture.custom_attribute_definitions.with_streaming_response.update(
            path_id="id",
            scope="organization",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = response.parse()
            assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_id` but received ''"):
            client.api.v2.architecture.custom_attribute_definitions.with_raw_response.update(
                path_id="",
                scope="organization",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        custom_attribute_definition = client.api.v2.architecture.custom_attribute_definitions.list()
        assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        custom_attribute_definition = client.api.v2.architecture.custom_attribute_definitions.list(
            associated_entity_types=["string"],
            page_number=1,
            page_size=1,
        )
        assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.custom_attribute_definitions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = response.parse()
        assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.custom_attribute_definitions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = response.parse()
            assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: EventPortal) -> None:
        custom_attribute_definition = client.api.v2.architecture.custom_attribute_definitions.delete(
            "id",
        )
        assert custom_attribute_definition is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.custom_attribute_definitions.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = response.parse()
        assert custom_attribute_definition is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: EventPortal) -> None:
        with client.api.v2.architecture.custom_attribute_definitions.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = response.parse()
            assert custom_attribute_definition is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.custom_attribute_definitions.with_raw_response.delete(
                "",
            )


class TestAsyncCustomAttributeDefinitions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = await async_client.api.v2.architecture.custom_attribute_definitions.create(
            scope="organization",
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = await async_client.api.v2.architecture.custom_attribute_definitions.create(
            scope="organization",
            id="id",
            application_domain_id="applicationDomainId",
            associated_entities=[
                {
                    "application_domain_ids": ["string"],
                    "entity_type": "entityType",
                }
            ],
            associated_entity_types=['["event","application"]'],
            name="colour",
            type="type",
            validation_messages={
                "errors": [
                    {
                        "context": {
                            "entity_names": ["string"],
                            "entity_type": "entityType",
                            "ids": ["string"],
                        },
                        "message": "message",
                        "message_key": "messageKey",
                    }
                ],
                "warnings": [
                    {
                        "context": {
                            "entity_names": ["string"],
                            "entity_type": "entityType",
                            "ids": ["string"],
                        },
                        "message": "message",
                        "message_key": "messageKey",
                    }
                ],
            },
            value_type="STRING",
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.custom_attribute_definitions.with_raw_response.create(
            scope="organization",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = await response.parse()
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.custom_attribute_definitions.with_streaming_response.create(
            scope="organization",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = await response.parse()
            assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = await async_client.api.v2.architecture.custom_attribute_definitions.retrieve(
            "id",
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.custom_attribute_definitions.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = await response.parse()
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.custom_attribute_definitions.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = await response.parse()
            assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.custom_attribute_definitions.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = await async_client.api.v2.architecture.custom_attribute_definitions.update(
            path_id="id",
            scope="organization",
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = await async_client.api.v2.architecture.custom_attribute_definitions.update(
            path_id="id",
            scope="organization",
            body_id="id",
            application_domain_id="applicationDomainId",
            associated_entities=[
                {
                    "application_domain_ids": ["string"],
                    "entity_type": "entityType",
                }
            ],
            associated_entity_types=['["event","application"]'],
            name="colour",
            type="type",
            validation_messages={
                "errors": [
                    {
                        "context": {
                            "entity_names": ["string"],
                            "entity_type": "entityType",
                            "ids": ["string"],
                        },
                        "message": "message",
                        "message_key": "messageKey",
                    }
                ],
                "warnings": [
                    {
                        "context": {
                            "entity_names": ["string"],
                            "entity_type": "entityType",
                            "ids": ["string"],
                        },
                        "message": "message",
                        "message_key": "messageKey",
                    }
                ],
            },
            value_type="STRING",
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.custom_attribute_definitions.with_raw_response.update(
            path_id="id",
            scope="organization",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = await response.parse()
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.custom_attribute_definitions.with_streaming_response.update(
            path_id="id",
            scope="organization",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = await response.parse()
            assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `path_id` but received ''"):
            await async_client.api.v2.architecture.custom_attribute_definitions.with_raw_response.update(
                path_id="",
                scope="organization",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = await async_client.api.v2.architecture.custom_attribute_definitions.list()
        assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = await async_client.api.v2.architecture.custom_attribute_definitions.list(
            associated_entity_types=["string"],
            page_number=1,
            page_size=1,
        )
        assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.custom_attribute_definitions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = await response.parse()
        assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with (
            async_client.api.v2.architecture.custom_attribute_definitions.with_streaming_response.list()
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = await response.parse()
            assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = await async_client.api.v2.architecture.custom_attribute_definitions.delete(
            "id",
        )
        assert custom_attribute_definition is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.custom_attribute_definitions.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = await response.parse()
        assert custom_attribute_definition is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.custom_attribute_definitions.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = await response.parse()
            assert custom_attribute_definition is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.custom_attribute_definitions.with_raw_response.delete(
                "",
            )
