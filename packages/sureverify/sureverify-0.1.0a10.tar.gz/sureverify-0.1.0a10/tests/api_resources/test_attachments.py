# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sureverify import Verify, AsyncVerify
from tests.utils import assert_matches_type
from sureverify.types import AttachmentCreateResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAttachments:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Verify) -> None:
        attachment = client.attachments.create(
            data={
                "attributes": {
                    "content_type": "application/pdf",
                    "name": "name",
                },
                "type": "Attachment",
            },
        )
        assert_matches_type(AttachmentCreateResponse, attachment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Verify) -> None:
        response = client.attachments.with_raw_response.create(
            data={
                "attributes": {
                    "content_type": "application/pdf",
                    "name": "name",
                },
                "type": "Attachment",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        attachment = response.parse()
        assert_matches_type(AttachmentCreateResponse, attachment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Verify) -> None:
        with client.attachments.with_streaming_response.create(
            data={
                "attributes": {
                    "content_type": "application/pdf",
                    "name": "name",
                },
                "type": "Attachment",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            attachment = response.parse()
            assert_matches_type(AttachmentCreateResponse, attachment, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAttachments:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncVerify) -> None:
        attachment = await async_client.attachments.create(
            data={
                "attributes": {
                    "content_type": "application/pdf",
                    "name": "name",
                },
                "type": "Attachment",
            },
        )
        assert_matches_type(AttachmentCreateResponse, attachment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncVerify) -> None:
        response = await async_client.attachments.with_raw_response.create(
            data={
                "attributes": {
                    "content_type": "application/pdf",
                    "name": "name",
                },
                "type": "Attachment",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        attachment = await response.parse()
        assert_matches_type(AttachmentCreateResponse, attachment, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncVerify) -> None:
        async with async_client.attachments.with_streaming_response.create(
            data={
                "attributes": {
                    "content_type": "application/pdf",
                    "name": "name",
                },
                "type": "Attachment",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            attachment = await response.parse()
            assert_matches_type(AttachmentCreateResponse, attachment, path=["response"])

        assert cast(Any, response.is_closed) is True
