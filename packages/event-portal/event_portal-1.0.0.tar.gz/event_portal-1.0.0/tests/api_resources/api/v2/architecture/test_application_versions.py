# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal.types.api.v2.architecture import (
    ApplicationVersionResponse,
    StateChangeRequestResponse,
    ApplicationVersionListResponse,
    MessagingServiceAssociationResponse,
    ApplicationVersionEventAccessRequestsResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApplicationVersions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.create(
            application_id="acb2j5k3mly",
            version="1.0.0",
        )
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.create(
            application_id="acb2j5k3mly",
            version="1.0.0",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            declared_consumed_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            declared_event_api_product_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            declared_produced_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            description="Application created by Solace PubSub+ Cloud documentation",
            display_name="Display name for the version",
            end_of_life_date="2021-12-31T20:30:57.920Z",
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
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_versions.with_raw_response.create(
            application_id="acb2j5k3mly",
            version="1.0.0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = response.parse()
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_versions.with_streaming_response.create(
            application_id="acb2j5k3mly",
            version="1.0.0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = response.parse()
            assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.retrieve(
            "versionId",
        )
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_versions.with_raw_response.retrieve(
            "versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = response.parse()
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_versions.with_streaming_response.retrieve(
            "versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = response.parse()
            assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.api.v2.architecture.application_versions.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.update(
            version_id="versionId",
            application_id="acb2j5k3mly",
            version="1.0.0",
        )
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.update(
            version_id="versionId",
            application_id="acb2j5k3mly",
            version="1.0.0",
            include=["string"],
            relations_broker_type="relationsBrokerType",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            declared_consumed_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            declared_event_api_product_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            declared_produced_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            description="Application created by Solace PubSub+ Cloud documentation",
            display_name="Display name for the version",
            end_of_life_date="2021-12-31T20:30:57.920Z",
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
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_versions.with_raw_response.update(
            version_id="versionId",
            application_id="acb2j5k3mly",
            version="1.0.0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = response.parse()
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_versions.with_streaming_response.update(
            version_id="versionId",
            application_id="acb2j5k3mly",
            version="1.0.0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = response.parse()
            assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.api.v2.architecture.application_versions.with_raw_response.update(
                version_id="",
                application_id="acb2j5k3mly",
                version="1.0.0",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.list()
        assert_matches_type(ApplicationVersionListResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.list(
            application_ids=["string"],
            ids=["string"],
            messaging_service_ids=["string"],
            page_number=1,
            page_size=1,
            state_ids=["string"],
        )
        assert_matches_type(ApplicationVersionListResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_versions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = response.parse()
        assert_matches_type(ApplicationVersionListResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_versions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = response.parse()
            assert_matches_type(ApplicationVersionListResponse, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.delete(
            "versionId",
        )
        assert application_version is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_versions.with_raw_response.delete(
            "versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = response.parse()
        assert application_version is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_versions.with_streaming_response.delete(
            "versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = response.parse()
            assert application_version is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.api.v2.architecture.application_versions.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_async_api(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.get_async_api(
            application_version_id="applicationVersionId",
        )
        assert_matches_type(str, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_async_api_with_all_params(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.get_async_api(
            application_version_id="applicationVersionId",
            async_api_version="2.0.0",
            context_id="contextId",
            context_type="eventBroker",
            environment_options="include_declared_and_attracted_events",
            expand="declaredSubscribedEvents",
            format="json",
            included_extensions="all",
            messaging_service_id="messagingServiceId",
            show_versioning=True,
        )
        assert_matches_type(str, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_async_api(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_versions.with_raw_response.get_async_api(
            application_version_id="applicationVersionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = response.parse()
        assert_matches_type(str, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_async_api(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_versions.with_streaming_response.get_async_api(
            application_version_id="applicationVersionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = response.parse()
            assert_matches_type(str, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_async_api(self, client: EventPortal) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_version_id` but received ''"
        ):
            client.api.v2.architecture.application_versions.with_raw_response.get_async_api(
                application_version_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_event_access_request_preview(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.get_event_access_request_preview(
            "applicationVersionId",
        )
        assert_matches_type(ApplicationVersionEventAccessRequestsResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_event_access_request_preview(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_versions.with_raw_response.get_event_access_request_preview(
            "applicationVersionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = response.parse()
        assert_matches_type(ApplicationVersionEventAccessRequestsResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_event_access_request_preview(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_versions.with_streaming_response.get_event_access_request_preview(
            "applicationVersionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = response.parse()
            assert_matches_type(ApplicationVersionEventAccessRequestsResponse, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_event_access_request_preview(self, client: EventPortal) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_version_id` but received ''"
        ):
            client.api.v2.architecture.application_versions.with_raw_response.get_event_access_request_preview(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_replace_messaging_service(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.replace_messaging_service(
            version_id="versionId",
        )
        assert_matches_type(MessagingServiceAssociationResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_replace_messaging_service_with_all_params(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.replace_messaging_service(
            version_id="versionId",
            messaging_service_ids=['["5h2km5khkj","h5mk26hkm2"]'],
        )
        assert_matches_type(MessagingServiceAssociationResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_replace_messaging_service(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_versions.with_raw_response.replace_messaging_service(
            version_id="versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = response.parse()
        assert_matches_type(MessagingServiceAssociationResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_replace_messaging_service(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_versions.with_streaming_response.replace_messaging_service(
            version_id="versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = response.parse()
            assert_matches_type(MessagingServiceAssociationResponse, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_replace_messaging_service(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.api.v2.architecture.application_versions.with_raw_response.replace_messaging_service(
                version_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update_state(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.update_state(
            version_id="versionId",
        )
        assert_matches_type(StateChangeRequestResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_state_with_all_params(self, client: EventPortal) -> None:
        application_version = client.api.v2.architecture.application_versions.update_state(
            version_id="versionId",
            state_id="1",
        )
        assert_matches_type(StateChangeRequestResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update_state(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_versions.with_raw_response.update_state(
            version_id="versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = response.parse()
        assert_matches_type(StateChangeRequestResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update_state(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_versions.with_streaming_response.update_state(
            version_id="versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = response.parse()
            assert_matches_type(StateChangeRequestResponse, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update_state(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.api.v2.architecture.application_versions.with_raw_response.update_state(
                version_id="",
            )


class TestAsyncApplicationVersions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        application_version = await async_client.api.v2.architecture.application_versions.create(
            application_id="acb2j5k3mly",
            version="1.0.0",
        )
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEventPortal) -> None:
        application_version = await async_client.api.v2.architecture.application_versions.create(
            application_id="acb2j5k3mly",
            version="1.0.0",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            declared_consumed_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            declared_event_api_product_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            declared_produced_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            description="Application created by Solace PubSub+ Cloud documentation",
            display_name="Display name for the version",
            end_of_life_date="2021-12-31T20:30:57.920Z",
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
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_versions.with_raw_response.create(
            application_id="acb2j5k3mly",
            version="1.0.0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = await response.parse()
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_versions.with_streaming_response.create(
            application_id="acb2j5k3mly",
            version="1.0.0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = await response.parse()
            assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        application_version = await async_client.api.v2.architecture.application_versions.retrieve(
            "versionId",
        )
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_versions.with_raw_response.retrieve(
            "versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = await response.parse()
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_versions.with_streaming_response.retrieve(
            "versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = await response.parse()
            assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.api.v2.architecture.application_versions.with_raw_response.retrieve(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncEventPortal) -> None:
        application_version = await async_client.api.v2.architecture.application_versions.update(
            version_id="versionId",
            application_id="acb2j5k3mly",
            version="1.0.0",
        )
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEventPortal) -> None:
        application_version = await async_client.api.v2.architecture.application_versions.update(
            version_id="versionId",
            application_id="acb2j5k3mly",
            version="1.0.0",
            include=["string"],
            relations_broker_type="relationsBrokerType",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            declared_consumed_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            declared_event_api_product_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            declared_produced_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            description="Application created by Solace PubSub+ Cloud documentation",
            display_name="Display name for the version",
            end_of_life_date="2021-12-31T20:30:57.920Z",
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
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_versions.with_raw_response.update(
            version_id="versionId",
            application_id="acb2j5k3mly",
            version="1.0.0",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = await response.parse()
        assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_versions.with_streaming_response.update(
            version_id="versionId",
            application_id="acb2j5k3mly",
            version="1.0.0",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = await response.parse()
            assert_matches_type(ApplicationVersionResponse, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.api.v2.architecture.application_versions.with_raw_response.update(
                version_id="",
                application_id="acb2j5k3mly",
                version="1.0.0",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        application_version = await async_client.api.v2.architecture.application_versions.list()
        assert_matches_type(ApplicationVersionListResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        application_version = await async_client.api.v2.architecture.application_versions.list(
            application_ids=["string"],
            ids=["string"],
            messaging_service_ids=["string"],
            page_number=1,
            page_size=1,
            state_ids=["string"],
        )
        assert_matches_type(ApplicationVersionListResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_versions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = await response.parse()
        assert_matches_type(ApplicationVersionListResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_versions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = await response.parse()
            assert_matches_type(ApplicationVersionListResponse, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncEventPortal) -> None:
        application_version = await async_client.api.v2.architecture.application_versions.delete(
            "versionId",
        )
        assert application_version is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_versions.with_raw_response.delete(
            "versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = await response.parse()
        assert application_version is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_versions.with_streaming_response.delete(
            "versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = await response.parse()
            assert application_version is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.api.v2.architecture.application_versions.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_async_api(self, async_client: AsyncEventPortal) -> None:
        application_version = await async_client.api.v2.architecture.application_versions.get_async_api(
            application_version_id="applicationVersionId",
        )
        assert_matches_type(str, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_async_api_with_all_params(self, async_client: AsyncEventPortal) -> None:
        application_version = await async_client.api.v2.architecture.application_versions.get_async_api(
            application_version_id="applicationVersionId",
            async_api_version="2.0.0",
            context_id="contextId",
            context_type="eventBroker",
            environment_options="include_declared_and_attracted_events",
            expand="declaredSubscribedEvents",
            format="json",
            included_extensions="all",
            messaging_service_id="messagingServiceId",
            show_versioning=True,
        )
        assert_matches_type(str, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_async_api(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_versions.with_raw_response.get_async_api(
            application_version_id="applicationVersionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = await response.parse()
        assert_matches_type(str, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_async_api(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_versions.with_streaming_response.get_async_api(
            application_version_id="applicationVersionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = await response.parse()
            assert_matches_type(str, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_async_api(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_version_id` but received ''"
        ):
            await async_client.api.v2.architecture.application_versions.with_raw_response.get_async_api(
                application_version_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_event_access_request_preview(self, async_client: AsyncEventPortal) -> None:
        application_version = (
            await async_client.api.v2.architecture.application_versions.get_event_access_request_preview(
                "applicationVersionId",
            )
        )
        assert_matches_type(ApplicationVersionEventAccessRequestsResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_event_access_request_preview(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_versions.with_raw_response.get_event_access_request_preview(
            "applicationVersionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = await response.parse()
        assert_matches_type(ApplicationVersionEventAccessRequestsResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_event_access_request_preview(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_versions.with_streaming_response.get_event_access_request_preview(
            "applicationVersionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = await response.parse()
            assert_matches_type(ApplicationVersionEventAccessRequestsResponse, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_event_access_request_preview(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(
            ValueError, match=r"Expected a non-empty value for `application_version_id` but received ''"
        ):
            await async_client.api.v2.architecture.application_versions.with_raw_response.get_event_access_request_preview(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_replace_messaging_service(self, async_client: AsyncEventPortal) -> None:
        application_version = await async_client.api.v2.architecture.application_versions.replace_messaging_service(
            version_id="versionId",
        )
        assert_matches_type(MessagingServiceAssociationResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_replace_messaging_service_with_all_params(self, async_client: AsyncEventPortal) -> None:
        application_version = await async_client.api.v2.architecture.application_versions.replace_messaging_service(
            version_id="versionId",
            messaging_service_ids=['["5h2km5khkj","h5mk26hkm2"]'],
        )
        assert_matches_type(MessagingServiceAssociationResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_replace_messaging_service(self, async_client: AsyncEventPortal) -> None:
        response = (
            await async_client.api.v2.architecture.application_versions.with_raw_response.replace_messaging_service(
                version_id="versionId",
            )
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = await response.parse()
        assert_matches_type(MessagingServiceAssociationResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_replace_messaging_service(self, async_client: AsyncEventPortal) -> None:
        async with (
            async_client.api.v2.architecture.application_versions.with_streaming_response.replace_messaging_service(
                version_id="versionId",
            )
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = await response.parse()
            assert_matches_type(MessagingServiceAssociationResponse, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_replace_messaging_service(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.api.v2.architecture.application_versions.with_raw_response.replace_messaging_service(
                version_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_state(self, async_client: AsyncEventPortal) -> None:
        application_version = await async_client.api.v2.architecture.application_versions.update_state(
            version_id="versionId",
        )
        assert_matches_type(StateChangeRequestResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_state_with_all_params(self, async_client: AsyncEventPortal) -> None:
        application_version = await async_client.api.v2.architecture.application_versions.update_state(
            version_id="versionId",
            state_id="1",
        )
        assert_matches_type(StateChangeRequestResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update_state(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_versions.with_raw_response.update_state(
            version_id="versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_version = await response.parse()
        assert_matches_type(StateChangeRequestResponse, application_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update_state(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_versions.with_streaming_response.update_state(
            version_id="versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_version = await response.parse()
            assert_matches_type(StateChangeRequestResponse, application_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update_state(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.api.v2.architecture.application_versions.with_raw_response.update_state(
                version_id="",
            )
