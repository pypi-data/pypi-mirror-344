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
        custom_attribute_definition = (
            client.api.v2.architecture.application_domains.custom_attribute_definitions.create(
                path_application_domain_id="applicationDomainId",
                scope="organization",
            )
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: EventPortal) -> None:
        custom_attribute_definition = (
            client.api.v2.architecture.application_domains.custom_attribute_definitions.create(
                path_application_domain_id="applicationDomainId",
                scope="organization",
                id="id",
                body_application_domain_id="applicationDomainId",
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
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.create(
            path_application_domain_id="applicationDomainId",
            scope="organization",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = response.parse()
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_domains.custom_attribute_definitions.with_streaming_response.create(
            path_application_domain_id="applicationDomainId",
            scope="organization",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = response.parse()
            assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_create(self, client: EventPortal) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `path_application_domain_id` but received ''"
        ):
            client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.create(
                path_application_domain_id="",
                scope="organization",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: EventPortal) -> None:
        custom_attribute_definition = (
            client.api.v2.architecture.application_domains.custom_attribute_definitions.update(
                custom_attribute_id="customAttributeId",
                path_application_domain_id="applicationDomainId",
                scope="organization",
            )
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: EventPortal) -> None:
        custom_attribute_definition = (
            client.api.v2.architecture.application_domains.custom_attribute_definitions.update(
                custom_attribute_id="customAttributeId",
                path_application_domain_id="applicationDomainId",
                scope="organization",
                id="id",
                body_application_domain_id="applicationDomainId",
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
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.update(
            custom_attribute_id="customAttributeId",
            path_application_domain_id="applicationDomainId",
            scope="organization",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = response.parse()
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_domains.custom_attribute_definitions.with_streaming_response.update(
            custom_attribute_id="customAttributeId",
            path_application_domain_id="applicationDomainId",
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
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `path_application_domain_id` but received ''"
        ):
            client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.update(
                custom_attribute_id="customAttributeId",
                path_application_domain_id="",
                scope="organization",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `custom_attribute_id` but received ''"):
            client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.update(
                custom_attribute_id="",
                path_application_domain_id="applicationDomainId",
                scope="organization",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        custom_attribute_definition = client.api.v2.architecture.application_domains.custom_attribute_definitions.list(
            application_domain_id="applicationDomainId",
        )
        assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        custom_attribute_definition = client.api.v2.architecture.application_domains.custom_attribute_definitions.list(
            application_domain_id="applicationDomainId",
            page_number=1,
            page_size=1,
        )
        assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.list(
            application_domain_id="applicationDomainId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = response.parse()
        assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_domains.custom_attribute_definitions.with_streaming_response.list(
            application_domain_id="applicationDomainId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = response.parse()
            assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_list(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_domain_id` but received ''"):
            client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.list(
                application_domain_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: EventPortal) -> None:
        custom_attribute_definition = (
            client.api.v2.architecture.application_domains.custom_attribute_definitions.delete(
                "applicationDomainId",
            )
        )
        assert custom_attribute_definition is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.delete(
            "applicationDomainId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = response.parse()
        assert custom_attribute_definition is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_domains.custom_attribute_definitions.with_streaming_response.delete(
            "applicationDomainId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = response.parse()
            assert custom_attribute_definition is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_domain_id` but received ''"):
            client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_delete_by_id(self, client: EventPortal) -> None:
        custom_attribute_definition = (
            client.api.v2.architecture.application_domains.custom_attribute_definitions.delete_by_id(
                custom_attribute_id="customAttributeId",
                application_domain_id="applicationDomainId",
            )
        )
        assert custom_attribute_definition is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete_by_id(self, client: EventPortal) -> None:
        response = (
            client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.delete_by_id(
                custom_attribute_id="customAttributeId",
                application_domain_id="applicationDomainId",
            )
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = response.parse()
        assert custom_attribute_definition is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete_by_id(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_domains.custom_attribute_definitions.with_streaming_response.delete_by_id(
            custom_attribute_id="customAttributeId",
            application_domain_id="applicationDomainId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = response.parse()
            assert custom_attribute_definition is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete_by_id(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_domain_id` but received ''"):
            client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.delete_by_id(
                custom_attribute_id="customAttributeId",
                application_domain_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `custom_attribute_id` but received ''"):
            client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.delete_by_id(
                custom_attribute_id="",
                application_domain_id="applicationDomainId",
            )


class TestAsyncCustomAttributeDefinitions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = (
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.create(
                path_application_domain_id="applicationDomainId",
                scope="organization",
            )
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = (
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.create(
                path_application_domain_id="applicationDomainId",
                scope="organization",
                id="id",
                body_application_domain_id="applicationDomainId",
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
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.create(
            path_application_domain_id="applicationDomainId",
            scope="organization",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = await response.parse()
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_streaming_response.create(
            path_application_domain_id="applicationDomainId",
            scope="organization",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = await response.parse()
            assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_create(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `path_application_domain_id` but received ''"
        ):
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.create(
                path_application_domain_id="",
                scope="organization",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = (
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.update(
                custom_attribute_id="customAttributeId",
                path_application_domain_id="applicationDomainId",
                scope="organization",
            )
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = (
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.update(
                custom_attribute_id="customAttributeId",
                path_application_domain_id="applicationDomainId",
                scope="organization",
                id="id",
                body_application_domain_id="applicationDomainId",
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
        )
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.update(
            custom_attribute_id="customAttributeId",
            path_application_domain_id="applicationDomainId",
            scope="organization",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = await response.parse()
        assert_matches_type(CustomAttributeDefinitionResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_streaming_response.update(
            custom_attribute_id="customAttributeId",
            path_application_domain_id="applicationDomainId",
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
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `path_application_domain_id` but received ''"
        ):
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.update(
                custom_attribute_id="customAttributeId",
                path_application_domain_id="",
                scope="organization",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `custom_attribute_id` but received ''"):
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.update(
                custom_attribute_id="",
                path_application_domain_id="applicationDomainId",
                scope="organization",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = (
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.list(
                application_domain_id="applicationDomainId",
            )
        )
        assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = (
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.list(
                application_domain_id="applicationDomainId",
                page_number=1,
                page_size=1,
            )
        )
        assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.list(
            application_domain_id="applicationDomainId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = await response.parse()
        assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_streaming_response.list(
            application_domain_id="applicationDomainId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = await response.parse()
            assert_matches_type(CustomAttributeDefinitionsResponse, custom_attribute_definition, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_list(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_domain_id` but received ''"):
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.list(
                application_domain_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = (
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.delete(
                "applicationDomainId",
            )
        )
        assert custom_attribute_definition is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.delete(
            "applicationDomainId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = await response.parse()
        assert custom_attribute_definition is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_streaming_response.delete(
            "applicationDomainId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = await response.parse()
            assert custom_attribute_definition is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_domain_id` but received ''"):
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete_by_id(self, async_client: AsyncEventPortal) -> None:
        custom_attribute_definition = (
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.delete_by_id(
                custom_attribute_id="customAttributeId",
                application_domain_id="applicationDomainId",
            )
        )
        assert custom_attribute_definition is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete_by_id(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.delete_by_id(
            custom_attribute_id="customAttributeId",
            application_domain_id="applicationDomainId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        custom_attribute_definition = await response.parse()
        assert custom_attribute_definition is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete_by_id(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_streaming_response.delete_by_id(
            custom_attribute_id="customAttributeId",
            application_domain_id="applicationDomainId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            custom_attribute_definition = await response.parse()
            assert custom_attribute_definition is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete_by_id(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `application_domain_id` but received ''"):
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.delete_by_id(
                custom_attribute_id="customAttributeId",
                application_domain_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `custom_attribute_id` but received ''"):
            await async_client.api.v2.architecture.application_domains.custom_attribute_definitions.with_raw_response.delete_by_id(
                custom_attribute_id="",
                application_domain_id="applicationDomainId",
            )
