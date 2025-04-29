# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sureverify import Verify, AsyncVerify
from tests.utils import assert_matches_type
from sureverify.types import (
    Policy,
    PolicyResponse,
)
from sureverify._utils import parse_date
from sureverify.pagination import SyncCursorPagination, AsyncCursorPagination

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPolicies:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Verify) -> None:
        policy = client.policies.create(
            data={
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    }
                },
                "type": "Policy",
            },
        )
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Verify) -> None:
        policy = client.policies.create(
            data={
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    },
                    "interested_party_address": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Address",
                        }
                    },
                    "lease_address": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Address",
                        }
                    },
                },
                "type": "Policy",
                "attributes": {
                    "additional_insured_names": "additional_insured_names",
                    "carrier": "carrier",
                    "coverages": [
                        {
                            "data": {
                                "attributes": {
                                    "name": "x",
                                    "included": True,
                                    "limit": 0,
                                    "notes": "notes",
                                },
                                "type": "PolicyCoverage",
                            }
                        }
                    ],
                    "currency": "xxx",
                    "deductible": "-1669910",
                    "effective_date": parse_date("2019-12-27"),
                    "expiration_date": parse_date("2019-12-27"),
                    "external_reference": "external_reference",
                    "interested_party_email": "dev@stainless.com",
                    "interested_party_name": "interested_party_name",
                    "is_sold_by_sure": True,
                    "liability_limit": "-1669910",
                    "personal_property_limit": "-1669910",
                    "policy_number": "policy_number",
                    "policy_status": "policy_status",
                    "premium": "-1669910",
                    "premium_for_fees": "-1669910",
                    "primary_insured_name": "primary_insured_name",
                    "underwriter": "underwriter",
                },
            },
        )
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Verify) -> None:
        response = client.policies.with_raw_response.create(
            data={
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    }
                },
                "type": "Policy",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = response.parse()
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Verify) -> None:
        with client.policies.with_streaming_response.create(
            data={
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    }
                },
                "type": "Policy",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = response.parse()
            assert_matches_type(PolicyResponse, policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Verify) -> None:
        policy = client.policies.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Verify) -> None:
        policy = client.policies.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_policy=["external_reference"],
            include=["lease_address"],
        )
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Verify) -> None:
        response = client.policies.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = response.parse()
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Verify) -> None:
        with client.policies.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = response.parse()
            assert_matches_type(PolicyResponse, policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.policies.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: Verify) -> None:
        policy = client.policies.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    }
                },
                "type": "Policy",
            },
        )
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: Verify) -> None:
        policy = client.policies.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    },
                    "interested_party_address": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Address",
                        }
                    },
                    "lease_address": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Address",
                        }
                    },
                },
                "type": "Policy",
                "attributes": {
                    "additional_insured_names": "additional_insured_names",
                    "carrier": "carrier",
                    "coverages": [
                        {
                            "data": {
                                "attributes": {
                                    "name": "x",
                                    "included": True,
                                    "limit": 0,
                                    "notes": "notes",
                                },
                                "type": "PolicyCoverage",
                            }
                        }
                    ],
                    "currency": "xxx",
                    "deductible": "-1669910",
                    "effective_date": parse_date("2019-12-27"),
                    "expiration_date": parse_date("2019-12-27"),
                    "external_reference": "external_reference",
                    "interested_party_email": "dev@stainless.com",
                    "interested_party_name": "interested_party_name",
                    "is_sold_by_sure": True,
                    "liability_limit": "-1669910",
                    "personal_property_limit": "-1669910",
                    "policy_number": "policy_number",
                    "policy_status": "policy_status",
                    "premium": "-1669910",
                    "premium_for_fees": "-1669910",
                    "primary_insured_name": "primary_insured_name",
                    "underwriter": "underwriter",
                },
            },
        )
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: Verify) -> None:
        response = client.policies.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    }
                },
                "type": "Policy",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = response.parse()
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: Verify) -> None:
        with client.policies.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    }
                },
                "type": "Policy",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = response.parse()
            assert_matches_type(PolicyResponse, policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.policies.with_raw_response.update(
                id="",
                data={
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "relationships": {
                        "resident": {
                            "data": {
                                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                                "type": "Resident",
                            }
                        }
                    },
                    "type": "Policy",
                },
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Verify) -> None:
        policy = client.policies.list()
        assert_matches_type(SyncCursorPagination[Policy], policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Verify) -> None:
        policy = client.policies.list(
            fields_policy=["external_reference"],
            filter_resident_community_property_manager_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            filter_resident_community_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            filter_resident_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            include=["lease_address"],
            page_cursor="page[cursor]",
            page_size=0,
        )
        assert_matches_type(SyncCursorPagination[Policy], policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Verify) -> None:
        response = client.policies.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = response.parse()
        assert_matches_type(SyncCursorPagination[Policy], policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Verify) -> None:
        with client.policies.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = response.parse()
            assert_matches_type(SyncCursorPagination[Policy], policy, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncPolicies:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncVerify) -> None:
        policy = await async_client.policies.create(
            data={
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    }
                },
                "type": "Policy",
            },
        )
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncVerify) -> None:
        policy = await async_client.policies.create(
            data={
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    },
                    "interested_party_address": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Address",
                        }
                    },
                    "lease_address": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Address",
                        }
                    },
                },
                "type": "Policy",
                "attributes": {
                    "additional_insured_names": "additional_insured_names",
                    "carrier": "carrier",
                    "coverages": [
                        {
                            "data": {
                                "attributes": {
                                    "name": "x",
                                    "included": True,
                                    "limit": 0,
                                    "notes": "notes",
                                },
                                "type": "PolicyCoverage",
                            }
                        }
                    ],
                    "currency": "xxx",
                    "deductible": "-1669910",
                    "effective_date": parse_date("2019-12-27"),
                    "expiration_date": parse_date("2019-12-27"),
                    "external_reference": "external_reference",
                    "interested_party_email": "dev@stainless.com",
                    "interested_party_name": "interested_party_name",
                    "is_sold_by_sure": True,
                    "liability_limit": "-1669910",
                    "personal_property_limit": "-1669910",
                    "policy_number": "policy_number",
                    "policy_status": "policy_status",
                    "premium": "-1669910",
                    "premium_for_fees": "-1669910",
                    "primary_insured_name": "primary_insured_name",
                    "underwriter": "underwriter",
                },
            },
        )
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncVerify) -> None:
        response = await async_client.policies.with_raw_response.create(
            data={
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    }
                },
                "type": "Policy",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = await response.parse()
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncVerify) -> None:
        async with async_client.policies.with_streaming_response.create(
            data={
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    }
                },
                "type": "Policy",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = await response.parse()
            assert_matches_type(PolicyResponse, policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncVerify) -> None:
        policy = await async_client.policies.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncVerify) -> None:
        policy = await async_client.policies.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_policy=["external_reference"],
            include=["lease_address"],
        )
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncVerify) -> None:
        response = await async_client.policies.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = await response.parse()
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncVerify) -> None:
        async with async_client.policies.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = await response.parse()
            assert_matches_type(PolicyResponse, policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.policies.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncVerify) -> None:
        policy = await async_client.policies.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    }
                },
                "type": "Policy",
            },
        )
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncVerify) -> None:
        policy = await async_client.policies.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    },
                    "interested_party_address": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Address",
                        }
                    },
                    "lease_address": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Address",
                        }
                    },
                },
                "type": "Policy",
                "attributes": {
                    "additional_insured_names": "additional_insured_names",
                    "carrier": "carrier",
                    "coverages": [
                        {
                            "data": {
                                "attributes": {
                                    "name": "x",
                                    "included": True,
                                    "limit": 0,
                                    "notes": "notes",
                                },
                                "type": "PolicyCoverage",
                            }
                        }
                    ],
                    "currency": "xxx",
                    "deductible": "-1669910",
                    "effective_date": parse_date("2019-12-27"),
                    "expiration_date": parse_date("2019-12-27"),
                    "external_reference": "external_reference",
                    "interested_party_email": "dev@stainless.com",
                    "interested_party_name": "interested_party_name",
                    "is_sold_by_sure": True,
                    "liability_limit": "-1669910",
                    "personal_property_limit": "-1669910",
                    "policy_number": "policy_number",
                    "policy_status": "policy_status",
                    "premium": "-1669910",
                    "premium_for_fees": "-1669910",
                    "primary_insured_name": "primary_insured_name",
                    "underwriter": "underwriter",
                },
            },
        )
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncVerify) -> None:
        response = await async_client.policies.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    }
                },
                "type": "Policy",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = await response.parse()
        assert_matches_type(PolicyResponse, policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncVerify) -> None:
        async with async_client.policies.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    }
                },
                "type": "Policy",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = await response.parse()
            assert_matches_type(PolicyResponse, policy, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.policies.with_raw_response.update(
                id="",
                data={
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "relationships": {
                        "resident": {
                            "data": {
                                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                                "type": "Resident",
                            }
                        }
                    },
                    "type": "Policy",
                },
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncVerify) -> None:
        policy = await async_client.policies.list()
        assert_matches_type(AsyncCursorPagination[Policy], policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncVerify) -> None:
        policy = await async_client.policies.list(
            fields_policy=["external_reference"],
            filter_resident_community_property_manager_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            filter_resident_community_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            filter_resident_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            include=["lease_address"],
            page_cursor="page[cursor]",
            page_size=0,
        )
        assert_matches_type(AsyncCursorPagination[Policy], policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncVerify) -> None:
        response = await async_client.policies.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        policy = await response.parse()
        assert_matches_type(AsyncCursorPagination[Policy], policy, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncVerify) -> None:
        async with async_client.policies.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            policy = await response.parse()
            assert_matches_type(AsyncCursorPagination[Policy], policy, path=["response"])

        assert cast(Any, response.is_closed) is True
