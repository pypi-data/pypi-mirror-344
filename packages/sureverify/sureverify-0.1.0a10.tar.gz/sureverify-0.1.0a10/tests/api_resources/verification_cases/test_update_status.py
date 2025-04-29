# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sureverify import Verify, AsyncVerify

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUpdateStatus:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_cancelled(self, client: Verify) -> None:
        update_status = client.verification_cases.update_status.cancelled(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_cancelled(self, client: Verify) -> None:
        response = client.verification_cases.update_status.with_raw_response.cancelled(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        update_status = response.parse()
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_cancelled(self, client: Verify) -> None:
        with client.verification_cases.update_status.with_streaming_response.cancelled(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            update_status = response.parse()
            assert update_status is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_cancelled(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_cases.update_status.with_raw_response.cancelled(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_completed(self, client: Verify) -> None:
        update_status = client.verification_cases.update_status.completed(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "attributes": {"is_compliant": True},
                "type": "UpdateComplianceAction",
            },
        )
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_completed(self, client: Verify) -> None:
        response = client.verification_cases.update_status.with_raw_response.completed(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "attributes": {"is_compliant": True},
                "type": "UpdateComplianceAction",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        update_status = response.parse()
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_completed(self, client: Verify) -> None:
        with client.verification_cases.update_status.with_streaming_response.completed(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "attributes": {"is_compliant": True},
                "type": "UpdateComplianceAction",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            update_status = response.parse()
            assert update_status is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_completed(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_cases.update_status.with_raw_response.completed(
                id="",
                data={
                    "attributes": {"is_compliant": True},
                    "type": "UpdateComplianceAction",
                },
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_draft(self, client: Verify) -> None:
        update_status = client.verification_cases.update_status.draft(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_draft(self, client: Verify) -> None:
        response = client.verification_cases.update_status.with_raw_response.draft(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        update_status = response.parse()
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_draft(self, client: Verify) -> None:
        with client.verification_cases.update_status.with_streaming_response.draft(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            update_status = response.parse()
            assert update_status is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_draft(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_cases.update_status.with_raw_response.draft(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_further_review_required(self, client: Verify) -> None:
        update_status = client.verification_cases.update_status.further_review_required(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_further_review_required(self, client: Verify) -> None:
        response = client.verification_cases.update_status.with_raw_response.further_review_required(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        update_status = response.parse()
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_further_review_required(self, client: Verify) -> None:
        with client.verification_cases.update_status.with_streaming_response.further_review_required(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            update_status = response.parse()
            assert update_status is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_further_review_required(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_cases.update_status.with_raw_response.further_review_required(
                "",
            )


class TestAsyncUpdateStatus:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_cancelled(self, async_client: AsyncVerify) -> None:
        update_status = await async_client.verification_cases.update_status.cancelled(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_cancelled(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_cases.update_status.with_raw_response.cancelled(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        update_status = await response.parse()
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_cancelled(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_cases.update_status.with_streaming_response.cancelled(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            update_status = await response.parse()
            assert update_status is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_cancelled(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_cases.update_status.with_raw_response.cancelled(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_completed(self, async_client: AsyncVerify) -> None:
        update_status = await async_client.verification_cases.update_status.completed(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "attributes": {"is_compliant": True},
                "type": "UpdateComplianceAction",
            },
        )
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_completed(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_cases.update_status.with_raw_response.completed(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "attributes": {"is_compliant": True},
                "type": "UpdateComplianceAction",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        update_status = await response.parse()
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_completed(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_cases.update_status.with_streaming_response.completed(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "attributes": {"is_compliant": True},
                "type": "UpdateComplianceAction",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            update_status = await response.parse()
            assert update_status is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_completed(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_cases.update_status.with_raw_response.completed(
                id="",
                data={
                    "attributes": {"is_compliant": True},
                    "type": "UpdateComplianceAction",
                },
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_draft(self, async_client: AsyncVerify) -> None:
        update_status = await async_client.verification_cases.update_status.draft(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_draft(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_cases.update_status.with_raw_response.draft(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        update_status = await response.parse()
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_draft(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_cases.update_status.with_streaming_response.draft(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            update_status = await response.parse()
            assert update_status is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_draft(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_cases.update_status.with_raw_response.draft(
                "",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_further_review_required(self, async_client: AsyncVerify) -> None:
        update_status = await async_client.verification_cases.update_status.further_review_required(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_further_review_required(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_cases.update_status.with_raw_response.further_review_required(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        update_status = await response.parse()
        assert update_status is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_further_review_required(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_cases.update_status.with_streaming_response.further_review_required(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            update_status = await response.parse()
            assert update_status is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_further_review_required(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_cases.update_status.with_raw_response.further_review_required(
                "",
            )
