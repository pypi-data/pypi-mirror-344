# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal.types.api.v2.architecture import (
    EventVersionResponse,
    EventVersionListResponse,
    StateChangeRequestResponse,
    MessagingServiceAssociationResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEventVersions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: EventPortal) -> None:
        event_version = client.api.v2.architecture.event_versions.create(
            event_id="acb2j5k3mly",
            version="1.0.0",
        )
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: EventPortal) -> None:
        event_version = client.api.v2.architecture.event_versions.create(
            event_id="acb2j5k3mly",
            version="1.0.0",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            delivery_descriptor={
                "id": "id",
                "address": {
                    "address_levels": [
                        {
                            "address_level_type": "literal",
                            "name": "root",
                            "enum_version_id": "enumVersionId",
                        }
                    ],
                    "address_type": "topic",
                    "type": "type",
                },
                "broker_type": "brokerType",
                "key_schema_primitive_type": "BYTES",
                "key_schema_version_id": "shb3mlyec2g",
                "type": "type",
            },
            description="Event version created by Solace PubSub+ Cloud documentation",
            display_name="Display name for the version",
            end_of_life_date="2021-12-31T20:30:57.920Z",
            schema_primitive_type="BYTES",
            schema_version_id="shb3mlyec2g",
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
        )
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_versions.with_raw_response.create(
            event_id="acb2j5k3mly",
            version="1.0.0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_version = response.parse()
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_versions.with_streaming_response.create(
            event_id="acb2j5k3mly",
            version="1.0.0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_version = response.parse()
            assert_matches_type(EventVersionResponse, event_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        event_version = client.api.v2.architecture.event_versions.retrieve(
            "id",
        )
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_versions.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_version = response.parse()
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_versions.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_version = response.parse()
            assert_matches_type(EventVersionResponse, event_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.event_versions.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: EventPortal) -> None:
        event_version = client.api.v2.architecture.event_versions.update(
            id="id",
            event_id="acb2j5k3mly",
            version="1.0.0",
        )
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: EventPortal) -> None:
        event_version = client.api.v2.architecture.event_versions.update(
            id="id",
            event_id="acb2j5k3mly",
            version="1.0.0",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            delivery_descriptor={
                "id": "id",
                "address": {
                    "address_levels": [
                        {
                            "address_level_type": "literal",
                            "name": "root",
                            "enum_version_id": "enumVersionId",
                        }
                    ],
                    "address_type": "topic",
                    "type": "type",
                },
                "broker_type": "brokerType",
                "key_schema_primitive_type": "BYTES",
                "key_schema_version_id": "shb3mlyec2g",
                "type": "type",
            },
            description="Event version created by Solace PubSub+ Cloud documentation",
            display_name="Display name for the version",
            end_of_life_date="2021-12-31T20:30:57.920Z",
            schema_primitive_type="BYTES",
            schema_version_id="shb3mlyec2g",
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
        )
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_versions.with_raw_response.update(
            id="id",
            event_id="acb2j5k3mly",
            version="1.0.0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_version = response.parse()
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_versions.with_streaming_response.update(
            id="id",
            event_id="acb2j5k3mly",
            version="1.0.0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_version = response.parse()
            assert_matches_type(EventVersionResponse, event_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.event_versions.with_raw_response.update(
                id="",
                event_id="acb2j5k3mly",
                version="1.0.0",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        event_version = client.api.v2.architecture.event_versions.list()
        assert_matches_type(EventVersionListResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        event_version = client.api.v2.architecture.event_versions.list(
            custom_attributes="customAttributes",
            event_ids=["string"],
            ids=["string"],
            messaging_service_ids=["string"],
            page_number=1,
            page_size=1,
            state_ids=["string"],
        )
        assert_matches_type(EventVersionListResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_versions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_version = response.parse()
        assert_matches_type(EventVersionListResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_versions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_version = response.parse()
            assert_matches_type(EventVersionListResponse, event_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: EventPortal) -> None:
        event_version = client.api.v2.architecture.event_versions.delete(
            "id",
        )
        assert event_version is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_versions.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_version = response.parse()
        assert event_version is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_versions.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_version = response.parse()
            assert event_version is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.event_versions.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_replace_messaging_service(self, client: EventPortal) -> None:
        event_version = client.api.v2.architecture.event_versions.replace_messaging_service(
            id="id",
        )
        assert_matches_type(MessagingServiceAssociationResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_replace_messaging_service_with_all_params(self, client: EventPortal) -> None:
        event_version = client.api.v2.architecture.event_versions.replace_messaging_service(
            id="id",
            messaging_service_ids=['["5h2km5khkj","h5mk26hkm2"]'],
        )
        assert_matches_type(MessagingServiceAssociationResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_replace_messaging_service(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_versions.with_raw_response.replace_messaging_service(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_version = response.parse()
        assert_matches_type(MessagingServiceAssociationResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_replace_messaging_service(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_versions.with_streaming_response.replace_messaging_service(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_version = response.parse()
            assert_matches_type(MessagingServiceAssociationResponse, event_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_replace_messaging_service(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.event_versions.with_raw_response.replace_messaging_service(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update_state(self, client: EventPortal) -> None:
        event_version = client.api.v2.architecture.event_versions.update_state(
            id="id",
        )
        assert_matches_type(StateChangeRequestResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_state_with_all_params(self, client: EventPortal) -> None:
        event_version = client.api.v2.architecture.event_versions.update_state(
            id="id",
            state_id="1",
        )
        assert_matches_type(StateChangeRequestResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update_state(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_versions.with_raw_response.update_state(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_version = response.parse()
        assert_matches_type(StateChangeRequestResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update_state(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_versions.with_streaming_response.update_state(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_version = response.parse()
            assert_matches_type(StateChangeRequestResponse, event_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update_state(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.event_versions.with_raw_response.update_state(
                id="",
            )


class TestAsyncEventVersions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        event_version = await async_client.api.v2.architecture.event_versions.create(
            event_id="acb2j5k3mly",
            version="1.0.0",
        )
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_version = await async_client.api.v2.architecture.event_versions.create(
            event_id="acb2j5k3mly",
            version="1.0.0",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            delivery_descriptor={
                "id": "id",
                "address": {
                    "address_levels": [
                        {
                            "address_level_type": "literal",
                            "name": "root",
                            "enum_version_id": "enumVersionId",
                        }
                    ],
                    "address_type": "topic",
                    "type": "type",
                },
                "broker_type": "brokerType",
                "key_schema_primitive_type": "BYTES",
                "key_schema_version_id": "shb3mlyec2g",
                "type": "type",
            },
            description="Event version created by Solace PubSub+ Cloud documentation",
            display_name="Display name for the version",
            end_of_life_date="2021-12-31T20:30:57.920Z",
            schema_primitive_type="BYTES",
            schema_version_id="shb3mlyec2g",
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
        )
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_versions.with_raw_response.create(
            event_id="acb2j5k3mly",
            version="1.0.0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_version = await response.parse()
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_versions.with_streaming_response.create(
            event_id="acb2j5k3mly",
            version="1.0.0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_version = await response.parse()
            assert_matches_type(EventVersionResponse, event_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        event_version = await async_client.api.v2.architecture.event_versions.retrieve(
            "id",
        )
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_versions.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_version = await response.parse()
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_versions.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_version = await response.parse()
            assert_matches_type(EventVersionResponse, event_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.event_versions.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncEventPortal) -> None:
        event_version = await async_client.api.v2.architecture.event_versions.update(
            id="id",
            event_id="acb2j5k3mly",
            version="1.0.0",
        )
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_version = await async_client.api.v2.architecture.event_versions.update(
            id="id",
            event_id="acb2j5k3mly",
            version="1.0.0",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            delivery_descriptor={
                "id": "id",
                "address": {
                    "address_levels": [
                        {
                            "address_level_type": "literal",
                            "name": "root",
                            "enum_version_id": "enumVersionId",
                        }
                    ],
                    "address_type": "topic",
                    "type": "type",
                },
                "broker_type": "brokerType",
                "key_schema_primitive_type": "BYTES",
                "key_schema_version_id": "shb3mlyec2g",
                "type": "type",
            },
            description="Event version created by Solace PubSub+ Cloud documentation",
            display_name="Display name for the version",
            end_of_life_date="2021-12-31T20:30:57.920Z",
            schema_primitive_type="BYTES",
            schema_version_id="shb3mlyec2g",
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
        )
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_versions.with_raw_response.update(
            id="id",
            event_id="acb2j5k3mly",
            version="1.0.0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_version = await response.parse()
        assert_matches_type(EventVersionResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_versions.with_streaming_response.update(
            id="id",
            event_id="acb2j5k3mly",
            version="1.0.0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_version = await response.parse()
            assert_matches_type(EventVersionResponse, event_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.event_versions.with_raw_response.update(
                id="",
                event_id="acb2j5k3mly",
                version="1.0.0",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        event_version = await async_client.api.v2.architecture.event_versions.list()
        assert_matches_type(EventVersionListResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_version = await async_client.api.v2.architecture.event_versions.list(
            custom_attributes="customAttributes",
            event_ids=["string"],
            ids=["string"],
            messaging_service_ids=["string"],
            page_number=1,
            page_size=1,
            state_ids=["string"],
        )
        assert_matches_type(EventVersionListResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_versions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_version = await response.parse()
        assert_matches_type(EventVersionListResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_versions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_version = await response.parse()
            assert_matches_type(EventVersionListResponse, event_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncEventPortal) -> None:
        event_version = await async_client.api.v2.architecture.event_versions.delete(
            "id",
        )
        assert event_version is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_versions.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_version = await response.parse()
        assert event_version is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_versions.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_version = await response.parse()
            assert event_version is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.event_versions.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_replace_messaging_service(self, async_client: AsyncEventPortal) -> None:
        event_version = await async_client.api.v2.architecture.event_versions.replace_messaging_service(
            id="id",
        )
        assert_matches_type(MessagingServiceAssociationResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_replace_messaging_service_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_version = await async_client.api.v2.architecture.event_versions.replace_messaging_service(
            id="id",
            messaging_service_ids=['["5h2km5khkj","h5mk26hkm2"]'],
        )
        assert_matches_type(MessagingServiceAssociationResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_replace_messaging_service(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_versions.with_raw_response.replace_messaging_service(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_version = await response.parse()
        assert_matches_type(MessagingServiceAssociationResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_replace_messaging_service(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_versions.with_streaming_response.replace_messaging_service(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_version = await response.parse()
            assert_matches_type(MessagingServiceAssociationResponse, event_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_replace_messaging_service(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.event_versions.with_raw_response.replace_messaging_service(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_state(self, async_client: AsyncEventPortal) -> None:
        event_version = await async_client.api.v2.architecture.event_versions.update_state(
            id="id",
        )
        assert_matches_type(StateChangeRequestResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_state_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_version = await async_client.api.v2.architecture.event_versions.update_state(
            id="id",
            state_id="1",
        )
        assert_matches_type(StateChangeRequestResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update_state(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_versions.with_raw_response.update_state(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_version = await response.parse()
        assert_matches_type(StateChangeRequestResponse, event_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update_state(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_versions.with_streaming_response.update_state(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_version = await response.parse()
            assert_matches_type(StateChangeRequestResponse, event_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update_state(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.event_versions.with_raw_response.update_state(
                id="",
            )
