# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sureverify import Verify, AsyncVerify
from tests.utils import assert_matches_type
from sureverify.types import (
    VerificationCase,
    VerificationCaseResponse,
)
from sureverify._utils import parse_date, parse_datetime
from sureverify.pagination import SyncCursorPagination, AsyncCursorPagination

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVerificationCases:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Verify) -> None:
        verification_case = client.verification_cases.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationCase",
            },
        )
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Verify) -> None:
        verification_case = client.verification_cases.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    },
                    "attachments": {
                        "data": [
                            {
                                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                                "type": "Attachment",
                            }
                        ]
                    },
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "policy": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Policy",
                        }
                    },
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    },
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "VerificationCase",
                "attributes": {
                    "due_at": parse_date("2019-12-27"),
                    "external_reference": "external_reference",
                    "notes": "notes",
                    "submitted_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                },
            },
        )
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Verify) -> None:
        response = client.verification_cases.with_raw_response.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationCase",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_case = response.parse()
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Verify) -> None:
        with client.verification_cases.with_streaming_response.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationCase",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_case = response.parse()
            assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Verify) -> None:
        verification_case = client.verification_cases.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Verify) -> None:
        verification_case = client.verification_cases.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_verification_case=["status"],
            include=["property_manager"],
        )
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Verify) -> None:
        response = client.verification_cases.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_case = response.parse()
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Verify) -> None:
        with client.verification_cases.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_case = response.parse()
            assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_cases.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: Verify) -> None:
        verification_case = client.verification_cases.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationCase",
            },
        )
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: Verify) -> None:
        verification_case = client.verification_cases.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    },
                    "attachments": {
                        "data": [
                            {
                                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                                "type": "Attachment",
                            }
                        ]
                    },
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "policy": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Policy",
                        }
                    },
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    },
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "VerificationCase",
                "attributes": {
                    "due_at": parse_date("2019-12-27"),
                    "external_reference": "external_reference",
                    "notes": "notes",
                    "submitted_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                },
            },
        )
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: Verify) -> None:
        response = client.verification_cases.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationCase",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_case = response.parse()
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: Verify) -> None:
        with client.verification_cases.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationCase",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_case = response.parse()
            assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_cases.with_raw_response.update(
                id="",
                data={
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "relationships": {
                        "property_manager": {
                            "data": {
                                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                                "type": "PropertyManager",
                            }
                        }
                    },
                    "type": "VerificationCase",
                },
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Verify) -> None:
        verification_case = client.verification_cases.list()
        assert_matches_type(SyncCursorPagination[VerificationCase], verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Verify) -> None:
        verification_case = client.verification_cases.list(
            fields_verification_case=["status"],
            filter_community_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            filter_property_manager_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            filter_resident_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            include=["property_manager"],
            page_cursor="page[cursor]",
            page_size=0,
        )
        assert_matches_type(SyncCursorPagination[VerificationCase], verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Verify) -> None:
        response = client.verification_cases.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_case = response.parse()
        assert_matches_type(SyncCursorPagination[VerificationCase], verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Verify) -> None:
        with client.verification_cases.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_case = response.parse()
            assert_matches_type(SyncCursorPagination[VerificationCase], verification_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_enqueue_processing(self, client: Verify) -> None:
        verification_case = client.verification_cases.enqueue_processing(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert verification_case is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_enqueue_processing(self, client: Verify) -> None:
        response = client.verification_cases.with_raw_response.enqueue_processing(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_case = response.parse()
        assert verification_case is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_enqueue_processing(self, client: Verify) -> None:
        with client.verification_cases.with_streaming_response.enqueue_processing(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_case = response.parse()
            assert verification_case is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_enqueue_processing(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_cases.with_raw_response.enqueue_processing(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_reset_checks(self, client: Verify) -> None:
        verification_case = client.verification_cases.reset_checks(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert verification_case is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_reset_checks(self, client: Verify) -> None:
        response = client.verification_cases.with_raw_response.reset_checks(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_case = response.parse()
        assert verification_case is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_reset_checks(self, client: Verify) -> None:
        with client.verification_cases.with_streaming_response.reset_checks(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_case = response.parse()
            assert verification_case is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_reset_checks(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_cases.with_raw_response.reset_checks(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_send_reminder_email(self, client: Verify) -> None:
        verification_case = client.verification_cases.send_reminder_email(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert verification_case is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_send_reminder_email(self, client: Verify) -> None:
        response = client.verification_cases.with_raw_response.send_reminder_email(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_case = response.parse()
        assert verification_case is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_send_reminder_email(self, client: Verify) -> None:
        with client.verification_cases.with_streaming_response.send_reminder_email(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_case = response.parse()
            assert verification_case is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_send_reminder_email(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_cases.with_raw_response.send_reminder_email(
                "",
            )


class TestAsyncVerificationCases:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncVerify) -> None:
        verification_case = await async_client.verification_cases.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationCase",
            },
        )
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncVerify) -> None:
        verification_case = await async_client.verification_cases.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    },
                    "attachments": {
                        "data": [
                            {
                                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                                "type": "Attachment",
                            }
                        ]
                    },
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "policy": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Policy",
                        }
                    },
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    },
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "VerificationCase",
                "attributes": {
                    "due_at": parse_date("2019-12-27"),
                    "external_reference": "external_reference",
                    "notes": "notes",
                    "submitted_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                },
            },
        )
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_cases.with_raw_response.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationCase",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_case = await response.parse()
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_cases.with_streaming_response.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationCase",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_case = await response.parse()
            assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncVerify) -> None:
        verification_case = await async_client.verification_cases.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncVerify) -> None:
        verification_case = await async_client.verification_cases.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_verification_case=["status"],
            include=["property_manager"],
        )
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_cases.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_case = await response.parse()
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_cases.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_case = await response.parse()
            assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_cases.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncVerify) -> None:
        verification_case = await async_client.verification_cases.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationCase",
            },
        )
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncVerify) -> None:
        verification_case = await async_client.verification_cases.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    },
                    "attachments": {
                        "data": [
                            {
                                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                                "type": "Attachment",
                            }
                        ]
                    },
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "policy": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Policy",
                        }
                    },
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    },
                    "resident": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Resident",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "VerificationCase",
                "attributes": {
                    "due_at": parse_date("2019-12-27"),
                    "external_reference": "external_reference",
                    "notes": "notes",
                    "submitted_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                },
            },
        )
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_cases.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationCase",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_case = await response.parse()
        assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_cases.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationCase",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_case = await response.parse()
            assert_matches_type(VerificationCaseResponse, verification_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_cases.with_raw_response.update(
                id="",
                data={
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "relationships": {
                        "property_manager": {
                            "data": {
                                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                                "type": "PropertyManager",
                            }
                        }
                    },
                    "type": "VerificationCase",
                },
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncVerify) -> None:
        verification_case = await async_client.verification_cases.list()
        assert_matches_type(AsyncCursorPagination[VerificationCase], verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncVerify) -> None:
        verification_case = await async_client.verification_cases.list(
            fields_verification_case=["status"],
            filter_community_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            filter_property_manager_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            filter_resident_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            include=["property_manager"],
            page_cursor="page[cursor]",
            page_size=0,
        )
        assert_matches_type(AsyncCursorPagination[VerificationCase], verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_cases.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_case = await response.parse()
        assert_matches_type(AsyncCursorPagination[VerificationCase], verification_case, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_cases.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_case = await response.parse()
            assert_matches_type(AsyncCursorPagination[VerificationCase], verification_case, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_enqueue_processing(self, async_client: AsyncVerify) -> None:
        verification_case = await async_client.verification_cases.enqueue_processing(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert verification_case is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_enqueue_processing(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_cases.with_raw_response.enqueue_processing(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_case = await response.parse()
        assert verification_case is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_enqueue_processing(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_cases.with_streaming_response.enqueue_processing(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_case = await response.parse()
            assert verification_case is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_enqueue_processing(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_cases.with_raw_response.enqueue_processing(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_reset_checks(self, async_client: AsyncVerify) -> None:
        verification_case = await async_client.verification_cases.reset_checks(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert verification_case is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_reset_checks(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_cases.with_raw_response.reset_checks(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_case = await response.parse()
        assert verification_case is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_reset_checks(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_cases.with_streaming_response.reset_checks(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_case = await response.parse()
            assert verification_case is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_reset_checks(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_cases.with_raw_response.reset_checks(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_send_reminder_email(self, async_client: AsyncVerify) -> None:
        verification_case = await async_client.verification_cases.send_reminder_email(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert verification_case is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_send_reminder_email(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_cases.with_raw_response.send_reminder_email(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_case = await response.parse()
        assert verification_case is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_send_reminder_email(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_cases.with_streaming_response.send_reminder_email(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_case = await response.parse()
            assert verification_case is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_send_reminder_email(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_cases.with_raw_response.send_reminder_email(
                "",
            )
