# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sureverify import Verify, AsyncVerify
from tests.utils import assert_matches_type
from sureverify.types import (
    VerificationSessionResponse,
)
from sureverify._utils import parse_date, parse_datetime

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVerificationSessions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Verify) -> None:
        verification_session = client.verification_sessions.create(
            data={
                "attributes": {
                    "expires_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "request": {
                        "related_record": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "property_manager",
                        },
                        "settings": {
                            "features": {},
                            "mode": {},
                        },
                    },
                },
                "type": "VerificationSession",
            },
        )
        assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Verify) -> None:
        verification_session = client.verification_sessions.create(
            data={
                "attributes": {
                    "expires_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "request": {
                        "related_record": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "property_manager",
                        },
                        "settings": {
                            "features": {
                                "purchase": {
                                    "details_page": {"enabled": True},
                                    "enabled": True,
                                    "instructions_page": {
                                        "coverage_requirements_section": {"enabled": True},
                                        "enabled": True,
                                        "evidence_requirements_section": {"enabled": True},
                                        "explainer_section": {"enabled": True},
                                        "interested_party_section": {"enabled": True},
                                    },
                                },
                                "upload": {
                                    "details_page": {"enabled": True},
                                    "enabled": True,
                                    "instructions_page": {
                                        "coverage_requirements_section": {"enabled": True},
                                        "enabled": True,
                                        "evidence_requirements_section": {"enabled": True},
                                        "explainer_section": {"enabled": True},
                                        "interested_party_section": {"enabled": True},
                                    },
                                },
                            },
                            "mode": {
                                "embedded": {
                                    "analytics_enabled": True,
                                    "background_color": "x",
                                    "enabled": True,
                                },
                                "hosted": {
                                    "analytics_enabled": True,
                                    "enabled": True,
                                    "favicon_bgcolor": "x",
                                    "favicon_url": "https://example.com",
                                    "footer": {
                                        "links": [
                                            {
                                                "title": "xx",
                                                "url": "https://example.com",
                                            }
                                        ],
                                        "text": "x",
                                    },
                                    "header": {
                                        "links": [
                                            {
                                                "title": "xx",
                                                "url": "https://example.com",
                                            }
                                        ]
                                    },
                                    "return_url": "https://example.com",
                                    "support_chat_enabled": True,
                                    "user_survey_enabled": True,
                                },
                            },
                            "brand": {
                                "colors": {
                                    "muted": {"hex": "x"},
                                    "primary": {"hex": "x"},
                                    "secondary": {"hex": "x"},
                                },
                                "logo_url": "https://example.com",
                                "style": {"enabled": True},
                                "title": "xx",
                            },
                            "external_ref": "x",
                            "on_completion": {
                                "when_compliant": {
                                    "custom_event_name": "xx",
                                    "message": "x",
                                    "redirect": "https://example.com",
                                },
                                "when_noncompliant": {
                                    "custom_event_name": "xx",
                                    "message": "x",
                                    "redirect": "https://example.com",
                                },
                                "when_submitted": {
                                    "custom_event_name": "xx",
                                    "message": "x",
                                    "redirect": "https://example.com",
                                },
                            },
                            "restrictions": {
                                "coverage_requirements": [
                                    {
                                        "coverage_kind": "personal_property",
                                        "coverage_minimum": "coverage_minimum",
                                    }
                                ],
                                "editable_fields": ["address.line1"],
                                "max_effective_date": parse_date("2019-12-27"),
                                "max_expiration_date": parse_date("2019-12-27"),
                                "min_effective_date": parse_date("2019-12-27"),
                                "min_expiration_date": parse_date("2019-12-27"),
                            },
                        },
                        "input": {
                            "address": {
                                "city": "x",
                                "line1": "xxx",
                                "line2": "x",
                                "postal": "xxxxx",
                                "state_code": "xx",
                            },
                            "carrier": "xx",
                            "effective_date": parse_date("2019-12-27"),
                            "email": "dev@stainless.com",
                            "expiration_date": parse_date("2019-12-27"),
                            "first_name": "xx",
                            "last_name": "xx",
                            "lease_end_date": parse_date("2019-12-27"),
                            "lease_start_date": parse_date("2019-12-27"),
                            "liability_coverage_amount": 0,
                            "phone_number": "x",
                            "policy_number": "xx",
                        },
                    },
                },
                "type": "VerificationSession",
                "relationships": {},
            },
        )
        assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Verify) -> None:
        response = client.verification_sessions.with_raw_response.create(
            data={
                "attributes": {
                    "expires_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "request": {
                        "related_record": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "property_manager",
                        },
                        "settings": {
                            "features": {},
                            "mode": {},
                        },
                    },
                },
                "type": "VerificationSession",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_session = response.parse()
        assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Verify) -> None:
        with client.verification_sessions.with_streaming_response.create(
            data={
                "attributes": {
                    "expires_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "request": {
                        "related_record": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "property_manager",
                        },
                        "settings": {
                            "features": {},
                            "mode": {},
                        },
                    },
                },
                "type": "VerificationSession",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_session = response.parse()
            assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Verify) -> None:
        verification_session = client.verification_sessions.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Verify) -> None:
        verification_session = client.verification_sessions.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_verification_session=["case"],
        )
        assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Verify) -> None:
        response = client.verification_sessions.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_session = response.parse()
        assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Verify) -> None:
        with client.verification_sessions.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_session = response.parse()
            assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_sessions.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: Verify) -> None:
        verification_session = client.verification_sessions.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert verification_session is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: Verify) -> None:
        response = client.verification_sessions.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_session = response.parse()
        assert verification_session is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: Verify) -> None:
        with client.verification_sessions.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_session = response.parse()
            assert verification_session is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_sessions.with_raw_response.delete(
                "",
            )


