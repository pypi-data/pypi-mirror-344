# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal.types.api.v2.architecture import (
    StateChangeRequestResponse,
    EventAPIProductVersionResponse,
    EventAPIProductVersionListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEventAPIProductVersions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: EventPortal) -> None:
        event_api_product_version = client.api.v2.architecture.event_api_product_versions.create(
            event_api_product_id="acb2j5k3mly",
        )
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: EventPortal) -> None:
        event_api_product_version = client.api.v2.architecture.event_api_product_versions.create(
            event_api_product_id="acb2j5k3mly",
            approval_type="automatic",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            description="Event API product created by Solace PubSub+ Cloud documentation",
            display_name="Event API product version display name",
            end_of_life_date="2021-12-31T20:30:57.920Z",
            event_api_product_registrations=[
                {
                    "access_request_id": "12345678",
                    "application_domain_id": "12345678",
                    "event_api_product_version_id": "12345678",
                    "plan_id": "12345678",
                    "registration_id": "12345678",
                    "custom_attributes": {"foo": "string"},
                    "state": "Pending Approval",
                }
            ],
            event_api_version_ids=["string"],
            filters=[
                {
                    "id": "id",
                    "event_version_id": "123456",
                    "topic_filters": [
                        {
                            "event_version_ids": ["string"],
                            "filter_value": " Tes?, TEST*FILTER, SAmPle",
                            "name": "name",
                        }
                    ],
                }
            ],
            plans=[
                {
                    "name": "Gold",
                    "solace_class_of_service_policy": {
                        "access_type": "exclusive",
                        "maximum_time_to_live": 1500,
                        "max_msg_spool_usage": 5,
                        "message_delivery_mode": "direct",
                        "queue_type": "single",
                    },
                }
            ],
            publish_state="unset",
            solace_messaging_services=[
                {
                    "solace_cloud_messaging_service_id": "service123",
                    "supported_protocols": ["string"],
                }
            ],
            state_id="1",
            summary="Summary string value of event API product version",
            version="1.0.0",
        )
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_product_versions.with_raw_response.create(
            event_api_product_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_product_version = response.parse()
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_product_versions.with_streaming_response.create(
            event_api_product_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_product_version = response.parse()
            assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        event_api_product_version = client.api.v2.architecture.event_api_product_versions.retrieve(
            version_id="versionId",
        )
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: EventPortal) -> None:
        event_api_product_version = client.api.v2.architecture.event_api_product_versions.retrieve(
            version_id="versionId",
            client_app_id="clientAppId",
            include="include",
        )
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_product_versions.with_raw_response.retrieve(
            version_id="versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_product_version = response.parse()
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_product_versions.with_streaming_response.retrieve(
            version_id="versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_product_version = response.parse()
            assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.api.v2.architecture.event_api_product_versions.with_raw_response.retrieve(
                version_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: EventPortal) -> None:
        event_api_product_version = client.api.v2.architecture.event_api_product_versions.update(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        )
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: EventPortal) -> None:
        event_api_product_version = client.api.v2.architecture.event_api_product_versions.update(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
            approval_type="automatic",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            description="Event API product created by Solace PubSub+ Cloud documentation",
            display_name="Event API product version display name",
            end_of_life_date="2021-12-31T20:30:57.920Z",
            event_api_product_registrations=[
                {
                    "access_request_id": "12345678",
                    "application_domain_id": "12345678",
                    "event_api_product_version_id": "12345678",
                    "plan_id": "12345678",
                    "registration_id": "12345678",
                    "custom_attributes": {"foo": "string"},
                    "state": "Pending Approval",
                }
            ],
            event_api_version_ids=["string"],
            filters=[
                {
                    "id": "id",
                    "event_version_id": "123456",
                    "topic_filters": [
                        {
                            "event_version_ids": ["string"],
                            "filter_value": " Tes?, TEST*FILTER, SAmPle",
                            "name": "name",
                        }
                    ],
                }
            ],
            plans=[
                {
                    "name": "Gold",
                    "solace_class_of_service_policy": {
                        "access_type": "exclusive",
                        "maximum_time_to_live": 1500,
                        "max_msg_spool_usage": 5,
                        "message_delivery_mode": "direct",
                        "queue_type": "single",
                    },
                }
            ],
            publish_state="unset",
            solace_messaging_services=[
                {
                    "solace_cloud_messaging_service_id": "service123",
                    "supported_protocols": ["string"],
                }
            ],
            state_id="1",
            summary="Summary string value of event API product version",
            version="1.0.0",
        )
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_product_versions.with_raw_response.update(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_product_version = response.parse()
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_product_versions.with_streaming_response.update(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_product_version = response.parse()
            assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.api.v2.architecture.event_api_product_versions.with_raw_response.update(
                version_id="",
                event_api_product_id="acb2j5k3mly",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        event_api_product_version = client.api.v2.architecture.event_api_product_versions.list()
        assert_matches_type(EventAPIProductVersionListResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        event_api_product_version = client.api.v2.architecture.event_api_product_versions.list(
            client_app_id="clientAppId",
            custom_attributes="customAttributes",
            event_api_product_ids=["string"],
            ids=["string"],
            include="include",
            latest=True,
            messaging_service_id="messagingServiceId",
            page_number=1,
            page_size=1,
            shared=True,
            state_id="stateId",
        )
        assert_matches_type(EventAPIProductVersionListResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_product_versions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_product_version = response.parse()
        assert_matches_type(EventAPIProductVersionListResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_product_versions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_product_version = response.parse()
            assert_matches_type(EventAPIProductVersionListResponse, event_api_product_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: EventPortal) -> None:
        event_api_product_version = client.api.v2.architecture.event_api_product_versions.delete(
            "versionId",
        )
        assert event_api_product_version is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_product_versions.with_raw_response.delete(
            "versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_product_version = response.parse()
        assert event_api_product_version is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_product_versions.with_streaming_response.delete(
            "versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_product_version = response.parse()
            assert event_api_product_version is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.api.v2.architecture.event_api_product_versions.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_publish(self, client: EventPortal) -> None:
        event_api_product_version = client.api.v2.architecture.event_api_product_versions.publish(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        )
        assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_publish_with_all_params(self, client: EventPortal) -> None:
        event_api_product_version = client.api.v2.architecture.event_api_product_versions.publish(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
            approval_type="automatic",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            description="Event API product created by Solace PubSub+ Cloud documentation",
            display_name="Event API product version display name",
            end_of_life_date="2021-12-31T20:30:57.920Z",
            event_api_product_registrations=[
                {
                    "access_request_id": "12345678",
                    "application_domain_id": "12345678",
                    "event_api_product_version_id": "12345678",
                    "plan_id": "12345678",
                    "registration_id": "12345678",
                    "custom_attributes": {"foo": "string"},
                    "state": "Pending Approval",
                }
            ],
            event_api_version_ids=["string"],
            filters=[
                {
                    "id": "id",
                    "event_version_id": "123456",
                    "topic_filters": [
                        {
                            "event_version_ids": ["string"],
                            "filter_value": " Tes?, TEST*FILTER, SAmPle",
                            "name": "name",
                        }
                    ],
                }
            ],
            plans=[
                {
                    "name": "Gold",
                    "solace_class_of_service_policy": {
                        "access_type": "exclusive",
                        "maximum_time_to_live": 1500,
                        "max_msg_spool_usage": 5,
                        "message_delivery_mode": "direct",
                        "queue_type": "single",
                    },
                }
            ],
            publish_state="unset",
            solace_messaging_services=[
                {
                    "solace_cloud_messaging_service_id": "service123",
                    "supported_protocols": ["string"],
                }
            ],
            state_id="1",
            summary="Summary string value of event API product version",
            version="1.0.0",
        )
        assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_publish(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_product_versions.with_raw_response.publish(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_product_version = response.parse()
        assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_publish(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_product_versions.with_streaming_response.publish(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_product_version = response.parse()
            assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_publish(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.api.v2.architecture.event_api_product_versions.with_raw_response.publish(
                version_id="",
                event_api_product_id="acb2j5k3mly",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update_state(self, client: EventPortal) -> None:
        event_api_product_version = client.api.v2.architecture.event_api_product_versions.update_state(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        )
        assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_state_with_all_params(self, client: EventPortal) -> None:
        event_api_product_version = client.api.v2.architecture.event_api_product_versions.update_state(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
            approval_type="automatic",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            description="Event API product created by Solace PubSub+ Cloud documentation",
            display_name="Event API product version display name",
            end_of_life_date="2021-12-31T20:30:57.920Z",
            event_api_product_registrations=[
                {
                    "access_request_id": "12345678",
                    "application_domain_id": "12345678",
                    "event_api_product_version_id": "12345678",
                    "plan_id": "12345678",
                    "registration_id": "12345678",
                    "custom_attributes": {"foo": "string"},
                    "state": "Pending Approval",
                }
            ],
            event_api_version_ids=["string"],
            filters=[
                {
                    "id": "id",
                    "event_version_id": "123456",
                    "topic_filters": [
                        {
                            "event_version_ids": ["string"],
                            "filter_value": " Tes?, TEST*FILTER, SAmPle",
                            "name": "name",
                        }
                    ],
                }
            ],
            plans=[
                {
                    "name": "Gold",
                    "solace_class_of_service_policy": {
                        "access_type": "exclusive",
                        "maximum_time_to_live": 1500,
                        "max_msg_spool_usage": 5,
                        "message_delivery_mode": "direct",
                        "queue_type": "single",
                    },
                }
            ],
            publish_state="unset",
            solace_messaging_services=[
                {
                    "solace_cloud_messaging_service_id": "service123",
                    "supported_protocols": ["string"],
                }
            ],
            state_id="1",
            summary="Summary string value of event API product version",
            version="1.0.0",
        )
        assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update_state(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_product_versions.with_raw_response.update_state(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_product_version = response.parse()
        assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update_state(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_product_versions.with_streaming_response.update_state(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_product_version = response.parse()
            assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update_state(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.api.v2.architecture.event_api_product_versions.with_raw_response.update_state(
                version_id="",
                event_api_product_id="acb2j5k3mly",
            )


class TestAsyncEventAPIProductVersions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        event_api_product_version = await async_client.api.v2.architecture.event_api_product_versions.create(
            event_api_product_id="acb2j5k3mly",
        )
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_api_product_version = await async_client.api.v2.architecture.event_api_product_versions.create(
            event_api_product_id="acb2j5k3mly",
            approval_type="automatic",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            description="Event API product created by Solace PubSub+ Cloud documentation",
            display_name="Event API product version display name",
            end_of_life_date="2021-12-31T20:30:57.920Z",
            event_api_product_registrations=[
                {
                    "access_request_id": "12345678",
                    "application_domain_id": "12345678",
                    "event_api_product_version_id": "12345678",
                    "plan_id": "12345678",
                    "registration_id": "12345678",
                    "custom_attributes": {"foo": "string"},
                    "state": "Pending Approval",
                }
            ],
            event_api_version_ids=["string"],
            filters=[
                {
                    "id": "id",
                    "event_version_id": "123456",
                    "topic_filters": [
                        {
                            "event_version_ids": ["string"],
                            "filter_value": " Tes?, TEST*FILTER, SAmPle",
                            "name": "name",
                        }
                    ],
                }
            ],
            plans=[
                {
                    "name": "Gold",
                    "solace_class_of_service_policy": {
                        "access_type": "exclusive",
                        "maximum_time_to_live": 1500,
                        "max_msg_spool_usage": 5,
                        "message_delivery_mode": "direct",
                        "queue_type": "single",
                    },
                }
            ],
            publish_state="unset",
            solace_messaging_services=[
                {
                    "solace_cloud_messaging_service_id": "service123",
                    "supported_protocols": ["string"],
                }
            ],
            state_id="1",
            summary="Summary string value of event API product version",
            version="1.0.0",
        )
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_product_versions.with_raw_response.create(
            event_api_product_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_product_version = await response.parse()
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_api_product_versions.with_streaming_response.create(
            event_api_product_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_product_version = await response.parse()
            assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        event_api_product_version = await async_client.api.v2.architecture.event_api_product_versions.retrieve(
            version_id="versionId",
        )
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_api_product_version = await async_client.api.v2.architecture.event_api_product_versions.retrieve(
            version_id="versionId",
            client_app_id="clientAppId",
            include="include",
        )
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_product_versions.with_raw_response.retrieve(
            version_id="versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_product_version = await response.parse()
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_api_product_versions.with_streaming_response.retrieve(
            version_id="versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_product_version = await response.parse()
            assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.api.v2.architecture.event_api_product_versions.with_raw_response.retrieve(
                version_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncEventPortal) -> None:
        event_api_product_version = await async_client.api.v2.architecture.event_api_product_versions.update(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        )
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_api_product_version = await async_client.api.v2.architecture.event_api_product_versions.update(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
            approval_type="automatic",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            description="Event API product created by Solace PubSub+ Cloud documentation",
            display_name="Event API product version display name",
            end_of_life_date="2021-12-31T20:30:57.920Z",
            event_api_product_registrations=[
                {
                    "access_request_id": "12345678",
                    "application_domain_id": "12345678",
                    "event_api_product_version_id": "12345678",
                    "plan_id": "12345678",
                    "registration_id": "12345678",
                    "custom_attributes": {"foo": "string"},
                    "state": "Pending Approval",
                }
            ],
            event_api_version_ids=["string"],
            filters=[
                {
                    "id": "id",
                    "event_version_id": "123456",
                    "topic_filters": [
                        {
                            "event_version_ids": ["string"],
                            "filter_value": " Tes?, TEST*FILTER, SAmPle",
                            "name": "name",
                        }
                    ],
                }
            ],
            plans=[
                {
                    "name": "Gold",
                    "solace_class_of_service_policy": {
                        "access_type": "exclusive",
                        "maximum_time_to_live": 1500,
                        "max_msg_spool_usage": 5,
                        "message_delivery_mode": "direct",
                        "queue_type": "single",
                    },
                }
            ],
            publish_state="unset",
            solace_messaging_services=[
                {
                    "solace_cloud_messaging_service_id": "service123",
                    "supported_protocols": ["string"],
                }
            ],
            state_id="1",
            summary="Summary string value of event API product version",
            version="1.0.0",
        )
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_product_versions.with_raw_response.update(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_product_version = await response.parse()
        assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_api_product_versions.with_streaming_response.update(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_product_version = await response.parse()
            assert_matches_type(EventAPIProductVersionResponse, event_api_product_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.api.v2.architecture.event_api_product_versions.with_raw_response.update(
                version_id="",
                event_api_product_id="acb2j5k3mly",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        event_api_product_version = await async_client.api.v2.architecture.event_api_product_versions.list()
        assert_matches_type(EventAPIProductVersionListResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_api_product_version = await async_client.api.v2.architecture.event_api_product_versions.list(
            client_app_id="clientAppId",
            custom_attributes="customAttributes",
            event_api_product_ids=["string"],
            ids=["string"],
            include="include",
            latest=True,
            messaging_service_id="messagingServiceId",
            page_number=1,
            page_size=1,
            shared=True,
            state_id="stateId",
        )
        assert_matches_type(EventAPIProductVersionListResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_product_versions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_product_version = await response.parse()
        assert_matches_type(EventAPIProductVersionListResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with (
            async_client.api.v2.architecture.event_api_product_versions.with_streaming_response.list()
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_product_version = await response.parse()
            assert_matches_type(EventAPIProductVersionListResponse, event_api_product_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncEventPortal) -> None:
        event_api_product_version = await async_client.api.v2.architecture.event_api_product_versions.delete(
            "versionId",
        )
        assert event_api_product_version is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_product_versions.with_raw_response.delete(
            "versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_product_version = await response.parse()
        assert event_api_product_version is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_api_product_versions.with_streaming_response.delete(
            "versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_product_version = await response.parse()
            assert event_api_product_version is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.api.v2.architecture.event_api_product_versions.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_publish(self, async_client: AsyncEventPortal) -> None:
        event_api_product_version = await async_client.api.v2.architecture.event_api_product_versions.publish(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        )
        assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_publish_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_api_product_version = await async_client.api.v2.architecture.event_api_product_versions.publish(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
            approval_type="automatic",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            description="Event API product created by Solace PubSub+ Cloud documentation",
            display_name="Event API product version display name",
            end_of_life_date="2021-12-31T20:30:57.920Z",
            event_api_product_registrations=[
                {
                    "access_request_id": "12345678",
                    "application_domain_id": "12345678",
                    "event_api_product_version_id": "12345678",
                    "plan_id": "12345678",
                    "registration_id": "12345678",
                    "custom_attributes": {"foo": "string"},
                    "state": "Pending Approval",
                }
            ],
            event_api_version_ids=["string"],
            filters=[
                {
                    "id": "id",
                    "event_version_id": "123456",
                    "topic_filters": [
                        {
                            "event_version_ids": ["string"],
                            "filter_value": " Tes?, TEST*FILTER, SAmPle",
                            "name": "name",
                        }
                    ],
                }
            ],
            plans=[
                {
                    "name": "Gold",
                    "solace_class_of_service_policy": {
                        "access_type": "exclusive",
                        "maximum_time_to_live": 1500,
                        "max_msg_spool_usage": 5,
                        "message_delivery_mode": "direct",
                        "queue_type": "single",
                    },
                }
            ],
            publish_state="unset",
            solace_messaging_services=[
                {
                    "solace_cloud_messaging_service_id": "service123",
                    "supported_protocols": ["string"],
                }
            ],
            state_id="1",
            summary="Summary string value of event API product version",
            version="1.0.0",
        )
        assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_publish(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_product_versions.with_raw_response.publish(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_product_version = await response.parse()
        assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_publish(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_api_product_versions.with_streaming_response.publish(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_product_version = await response.parse()
            assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_publish(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.api.v2.architecture.event_api_product_versions.with_raw_response.publish(
                version_id="",
                event_api_product_id="acb2j5k3mly",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_state(self, async_client: AsyncEventPortal) -> None:
        event_api_product_version = await async_client.api.v2.architecture.event_api_product_versions.update_state(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        )
        assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_state_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_api_product_version = await async_client.api.v2.architecture.event_api_product_versions.update_state(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
            approval_type="automatic",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            description="Event API product created by Solace PubSub+ Cloud documentation",
            display_name="Event API product version display name",
            end_of_life_date="2021-12-31T20:30:57.920Z",
            event_api_product_registrations=[
                {
                    "access_request_id": "12345678",
                    "application_domain_id": "12345678",
                    "event_api_product_version_id": "12345678",
                    "plan_id": "12345678",
                    "registration_id": "12345678",
                    "custom_attributes": {"foo": "string"},
                    "state": "Pending Approval",
                }
            ],
            event_api_version_ids=["string"],
            filters=[
                {
                    "id": "id",
                    "event_version_id": "123456",
                    "topic_filters": [
                        {
                            "event_version_ids": ["string"],
                            "filter_value": " Tes?, TEST*FILTER, SAmPle",
                            "name": "name",
                        }
                    ],
                }
            ],
            plans=[
                {
                    "name": "Gold",
                    "solace_class_of_service_policy": {
                        "access_type": "exclusive",
                        "maximum_time_to_live": 1500,
                        "max_msg_spool_usage": 5,
                        "message_delivery_mode": "direct",
                        "queue_type": "single",
                    },
                }
            ],
            publish_state="unset",
            solace_messaging_services=[
                {
                    "solace_cloud_messaging_service_id": "service123",
                    "supported_protocols": ["string"],
                }
            ],
            state_id="1",
            summary="Summary string value of event API product version",
            version="1.0.0",
        )
        assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update_state(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_product_versions.with_raw_response.update_state(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_product_version = await response.parse()
        assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update_state(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_api_product_versions.with_streaming_response.update_state(
            version_id="versionId",
            event_api_product_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_product_version = await response.parse()
            assert_matches_type(StateChangeRequestResponse, event_api_product_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update_state(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.api.v2.architecture.event_api_product_versions.with_raw_response.update_state(
                version_id="",
                event_api_product_id="acb2j5k3mly",
            )
