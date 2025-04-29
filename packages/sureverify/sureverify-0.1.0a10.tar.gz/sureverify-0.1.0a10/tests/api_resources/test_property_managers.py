# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sureverify import Verify, AsyncVerify
from tests.utils import assert_matches_type
from sureverify.types import (
    PropertyManager,
    PropertyManagerResponse,
)
from sureverify.pagination import SyncCursorPagination, AsyncCursorPagination

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPropertyManagers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Verify) -> None:
        property_manager = client.property_managers.create(
            data={
                "attributes": {"name": "x"},
                "type": "PropertyManager",
            },
        )
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Verify) -> None:
        property_manager = client.property_managers.create(
            data={
                "attributes": {
                    "name": "x",
                    "admin_review_required": True,
                    "admin_review_required_only_for_non_compliant": True,
                    "allow_invalid_address": True,
                    "allow_new_policies_from_carriers": True,
                    "allow_new_residents": True,
                    "allow_new_units": True,
                    "allow_overriding": True,
                    "allow_partial_name_and_unit_match": True,
                    "contact_email_address": "dev@stainless.com",
                    "contact_name": "contact_name",
                    "contact_phone_number": "contact_phone_number",
                    "force_admin_review_if_overridden": True,
                    "force_coverage_term_to_overlap_with_lease": True,
                    "force_extra_confirmation_on_verification_submission": True,
                    "interest_name": "interest_name",
                    "is_active": True,
                    "notes": "notes",
                    "send_email_when_becoming_non_compliant": True,
                    "send_email_when_case_compliant": True,
                    "send_email_when_case_incomplete": True,
                    "send_email_when_case_non_compliant": True,
                    "send_email_when_case_submitted": True,
                    "send_email_when_compliance_is_expiring_soon": True,
                    "send_email_when_new_policy_is_added": True,
                    "send_email_when_no_verification_started": True,
                    "send_email_when_policy_updated": True,
                },
                "type": "PropertyManager",
                "relationships": {
                    "contact_address": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Address",
                        }
                    }
                },
            },
        )
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Verify) -> None:
        response = client.property_managers.with_raw_response.create(
            data={
                "attributes": {"name": "x"},
                "type": "PropertyManager",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        property_manager = response.parse()
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Verify) -> None:
        with client.property_managers.with_streaming_response.create(
            data={
                "attributes": {"name": "x"},
                "type": "PropertyManager",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            property_manager = response.parse()
            assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Verify) -> None:
        property_manager = client.property_managers.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Verify) -> None:
        property_manager = client.property_managers.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_property_manager=["name"],
            include=["interest_mailbox"],
        )
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Verify) -> None:
        response = client.property_managers.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        property_manager = response.parse()
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Verify) -> None:
        with client.property_managers.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            property_manager = response.parse()
            assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.property_managers.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: Verify) -> None:
        property_manager = client.property_managers.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {"name": "x"},
                "type": "PropertyManager",
            },
        )
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: Verify) -> None:
        property_manager = client.property_managers.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {
                    "name": "x",
                    "admin_review_required": True,
                    "admin_review_required_only_for_non_compliant": True,
                    "allow_invalid_address": True,
                    "allow_new_policies_from_carriers": True,
                    "allow_new_residents": True,
                    "allow_new_units": True,
                    "allow_overriding": True,
                    "allow_partial_name_and_unit_match": True,
                    "contact_email_address": "dev@stainless.com",
                    "contact_name": "contact_name",
                    "contact_phone_number": "contact_phone_number",
                    "force_admin_review_if_overridden": True,
                    "force_coverage_term_to_overlap_with_lease": True,
                    "force_extra_confirmation_on_verification_submission": True,
                    "interest_name": "interest_name",
                    "is_active": True,
                    "notes": "notes",
                    "send_email_when_becoming_non_compliant": True,
                    "send_email_when_case_compliant": True,
                    "send_email_when_case_incomplete": True,
                    "send_email_when_case_non_compliant": True,
                    "send_email_when_case_submitted": True,
                    "send_email_when_compliance_is_expiring_soon": True,
                    "send_email_when_new_policy_is_added": True,
                    "send_email_when_no_verification_started": True,
                    "send_email_when_policy_updated": True,
                },
                "type": "PropertyManager",
                "relationships": {
                    "contact_address": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Address",
                        }
                    }
                },
            },
        )
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: Verify) -> None:
        response = client.property_managers.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {"name": "x"},
                "type": "PropertyManager",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        property_manager = response.parse()
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: Verify) -> None:
        with client.property_managers.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {"name": "x"},
                "type": "PropertyManager",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            property_manager = response.parse()
            assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.property_managers.with_raw_response.update(
                id="",
                data={
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "attributes": {"name": "x"},
                    "type": "PropertyManager",
                },
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Verify) -> None:
        property_manager = client.property_managers.list()
        assert_matches_type(SyncCursorPagination[PropertyManager], property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Verify) -> None:
        property_manager = client.property_managers.list(
            fields_property_manager=["name"],
            include=["interest_mailbox"],
            page_cursor="page[cursor]",
            page_size=0,
        )
        assert_matches_type(SyncCursorPagination[PropertyManager], property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Verify) -> None:
        response = client.property_managers.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        property_manager = response.parse()
        assert_matches_type(SyncCursorPagination[PropertyManager], property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Verify) -> None:
        with client.property_managers.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            property_manager = response.parse()
            assert_matches_type(SyncCursorPagination[PropertyManager], property_manager, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPropertyManagers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncVerify) -> None:
        property_manager = await async_client.property_managers.create(
            data={
                "attributes": {"name": "x"},
                "type": "PropertyManager",
            },
        )
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncVerify) -> None:
        property_manager = await async_client.property_managers.create(
            data={
                "attributes": {
                    "name": "x",
                    "admin_review_required": True,
                    "admin_review_required_only_for_non_compliant": True,
                    "allow_invalid_address": True,
                    "allow_new_policies_from_carriers": True,
                    "allow_new_residents": True,
                    "allow_new_units": True,
                    "allow_overriding": True,
                    "allow_partial_name_and_unit_match": True,
                    "contact_email_address": "dev@stainless.com",
                    "contact_name": "contact_name",
                    "contact_phone_number": "contact_phone_number",
                    "force_admin_review_if_overridden": True,
                    "force_coverage_term_to_overlap_with_lease": True,
                    "force_extra_confirmation_on_verification_submission": True,
                    "interest_name": "interest_name",
                    "is_active": True,
                    "notes": "notes",
                    "send_email_when_becoming_non_compliant": True,
                    "send_email_when_case_compliant": True,
                    "send_email_when_case_incomplete": True,
                    "send_email_when_case_non_compliant": True,
                    "send_email_when_case_submitted": True,
                    "send_email_when_compliance_is_expiring_soon": True,
                    "send_email_when_new_policy_is_added": True,
                    "send_email_when_no_verification_started": True,
                    "send_email_when_policy_updated": True,
                },
                "type": "PropertyManager",
                "relationships": {
                    "contact_address": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Address",
                        }
                    }
                },
            },
        )
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncVerify) -> None:
        response = await async_client.property_managers.with_raw_response.create(
            data={
                "attributes": {"name": "x"},
                "type": "PropertyManager",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        property_manager = await response.parse()
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncVerify) -> None:
        async with async_client.property_managers.with_streaming_response.create(
            data={
                "attributes": {"name": "x"},
                "type": "PropertyManager",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            property_manager = await response.parse()
            assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncVerify) -> None:
        property_manager = await async_client.property_managers.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncVerify) -> None:
        property_manager = await async_client.property_managers.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_property_manager=["name"],
            include=["interest_mailbox"],
        )
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncVerify) -> None:
        response = await async_client.property_managers.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        property_manager = await response.parse()
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncVerify) -> None:
        async with async_client.property_managers.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            property_manager = await response.parse()
            assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.property_managers.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncVerify) -> None:
        property_manager = await async_client.property_managers.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {"name": "x"},
                "type": "PropertyManager",
            },
        )
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncVerify) -> None:
        property_manager = await async_client.property_managers.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {
                    "name": "x",
                    "admin_review_required": True,
                    "admin_review_required_only_for_non_compliant": True,
                    "allow_invalid_address": True,
                    "allow_new_policies_from_carriers": True,
                    "allow_new_residents": True,
                    "allow_new_units": True,
                    "allow_overriding": True,
                    "allow_partial_name_and_unit_match": True,
                    "contact_email_address": "dev@stainless.com",
                    "contact_name": "contact_name",
                    "contact_phone_number": "contact_phone_number",
                    "force_admin_review_if_overridden": True,
                    "force_coverage_term_to_overlap_with_lease": True,
                    "force_extra_confirmation_on_verification_submission": True,
                    "interest_name": "interest_name",
                    "is_active": True,
                    "notes": "notes",
                    "send_email_when_becoming_non_compliant": True,
                    "send_email_when_case_compliant": True,
                    "send_email_when_case_incomplete": True,
                    "send_email_when_case_non_compliant": True,
                    "send_email_when_case_submitted": True,
                    "send_email_when_compliance_is_expiring_soon": True,
                    "send_email_when_new_policy_is_added": True,
                    "send_email_when_no_verification_started": True,
                    "send_email_when_policy_updated": True,
                },
                "type": "PropertyManager",
                "relationships": {
                    "contact_address": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Address",
                        }
                    }
                },
            },
        )
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncVerify) -> None:
        response = await async_client.property_managers.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {"name": "x"},
                "type": "PropertyManager",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        property_manager = await response.parse()
        assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncVerify) -> None:
        async with async_client.property_managers.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {"name": "x"},
                "type": "PropertyManager",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            property_manager = await response.parse()
            assert_matches_type(PropertyManagerResponse, property_manager, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.property_managers.with_raw_response.update(
                id="",
                data={
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "attributes": {"name": "x"},
                    "type": "PropertyManager",
                },
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncVerify) -> None:
        property_manager = await async_client.property_managers.list()
        assert_matches_type(AsyncCursorPagination[PropertyManager], property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncVerify) -> None:
        property_manager = await async_client.property_managers.list(
            fields_property_manager=["name"],
            include=["interest_mailbox"],
            page_cursor="page[cursor]",
            page_size=0,
        )
        assert_matches_type(AsyncCursorPagination[PropertyManager], property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncVerify) -> None:
        response = await async_client.property_managers.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        property_manager = await response.parse()
        assert_matches_type(AsyncCursorPagination[PropertyManager], property_manager, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncVerify) -> None:
        async with async_client.property_managers.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            property_manager = await response.parse()
            assert_matches_type(AsyncCursorPagination[PropertyManager], property_manager, path=["response"])

        assert cast(Any, response.is_closed) is True