class TestAsyncVerificationSessions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncVerify) -> None:
        verification_session = await async_client.verification_sessions.create(
            data={
                "attributes": {
                    "expires_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "request": {
                        "related_record": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "property_manager",
                        },
                        "settings": {
                            "features": {},
                            "mode": {},
                        },
                    },
                },
                "type": "VerificationSession",
            },
        )
        assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncVerify) -> None:
        verification_session = await async_client.verification_sessions.create(
            data={
                "attributes": {
                    "expires_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "request": {
                        "related_record": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "property_manager",
                        },
                        "settings": {
                            "features": {
                                "purchase": {
                                    "details_page": {"enabled": True},
                                    "enabled": True,
                                    "instructions_page": {
                                        "coverage_requirements_section": {"enabled": True},
                                        "enabled": True,
                                        "evidence_requirements_section": {"enabled": True},
                                        "explainer_section": {"enabled": True},
                                        "interested_party_section": {"enabled": True},
                                    },
                                },
                                "upload": {
                                    "details_page": {"enabled": True},
                                    "enabled": True,
                                    "instructions_page": {
                                        "coverage_requirements_section": {"enabled": True},
                                        "enabled": True,
                                        "evidence_requirements_section": {"enabled": True},
                                        "explainer_section": {"enabled": True},
                                        "interested_party_section": {"enabled": True},
                                    },
                                },
                            },
                            "mode": {
                                "embedded": {
                                    "analytics_enabled": True,
                                    "background_color": "x",
                                    "enabled": True,
                                },
                                "hosted": {
                                    "analytics_enabled": True,
                                    "enabled": True,
                                    "favicon_bgcolor": "x",
                                    "favicon_url": "https://example.com",
                                    "footer": {
                                        "links": [
                                            {
                                                "title": "xx",
                                                "url": "https://example.com",
                                            }
                                        ],
                                        "text": "x",
                                    },
                                    "header": {
                                        "links": [
                                            {
                                                "title": "xx",
                                                "url": "https://example.com",
                                            }
                                        ]
                                    },
                                    "return_url": "https://example.com",
                                    "support_chat_enabled": True,
                                    "user_survey_enabled": True,
                                },
                            },
                            "brand": {
                                "colors": {
                                    "muted": {"hex": "x"},
                                    "primary": {"hex": "x"},
                                    "secondary": {"hex": "x"},
                                },
                                "logo_url": "https://example.com",
                                "style": {"enabled": True},
                                "title": "xx",
                            },
                            "external_ref": "x",
                            "on_completion": {
                                "when_compliant": {
                                    "custom_event_name": "xx",
                                    "message": "x",
                                    "redirect": "https://example.com",
                                },
                                "when_noncompliant": {
                                    "custom_event_name": "xx",
                                    "message": "x",
                                    "redirect": "https://example.com",
                                },
                                "when_submitted": {
                                    "custom_event_name": "xx",
                                    "message": "x",
                                    "redirect": "https://example.com",
                                },
                            },
                            "restrictions": {
                                "coverage_requirements": [
                                    {
                                        "coverage_kind": "personal_property",
                                        "coverage_minimum": "coverage_minimum",
                                    }
                                ],
                                "editable_fields": ["address.line1"],
                                "max_effective_date": parse_date("2019-12-27"),
                                "max_expiration_date": parse_date("2019-12-27"),
                                "min_effective_date": parse_date("2019-12-27"),
                                "min_expiration_date": parse_date("2019-12-27"),
                            },
                        },
                        "input": {
                            "address": {
                                "city": "x",
                                "line1": "xxx",
                                "line2": "x",
                                "postal": "xxxxx",
                                "state_code": "xx",
                            },
                            "carrier": "xx",
                            "effective_date": parse_date("2019-12-27"),
                            "email": "dev@stainless.com",
                            "expiration_date": parse_date("2019-12-27"),
                            "first_name": "xx",
                            "last_name": "xx",
                            "lease_end_date": parse_date("2019-12-27"),
                            "lease_start_date": parse_date("2019-12-27"),
                            "liability_coverage_amount": 0,
                            "phone_number": "x",
                            "policy_number": "xx",
                        },
                    },
                },
                "type": "VerificationSession",
                "relationships": {},
            },
        )
        assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_sessions.with_raw_response.create(
            data={
                "attributes": {
                    "expires_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "request": {
                        "related_record": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "property_manager",
                        },
                        "settings": {
                            "features": {},
                            "mode": {},
                        },
                    },
                },
                "type": "VerificationSession",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_session = await response.parse()
        assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_sessions.with_streaming_response.create(
            data={
                "attributes": {
                    "expires_at": parse_datetime("2019-12-27T18:11:19.117Z"),
                    "request": {
                        "related_record": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "property_manager",
                        },
                        "settings": {
                            "features": {},
                            "mode": {},
                        },
                    },
                },
                "type": "VerificationSession",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_session = await response.parse()
            assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncVerify) -> None:
        verification_session = await async_client.verification_sessions.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncVerify) -> None:
        verification_session = await async_client.verification_sessions.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_verification_session=["case"],
        )
        assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_sessions.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_session = await response.parse()
        assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_sessions.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_session = await response.parse()
            assert_matches_type(VerificationSessionResponse, verification_session, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_sessions.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncVerify) -> None:
        verification_session = await async_client.verification_sessions.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert verification_session is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_sessions.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_session = await response.parse()
        assert verification_session is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_sessions.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_session = await response.parse()
            assert verification_session is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_sessions.with_raw_response.delete(
                "",
            )
