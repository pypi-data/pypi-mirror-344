# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import httpx
import pytest
from respx import MockRouter

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal._response import (
    BinaryAPIResponse,
    AsyncBinaryAPIResponse,
    StreamedBinaryAPIResponse,
    AsyncStreamedBinaryAPIResponse,
)
from event_portal.types.api.v2.architecture import (
    ApplicationDomainResponse,
    ApplicationDomainListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestApplicationDomains:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: EventPortal) -> None:
        application_domain = client.api.v2.architecture.application_domains.create(
            name="My First Application Domain",
        )
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: EventPortal) -> None:
        application_domain = client.api.v2.architecture.application_domains.create(
            name="My First Application Domain",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            deletion_protected=False,
            description="Application Domain created by the Solace PubSub+ Cloud API documentation",
            non_draft_descriptions_editable=False,
            topic_domain_enforcement_enabled=False,
            type="type",
            unique_topic_address_enforcement_enabled=False,
        )
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_domains.with_raw_response.create(
            name="My First Application Domain",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_domain = response.parse()
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_domains.with_streaming_response.create(
            name="My First Application Domain",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_domain = response.parse()
            assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        application_domain = client.api.v2.architecture.application_domains.retrieve(
            id="id",
        )
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: EventPortal) -> None:
        application_domain = client.api.v2.architecture.application_domains.retrieve(
            id="id",
            include=["string"],
        )
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_domains.with_raw_response.retrieve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_domain = response.parse()
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_domains.with_streaming_response.retrieve(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_domain = response.parse()
            assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.application_domains.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: EventPortal) -> None:
        application_domain = client.api.v2.architecture.application_domains.update(
            id="id",
            name="My First Application Domain",
        )
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: EventPortal) -> None:
        application_domain = client.api.v2.architecture.application_domains.update(
            id="id",
            name="My First Application Domain",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            deletion_protected=False,
            description="Application Domain created by the Solace PubSub+ Cloud API documentation",
            non_draft_descriptions_editable=False,
            topic_domain_enforcement_enabled=False,
            type="type",
            unique_topic_address_enforcement_enabled=False,
        )
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_domains.with_raw_response.update(
            id="id",
            name="My First Application Domain",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_domain = response.parse()
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_domains.with_streaming_response.update(
            id="id",
            name="My First Application Domain",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_domain = response.parse()
            assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.application_domains.with_raw_response.update(
                id="",
                name="My First Application Domain",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        application_domain = client.api.v2.architecture.application_domains.list()
        assert_matches_type(ApplicationDomainListResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        application_domain = client.api.v2.architecture.application_domains.list(
            ids=["string"],
            include=["string"],
            name="name",
            page_number=1,
            page_size=1,
        )
        assert_matches_type(ApplicationDomainListResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_domains.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_domain = response.parse()
        assert_matches_type(ApplicationDomainListResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_domains.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_domain = response.parse()
            assert_matches_type(ApplicationDomainListResponse, application_domain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: EventPortal) -> None:
        application_domain = client.api.v2.architecture.application_domains.delete(
            "id",
        )
        assert application_domain is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_domains.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_domain = response.parse()
        assert application_domain is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_domains.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_domain = response.parse()
            assert application_domain is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.api.v2.architecture.application_domains.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_method_export(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/applicationDomains/export/[object Object]").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        application_domain = client.api.v2.architecture.application_domains.export(
            {},
        )
        assert application_domain.is_closed
        assert application_domain.json() == {"foo": "bar"}
        assert cast(Any, application_domain.is_closed) is True
        assert isinstance(application_domain, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_raw_response_export(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/applicationDomains/export/[object Object]").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        application_domain = client.api.v2.architecture.application_domains.with_raw_response.export(
            {},
        )

        assert application_domain.is_closed is True
        assert application_domain.http_request.headers.get("X-Stainless-Lang") == "python"
        assert application_domain.json() == {"foo": "bar"}
        assert isinstance(application_domain, BinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    def test_streaming_response_export(self, client: EventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/applicationDomains/export/[object Object]").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        with client.api.v2.architecture.application_domains.with_streaming_response.export(
            {},
        ) as application_domain:
            assert not application_domain.is_closed
            assert application_domain.http_request.headers.get("X-Stainless-Lang") == "python"

            assert application_domain.json() == {"foo": "bar"}
            assert cast(Any, application_domain.is_closed) is True
            assert isinstance(application_domain, StreamedBinaryAPIResponse)

        assert cast(Any, application_domain.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_import(self, client: EventPortal) -> None:
        application_domain = client.api.v2.architecture.application_domains.import_()
        assert application_domain is None

    @pytest.mark.skip()
    @parametrize
    def test_method_import_with_all_params(self, client: EventPortal) -> None:
        application_domain = client.api.v2.architecture.application_domains.import_(
            address_spaces=[
                {
                    "broker_type": "kafka",
                    "delimiter": "_",
                }
            ],
            application_domains=[
                {
                    "name": "My First Application Domain",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "deletion_protected": False,
                    "description": "Application Domain created by the Solace PubSub+ Cloud API documentation",
                    "non_draft_descriptions_editable": False,
                    "topic_domain_enforcement_enabled": False,
                    "type": "type",
                    "unique_topic_address_enforcement_enabled": False,
                }
            ],
            applications=[
                {
                    "application_domain_id": "acb2j5k3mly",
                    "application_type": "standard",
                    "broker_type": "solace",
                    "name": "My First Application",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "type": "type",
                }
            ],
            application_versions=[
                {
                    "application_id": "acb2j5k3mly",
                    "version": "1.0.0",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "declared_consumed_event_version_ids": ['["5h2km5khkj","h5mk26hkm2"]'],
                    "declared_event_api_product_version_ids": ['["5h2km5khkj","h5mk26hkm2"]'],
                    "declared_produced_event_version_ids": ['["5h2km5khkj","h5mk26hkm2"]'],
                    "description": "Application created by Solace PubSub+ Cloud documentation",
                    "display_name": "Display name for the version",
                    "end_of_life_date": "2021-12-31T20:30:57.920Z",
                    "type": "type",
                    "validation_messages": {
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
                }
            ],
            custom_attribute_definitions=[
                {
                    "scope": "organization",
                    "id": "id",
                    "application_domain_id": "applicationDomainId",
                    "associated_entities": [
                        {
                            "application_domain_ids": ["string"],
                            "entity_type": "entityType",
                        }
                    ],
                    "associated_entity_types": ['["event","application"]'],
                    "name": "colour",
                    "type": "type",
                    "validation_messages": {
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
                    "value_type": "STRING",
                }
            ],
            enums=[
                {
                    "application_domain_id": "12345678",
                    "name": "My First Enum",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "shared": False,
                }
            ],
            enum_versions=[
                {
                    "enum_id": "xyz23mwec2g",
                    "values": [
                        {
                            "value": "Ontario",
                            "enum_version_id": "xyz23mwec2g",
                            "label": "Display name for the value",
                        }
                    ],
                    "version": "1.0.0",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "description": "Enum created by Solace PubSub+ Cloud API documentation",
                    "display_name": "Display name for the version",
                    "end_of_life_date": "2021-12-31T20:30:57.920Z",
                }
            ],
            event_api_products=[
                {
                    "application_domain_id": "abcappdomainid",
                    "broker_type": "kafka",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "name": "EventApiProductTest",
                    "shared": True,
                }
            ],
            event_api_product_versions=[
                {
                    "event_api_product_id": "acb2j5k3mly",
                    "approval_type": "automatic",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "description": "Event API product created by Solace PubSub+ Cloud documentation",
                    "display_name": "Event API product version display name",
                    "end_of_life_date": "2021-12-31T20:30:57.920Z",
                    "event_api_product_registrations": [
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
                    "event_api_version_ids": ["string"],
                    "filters": [
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
                    "plans": [
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
                    "publish_state": "unset",
                    "solace_messaging_services": [
                        {
                            "solace_cloud_messaging_service_id": "service123",
                            "supported_protocols": ["string"],
                        }
                    ],
                    "state_id": "1",
                    "summary": "Summary string value of event API product version",
                    "version": "1.0.0",
                }
            ],
            event_apis=[
                {
                    "application_domain_id": "acb2j5k3mly",
                    "broker_type": "kafka",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "name": "Apitest",
                    "shared": True,
                }
            ],
            event_api_versions=[
                {
                    "event_api_id": "acb2j5k3mly",
                    "consumed_event_version_ids": ['["5h2km5khkj","h5mk26hkm2"]'],
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "declared_event_api_product_version_ids": ['["5h2km5khkj","h5mk26hkm2"]'],
                    "description": "Event Api created by Solace PubSub+ Cloud documentation",
                    "display_name": "Display name for the eventApi version",
                    "produced_event_version_ids": ['["5h2km5khkj","h5mk26hkm2"]'],
                    "state_id": "1",
                    "type": "type",
                    "version": "1.0.0",
                }
            ],
            events=[
                {
                    "application_domain_id": "acb2j5k3mly",
                    "name": "My First Event",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "requires_approval": False,
                    "shared": False,
                }
            ],
            event_versions=[
                {
                    "event_id": "acb2j5k3mly",
                    "version": "1.0.0",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "delivery_descriptor": {
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
                    "description": "Event version created by Solace PubSub+ Cloud documentation",
                    "display_name": "Display name for the version",
                    "end_of_life_date": "2021-12-31T20:30:57.920Z",
                    "schema_primitive_type": "BYTES",
                    "schema_version_id": "shb3mlyec2g",
                    "type": "type",
                    "validation_messages": {
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
                }
            ],
            format_version="formatVersion",
            schemas=[
                {
                    "application_domain_id": "12345678",
                    "name": "My First Schema",
                    "schema_type": "jsonSchema",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "shared": False,
                }
            ],
            schema_versions=[
                {
                    "schema_id": "12345678",
                    "version": "1.0.0",
                    "content": '{ "$schema": "http://json-schema.org/draft-07/schema#", "$id": "http://example.com/root.json","type": "object", "title": "An example schema", "required": [ "attribute", ], "properties": { "attribute": { "$id": "#/properties/attribute", "type": "string", "title": "An example of a string based attribute", "examples": [ "aValue" ], "pattern": "^(.*)$" } }}',
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "description": "Schema created by Solace PubSub+ Cloud API documentation",
                    "display_name": "Display name for the version",
                    "end_of_life_date": "2021-12-31T20:30:57.920Z",
                    "schema_version_references": [{"schema_version_id": "schemaVersionId"}],
                }
            ],
            topic_domains=[
                {
                    "address_levels": [
                        {
                            "address_level_type": "literal",
                            "name": "root",
                            "enum_version_id": "enumVersionId",
                        }
                    ],
                    "application_domain_id": "acb2j5k3mly",
                    "broker_type": "solace",
                }
            ],
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
        assert application_domain is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_import(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.application_domains.with_raw_response.import_()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_domain = response.parse()
        assert application_domain is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_import(self, client: EventPortal) -> None:
        with client.api.v2.architecture.application_domains.with_streaming_response.import_() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_domain = response.parse()
            assert application_domain is None

        assert cast(Any, response.is_closed) is True


class TestAsyncApplicationDomains:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        application_domain = await async_client.api.v2.architecture.application_domains.create(
            name="My First Application Domain",
        )
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEventPortal) -> None:
        application_domain = await async_client.api.v2.architecture.application_domains.create(
            name="My First Application Domain",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            deletion_protected=False,
            description="Application Domain created by the Solace PubSub+ Cloud API documentation",
            non_draft_descriptions_editable=False,
            topic_domain_enforcement_enabled=False,
            type="type",
            unique_topic_address_enforcement_enabled=False,
        )
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_domains.with_raw_response.create(
            name="My First Application Domain",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_domain = await response.parse()
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_domains.with_streaming_response.create(
            name="My First Application Domain",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_domain = await response.parse()
            assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        application_domain = await async_client.api.v2.architecture.application_domains.retrieve(
            id="id",
        )
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncEventPortal) -> None:
        application_domain = await async_client.api.v2.architecture.application_domains.retrieve(
            id="id",
            include=["string"],
        )
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_domains.with_raw_response.retrieve(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_domain = await response.parse()
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_domains.with_streaming_response.retrieve(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_domain = await response.parse()
            assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.application_domains.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncEventPortal) -> None:
        application_domain = await async_client.api.v2.architecture.application_domains.update(
            id="id",
            name="My First Application Domain",
        )
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEventPortal) -> None:
        application_domain = await async_client.api.v2.architecture.application_domains.update(
            id="id",
            name="My First Application Domain",
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            deletion_protected=False,
            description="Application Domain created by the Solace PubSub+ Cloud API documentation",
            non_draft_descriptions_editable=False,
            topic_domain_enforcement_enabled=False,
            type="type",
            unique_topic_address_enforcement_enabled=False,
        )
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_domains.with_raw_response.update(
            id="id",
            name="My First Application Domain",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_domain = await response.parse()
        assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_domains.with_streaming_response.update(
            id="id",
            name="My First Application Domain",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_domain = await response.parse()
            assert_matches_type(ApplicationDomainResponse, application_domain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.application_domains.with_raw_response.update(
                id="",
                name="My First Application Domain",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        application_domain = await async_client.api.v2.architecture.application_domains.list()
        assert_matches_type(ApplicationDomainListResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        application_domain = await async_client.api.v2.architecture.application_domains.list(
            ids=["string"],
            include=["string"],
            name="name",
            page_number=1,
            page_size=1,
        )
        assert_matches_type(ApplicationDomainListResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_domains.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_domain = await response.parse()
        assert_matches_type(ApplicationDomainListResponse, application_domain, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_domains.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_domain = await response.parse()
            assert_matches_type(ApplicationDomainListResponse, application_domain, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncEventPortal) -> None:
        application_domain = await async_client.api.v2.architecture.application_domains.delete(
            "id",
        )
        assert application_domain is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_domains.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_domain = await response.parse()
        assert application_domain is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_domains.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_domain = await response.parse()
            assert application_domain is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.api.v2.architecture.application_domains.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_method_export(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/applicationDomains/export/[object Object]").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        application_domain = await async_client.api.v2.architecture.application_domains.export(
            {},
        )
        assert application_domain.is_closed
        assert await application_domain.json() == {"foo": "bar"}
        assert cast(Any, application_domain.is_closed) is True
        assert isinstance(application_domain, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_raw_response_export(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/applicationDomains/export/[object Object]").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )

        application_domain = await async_client.api.v2.architecture.application_domains.with_raw_response.export(
            {},
        )

        assert application_domain.is_closed is True
        assert application_domain.http_request.headers.get("X-Stainless-Lang") == "python"
        assert await application_domain.json() == {"foo": "bar"}
        assert isinstance(application_domain, AsyncBinaryAPIResponse)

    @pytest.mark.skip()
    @parametrize
    @pytest.mark.respx(base_url=base_url)
    async def test_streaming_response_export(self, async_client: AsyncEventPortal, respx_mock: MockRouter) -> None:
        respx_mock.get("/api/v2/architecture/applicationDomains/export/[object Object]").mock(
            return_value=httpx.Response(200, json={"foo": "bar"})
        )
        async with async_client.api.v2.architecture.application_domains.with_streaming_response.export(
            {},
        ) as application_domain:
            assert not application_domain.is_closed
            assert application_domain.http_request.headers.get("X-Stainless-Lang") == "python"

            assert await application_domain.json() == {"foo": "bar"}
            assert cast(Any, application_domain.is_closed) is True
            assert isinstance(application_domain, AsyncStreamedBinaryAPIResponse)

        assert cast(Any, application_domain.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_import(self, async_client: AsyncEventPortal) -> None:
        application_domain = await async_client.api.v2.architecture.application_domains.import_()
        assert application_domain is None

    @pytest.mark.skip()
    @parametrize
    async def test_method_import_with_all_params(self, async_client: AsyncEventPortal) -> None:
        application_domain = await async_client.api.v2.architecture.application_domains.import_(
            address_spaces=[
                {
                    "broker_type": "kafka",
                    "delimiter": "_",
                }
            ],
            application_domains=[
                {
                    "name": "My First Application Domain",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "deletion_protected": False,
                    "description": "Application Domain created by the Solace PubSub+ Cloud API documentation",
                    "non_draft_descriptions_editable": False,
                    "topic_domain_enforcement_enabled": False,
                    "type": "type",
                    "unique_topic_address_enforcement_enabled": False,
                }
            ],
            applications=[
                {
                    "application_domain_id": "acb2j5k3mly",
                    "application_type": "standard",
                    "broker_type": "solace",
                    "name": "My First Application",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "type": "type",
                }
            ],
            application_versions=[
                {
                    "application_id": "acb2j5k3mly",
                    "version": "1.0.0",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "declared_consumed_event_version_ids": ['["5h2km5khkj","h5mk26hkm2"]'],
                    "declared_event_api_product_version_ids": ['["5h2km5khkj","h5mk26hkm2"]'],
                    "declared_produced_event_version_ids": ['["5h2km5khkj","h5mk26hkm2"]'],
                    "description": "Application created by Solace PubSub+ Cloud documentation",
                    "display_name": "Display name for the version",
                    "end_of_life_date": "2021-12-31T20:30:57.920Z",
                    "type": "type",
                    "validation_messages": {
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
                }
            ],
            custom_attribute_definitions=[
                {
                    "scope": "organization",
                    "id": "id",
                    "application_domain_id": "applicationDomainId",
                    "associated_entities": [
                        {
                            "application_domain_ids": ["string"],
                            "entity_type": "entityType",
                        }
                    ],
                    "associated_entity_types": ['["event","application"]'],
                    "name": "colour",
                    "type": "type",
                    "validation_messages": {
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
                    "value_type": "STRING",
                }
            ],
            enums=[
                {
                    "application_domain_id": "12345678",
                    "name": "My First Enum",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "shared": False,
                }
            ],
            enum_versions=[
                {
                    "enum_id": "xyz23mwec2g",
                    "values": [
                        {
                            "value": "Ontario",
                            "enum_version_id": "xyz23mwec2g",
                            "label": "Display name for the value",
                        }
                    ],
                    "version": "1.0.0",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "description": "Enum created by Solace PubSub+ Cloud API documentation",
                    "display_name": "Display name for the version",
                    "end_of_life_date": "2021-12-31T20:30:57.920Z",
                }
            ],
            event_api_products=[
                {
                    "application_domain_id": "abcappdomainid",
                    "broker_type": "kafka",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "name": "EventApiProductTest",
                    "shared": True,
                }
            ],
            event_api_product_versions=[
                {
                    "event_api_product_id": "acb2j5k3mly",
                    "approval_type": "automatic",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "description": "Event API product created by Solace PubSub+ Cloud documentation",
                    "display_name": "Event API product version display name",
                    "end_of_life_date": "2021-12-31T20:30:57.920Z",
                    "event_api_product_registrations": [
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
                    "event_api_version_ids": ["string"],
                    "filters": [
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
                    "plans": [
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
                    "publish_state": "unset",
                    "solace_messaging_services": [
                        {
                            "solace_cloud_messaging_service_id": "service123",
                            "supported_protocols": ["string"],
                        }
                    ],
                    "state_id": "1",
                    "summary": "Summary string value of event API product version",
                    "version": "1.0.0",
                }
            ],
            event_apis=[
                {
                    "application_domain_id": "acb2j5k3mly",
                    "broker_type": "kafka",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "name": "Apitest",
                    "shared": True,
                }
            ],
            event_api_versions=[
                {
                    "event_api_id": "acb2j5k3mly",
                    "consumed_event_version_ids": ['["5h2km5khkj","h5mk26hkm2"]'],
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "declared_event_api_product_version_ids": ['["5h2km5khkj","h5mk26hkm2"]'],
                    "description": "Event Api created by Solace PubSub+ Cloud documentation",
                    "display_name": "Display name for the eventApi version",
                    "produced_event_version_ids": ['["5h2km5khkj","h5mk26hkm2"]'],
                    "state_id": "1",
                    "type": "type",
                    "version": "1.0.0",
                }
            ],
            events=[
                {
                    "application_domain_id": "acb2j5k3mly",
                    "name": "My First Event",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "requires_approval": False,
                    "shared": False,
                }
            ],
            event_versions=[
                {
                    "event_id": "acb2j5k3mly",
                    "version": "1.0.0",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "delivery_descriptor": {
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
                    "description": "Event version created by Solace PubSub+ Cloud documentation",
                    "display_name": "Display name for the version",
                    "end_of_life_date": "2021-12-31T20:30:57.920Z",
                    "schema_primitive_type": "BYTES",
                    "schema_version_id": "shb3mlyec2g",
                    "type": "type",
                    "validation_messages": {
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
                }
            ],
            format_version="formatVersion",
            schemas=[
                {
                    "application_domain_id": "12345678",
                    "name": "My First Schema",
                    "schema_type": "jsonSchema",
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "shared": False,
                }
            ],
            schema_versions=[
                {
                    "schema_id": "12345678",
                    "version": "1.0.0",
                    "content": '{ "$schema": "http://json-schema.org/draft-07/schema#", "$id": "http://example.com/root.json","type": "object", "title": "An example schema", "required": [ "attribute", ], "properties": { "attribute": { "$id": "#/properties/attribute", "type": "string", "title": "An example of a string based attribute", "examples": [ "aValue" ], "pattern": "^(.*)$" } }}',
                    "custom_attributes": [
                        {
                            "custom_attribute_definition_id": "acb2j5k3mly",
                            "custom_attribute_definition_name": "color",
                            "string_values": "red",
                            "value": "red",
                        }
                    ],
                    "description": "Schema created by Solace PubSub+ Cloud API documentation",
                    "display_name": "Display name for the version",
                    "end_of_life_date": "2021-12-31T20:30:57.920Z",
                    "schema_version_references": [{"schema_version_id": "schemaVersionId"}],
                }
            ],
            topic_domains=[
                {
                    "address_levels": [
                        {
                            "address_level_type": "literal",
                            "name": "root",
                            "enum_version_id": "enumVersionId",
                        }
                    ],
                    "application_domain_id": "acb2j5k3mly",
                    "broker_type": "solace",
                }
            ],
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
        assert application_domain is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_import(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.application_domains.with_raw_response.import_()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        application_domain = await response.parse()
        assert application_domain is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_import(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.application_domains.with_streaming_response.import_() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            application_domain = await response.parse()
            assert application_domain is None

        assert cast(Any, response.is_closed) is True
