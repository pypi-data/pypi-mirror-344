# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from event_portal import EventPortal, AsyncEventPortal
from event_portal.types.api.v2.architecture import (
    EventAPIVersionResponse,
    StateChangeRequestResponse,
    EventAPIVersionListResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestEventAPIVersions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: EventPortal) -> None:
        event_api_version = client.api.v2.architecture.event_api_versions.create(
            event_api_id="acb2j5k3mly",
        )
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: EventPortal) -> None:
        event_api_version = client.api.v2.architecture.event_api_versions.create(
            event_api_id="acb2j5k3mly",
            consumed_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            declared_event_api_product_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            description="Event Api created by Solace PubSub+ Cloud documentation",
            display_name="Display name for the eventApi version",
            produced_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            state_id="1",
            type="type",
            version="1.0.0",
        )
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_versions.with_raw_response.create(
            event_api_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_version = response.parse()
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_versions.with_streaming_response.create(
            event_api_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_version = response.parse()
            assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: EventPortal) -> None:
        event_api_version = client.api.v2.architecture.event_api_versions.retrieve(
            version_id="versionId",
        )
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: EventPortal) -> None:
        event_api_version = client.api.v2.architecture.event_api_versions.retrieve(
            version_id="versionId",
            include="include",
        )
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_versions.with_raw_response.retrieve(
            version_id="versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_version = response.parse()
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_versions.with_streaming_response.retrieve(
            version_id="versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_version = response.parse()
            assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.api.v2.architecture.event_api_versions.with_raw_response.retrieve(
                version_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: EventPortal) -> None:
        event_api_version = client.api.v2.architecture.event_api_versions.update(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
        )
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: EventPortal) -> None:
        event_api_version = client.api.v2.architecture.event_api_versions.update(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
            consumed_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            declared_event_api_product_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            description="Event Api created by Solace PubSub+ Cloud documentation",
            display_name="Display name for the eventApi version",
            produced_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            state_id="1",
            type="type",
            version="1.0.0",
        )
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_versions.with_raw_response.update(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_version = response.parse()
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_versions.with_streaming_response.update(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_version = response.parse()
            assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.api.v2.architecture.event_api_versions.with_raw_response.update(
                version_id="",
                event_api_id="acb2j5k3mly",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: EventPortal) -> None:
        event_api_version = client.api.v2.architecture.event_api_versions.list()
        assert_matches_type(EventAPIVersionListResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: EventPortal) -> None:
        event_api_version = client.api.v2.architecture.event_api_versions.list(
            custom_attributes="customAttributes",
            event_api_ids=["string"],
            ids=["string"],
            include="include",
            page_number=1,
            page_size=1,
            state_id="stateId",
        )
        assert_matches_type(EventAPIVersionListResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_versions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_version = response.parse()
        assert_matches_type(EventAPIVersionListResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_versions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_version = response.parse()
            assert_matches_type(EventAPIVersionListResponse, event_api_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: EventPortal) -> None:
        event_api_version = client.api.v2.architecture.event_api_versions.delete(
            "versionId",
        )
        assert event_api_version is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_versions.with_raw_response.delete(
            "versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_version = response.parse()
        assert event_api_version is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_versions.with_streaming_response.delete(
            "versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_version = response.parse()
            assert event_api_version is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.api.v2.architecture.event_api_versions.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_get_async_api(self, client: EventPortal) -> None:
        event_api_version = client.api.v2.architecture.event_api_versions.get_async_api(
            event_api_version_id="eventApiVersionId",
        )
        assert_matches_type(str, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_get_async_api_with_all_params(self, client: EventPortal) -> None:
        event_api_version = client.api.v2.architecture.event_api_versions.get_async_api(
            event_api_version_id="eventApiVersionId",
            async_api_version="2.0.0",
            event_api_product_version_id="eventApiProductVersionId",
            format="json",
            gateway_messaging_service_ids=["string"],
            included_extensions="all",
            plan_id="planId",
            show_versioning=True,
        )
        assert_matches_type(str, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_get_async_api(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_versions.with_raw_response.get_async_api(
            event_api_version_id="eventApiVersionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_version = response.parse()
        assert_matches_type(str, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_get_async_api(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_versions.with_streaming_response.get_async_api(
            event_api_version_id="eventApiVersionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_version = response.parse()
            assert_matches_type(str, event_api_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_get_async_api(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `event_api_version_id` but received ''"):
            client.api.v2.architecture.event_api_versions.with_raw_response.get_async_api(
                event_api_version_id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update_state(self, client: EventPortal) -> None:
        event_api_version = client.api.v2.architecture.event_api_versions.update_state(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
        )
        assert_matches_type(StateChangeRequestResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_state_with_all_params(self, client: EventPortal) -> None:
        event_api_version = client.api.v2.architecture.event_api_versions.update_state(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
            consumed_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            declared_event_api_product_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            description="Event Api created by Solace PubSub+ Cloud documentation",
            display_name="Display name for the eventApi version",
            produced_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            state_id="1",
            type="type",
            version="1.0.0",
        )
        assert_matches_type(StateChangeRequestResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update_state(self, client: EventPortal) -> None:
        response = client.api.v2.architecture.event_api_versions.with_raw_response.update_state(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_version = response.parse()
        assert_matches_type(StateChangeRequestResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update_state(self, client: EventPortal) -> None:
        with client.api.v2.architecture.event_api_versions.with_streaming_response.update_state(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_version = response.parse()
            assert_matches_type(StateChangeRequestResponse, event_api_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update_state(self, client: EventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            client.api.v2.architecture.event_api_versions.with_raw_response.update_state(
                version_id="",
                event_api_id="acb2j5k3mly",
            )


class TestAsyncEventAPIVersions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncEventPortal) -> None:
        event_api_version = await async_client.api.v2.architecture.event_api_versions.create(
            event_api_id="acb2j5k3mly",
        )
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_api_version = await async_client.api.v2.architecture.event_api_versions.create(
            event_api_id="acb2j5k3mly",
            consumed_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            declared_event_api_product_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            description="Event Api created by Solace PubSub+ Cloud documentation",
            display_name="Display name for the eventApi version",
            produced_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            state_id="1",
            type="type",
            version="1.0.0",
        )
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_versions.with_raw_response.create(
            event_api_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_version = await response.parse()
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_api_versions.with_streaming_response.create(
            event_api_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_version = await response.parse()
            assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncEventPortal) -> None:
        event_api_version = await async_client.api.v2.architecture.event_api_versions.retrieve(
            version_id="versionId",
        )
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_api_version = await async_client.api.v2.architecture.event_api_versions.retrieve(
            version_id="versionId",
            include="include",
        )
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_versions.with_raw_response.retrieve(
            version_id="versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_version = await response.parse()
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_api_versions.with_streaming_response.retrieve(
            version_id="versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_version = await response.parse()
            assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.api.v2.architecture.event_api_versions.with_raw_response.retrieve(
                version_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncEventPortal) -> None:
        event_api_version = await async_client.api.v2.architecture.event_api_versions.update(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
        )
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_api_version = await async_client.api.v2.architecture.event_api_versions.update(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
            consumed_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            declared_event_api_product_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            description="Event Api created by Solace PubSub+ Cloud documentation",
            display_name="Display name for the eventApi version",
            produced_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            state_id="1",
            type="type",
            version="1.0.0",
        )
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_versions.with_raw_response.update(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_version = await response.parse()
        assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_api_versions.with_streaming_response.update(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_version = await response.parse()
            assert_matches_type(EventAPIVersionResponse, event_api_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.api.v2.architecture.event_api_versions.with_raw_response.update(
                version_id="",
                event_api_id="acb2j5k3mly",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncEventPortal) -> None:
        event_api_version = await async_client.api.v2.architecture.event_api_versions.list()
        assert_matches_type(EventAPIVersionListResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_api_version = await async_client.api.v2.architecture.event_api_versions.list(
            custom_attributes="customAttributes",
            event_api_ids=["string"],
            ids=["string"],
            include="include",
            page_number=1,
            page_size=1,
            state_id="stateId",
        )
        assert_matches_type(EventAPIVersionListResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_versions.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_version = await response.parse()
        assert_matches_type(EventAPIVersionListResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_api_versions.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_version = await response.parse()
            assert_matches_type(EventAPIVersionListResponse, event_api_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncEventPortal) -> None:
        event_api_version = await async_client.api.v2.architecture.event_api_versions.delete(
            "versionId",
        )
        assert event_api_version is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_versions.with_raw_response.delete(
            "versionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_version = await response.parse()
        assert event_api_version is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_api_versions.with_streaming_response.delete(
            "versionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_version = await response.parse()
            assert event_api_version is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.api.v2.architecture.event_api_versions.with_raw_response.delete(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_async_api(self, async_client: AsyncEventPortal) -> None:
        event_api_version = await async_client.api.v2.architecture.event_api_versions.get_async_api(
            event_api_version_id="eventApiVersionId",
        )
        assert_matches_type(str, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_get_async_api_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_api_version = await async_client.api.v2.architecture.event_api_versions.get_async_api(
            event_api_version_id="eventApiVersionId",
            async_api_version="2.0.0",
            event_api_product_version_id="eventApiProductVersionId",
            format="json",
            gateway_messaging_service_ids=["string"],
            included_extensions="all",
            plan_id="planId",
            show_versioning=True,
        )
        assert_matches_type(str, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_get_async_api(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_versions.with_raw_response.get_async_api(
            event_api_version_id="eventApiVersionId",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_version = await response.parse()
        assert_matches_type(str, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_get_async_api(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_api_versions.with_streaming_response.get_async_api(
            event_api_version_id="eventApiVersionId",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_version = await response.parse()
            assert_matches_type(str, event_api_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_get_async_api(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `event_api_version_id` but received ''"):
            await async_client.api.v2.architecture.event_api_versions.with_raw_response.get_async_api(
                event_api_version_id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_state(self, async_client: AsyncEventPortal) -> None:
        event_api_version = await async_client.api.v2.architecture.event_api_versions.update_state(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
        )
        assert_matches_type(StateChangeRequestResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_state_with_all_params(self, async_client: AsyncEventPortal) -> None:
        event_api_version = await async_client.api.v2.architecture.event_api_versions.update_state(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
            consumed_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            custom_attributes=[
                {
                    "custom_attribute_definition_id": "acb2j5k3mly",
                    "custom_attribute_definition_name": "color",
                    "string_values": "red",
                    "value": "red",
                }
            ],
            declared_event_api_product_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            description="Event Api created by Solace PubSub+ Cloud documentation",
            display_name="Display name for the eventApi version",
            produced_event_version_ids=['["5h2km5khkj","h5mk26hkm2"]'],
            state_id="1",
            type="type",
            version="1.0.0",
        )
        assert_matches_type(StateChangeRequestResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update_state(self, async_client: AsyncEventPortal) -> None:
        response = await async_client.api.v2.architecture.event_api_versions.with_raw_response.update_state(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        event_api_version = await response.parse()
        assert_matches_type(StateChangeRequestResponse, event_api_version, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update_state(self, async_client: AsyncEventPortal) -> None:
        async with async_client.api.v2.architecture.event_api_versions.with_streaming_response.update_state(
            version_id="versionId",
            event_api_id="acb2j5k3mly",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            event_api_version = await response.parse()
            assert_matches_type(StateChangeRequestResponse, event_api_version, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update_state(self, async_client: AsyncEventPortal) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `version_id` but received ''"):
            await async_client.api.v2.architecture.event_api_versions.with_raw_response.update_state(
                version_id="",
                event_api_id="acb2j5k3mly",
            )
