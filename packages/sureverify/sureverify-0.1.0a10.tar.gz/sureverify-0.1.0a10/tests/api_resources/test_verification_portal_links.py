# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sureverify import Verify, AsyncVerify
from tests.utils import assert_matches_type
from sureverify.types import (
    VerificationPortalLink,
    VerificationPortalLinkResponse,
)
from sureverify.pagination import SyncCursorPagination, AsyncCursorPagination

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVerificationPortalLinks:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Verify) -> None:
        verification_portal_link = client.verification_portal_links.create(
            data={
                "attributes": {
                    "location": "header",
                    "title": "x",
                    "url": "https://example.com",
                },
                "relationships": {
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    }
                },
                "type": "VerificationPortalLink",
            },
        )
        assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Verify) -> None:
        response = client.verification_portal_links.with_raw_response.create(
            data={
                "attributes": {
                    "location": "header",
                    "title": "x",
                    "url": "https://example.com",
                },
                "relationships": {
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    }
                },
                "type": "VerificationPortalLink",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal_link = response.parse()
        assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Verify) -> None:
        with client.verification_portal_links.with_streaming_response.create(
            data={
                "attributes": {
                    "location": "header",
                    "title": "x",
                    "url": "https://example.com",
                },
                "relationships": {
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    }
                },
                "type": "VerificationPortalLink",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal_link = response.parse()
            assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Verify) -> None:
        verification_portal_link = client.verification_portal_links.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Verify) -> None:
        verification_portal_link = client.verification_portal_links.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_verification_portal_link=["portal"],
        )
        assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Verify) -> None:
        response = client.verification_portal_links.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal_link = response.parse()
        assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Verify) -> None:
        with client.verification_portal_links.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal_link = response.parse()
            assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_portal_links.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: Verify) -> None:
        verification_portal_link = client.verification_portal_links.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {
                    "location": "header",
                    "title": "x",
                    "url": "https://example.com",
                },
                "relationships": {
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    }
                },
                "type": "VerificationPortalLink",
            },
        )
        assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: Verify) -> None:
        response = client.verification_portal_links.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {
                    "location": "header",
                    "title": "x",
                    "url": "https://example.com",
                },
                "relationships": {
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    }
                },
                "type": "VerificationPortalLink",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal_link = response.parse()
        assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: Verify) -> None:
        with client.verification_portal_links.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {
                    "location": "header",
                    "title": "x",
                    "url": "https://example.com",
                },
                "relationships": {
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    }
                },
                "type": "VerificationPortalLink",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal_link = response.parse()
            assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_portal_links.with_raw_response.update(
                id="",
                data={
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "attributes": {
                        "location": "header",
                        "title": "x",
                        "url": "https://example.com",
                    },
                    "relationships": {
                        "portal": {
                            "data": {
                                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                                "type": "VerificationPortal",
                            }
                        }
                    },
                    "type": "VerificationPortalLink",
                },
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Verify) -> None:
        verification_portal_link = client.verification_portal_links.list()
        assert_matches_type(SyncCursorPagination[VerificationPortalLink], verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Verify) -> None:
        verification_portal_link = client.verification_portal_links.list(
            fields_verification_portal_link=["portal"],
            filter_portal_property_manager_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            filter_portal_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            page_cursor="page[cursor]",
            page_size=0,
        )
        assert_matches_type(SyncCursorPagination[VerificationPortalLink], verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Verify) -> None:
        response = client.verification_portal_links.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal_link = response.parse()
        assert_matches_type(SyncCursorPagination[VerificationPortalLink], verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Verify) -> None:
        with client.verification_portal_links.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal_link = response.parse()
            assert_matches_type(
                SyncCursorPagination[VerificationPortalLink], verification_portal_link, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_delete(self, client: Verify) -> None:
        verification_portal_link = client.verification_portal_links.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert verification_portal_link is None

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_delete(self, client: Verify) -> None:
        response = client.verification_portal_links.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal_link = response.parse()
        assert verification_portal_link is None

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_delete(self, client: Verify) -> None:
        with client.verification_portal_links.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal_link = response.parse()
            assert verification_portal_link is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_delete(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_portal_links.with_raw_response.delete(
                "",
            )


class TestAsyncVerificationPortalLinks:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncVerify) -> None:
        verification_portal_link = await async_client.verification_portal_links.create(
            data={
                "attributes": {
                    "location": "header",
                    "title": "x",
                    "url": "https://example.com",
                },
                "relationships": {
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    }
                },
                "type": "VerificationPortalLink",
            },
        )
        assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_portal_links.with_raw_response.create(
            data={
                "attributes": {
                    "location": "header",
                    "title": "x",
                    "url": "https://example.com",
                },
                "relationships": {
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    }
                },
                "type": "VerificationPortalLink",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal_link = await response.parse()
        assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_portal_links.with_streaming_response.create(
            data={
                "attributes": {
                    "location": "header",
                    "title": "x",
                    "url": "https://example.com",
                },
                "relationships": {
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    }
                },
                "type": "VerificationPortalLink",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal_link = await response.parse()
            assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncVerify) -> None:
        verification_portal_link = await async_client.verification_portal_links.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncVerify) -> None:
        verification_portal_link = await async_client.verification_portal_links.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_verification_portal_link=["portal"],
        )
        assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_portal_links.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal_link = await response.parse()
        assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_portal_links.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal_link = await response.parse()
            assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_portal_links.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncVerify) -> None:
        verification_portal_link = await async_client.verification_portal_links.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {
                    "location": "header",
                    "title": "x",
                    "url": "https://example.com",
                },
                "relationships": {
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    }
                },
                "type": "VerificationPortalLink",
            },
        )
        assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_portal_links.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {
                    "location": "header",
                    "title": "x",
                    "url": "https://example.com",
                },
                "relationships": {
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    }
                },
                "type": "VerificationPortalLink",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal_link = await response.parse()
        assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_portal_links.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {
                    "location": "header",
                    "title": "x",
                    "url": "https://example.com",
                },
                "relationships": {
                    "portal": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "VerificationPortal",
                        }
                    }
                },
                "type": "VerificationPortalLink",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal_link = await response.parse()
            assert_matches_type(VerificationPortalLinkResponse, verification_portal_link, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_portal_links.with_raw_response.update(
                id="",
                data={
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "attributes": {
                        "location": "header",
                        "title": "x",
                        "url": "https://example.com",
                    },
                    "relationships": {
                        "portal": {
                            "data": {
                                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                                "type": "VerificationPortal",
                            }
                        }
                    },
                    "type": "VerificationPortalLink",
                },
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncVerify) -> None:
        verification_portal_link = await async_client.verification_portal_links.list()
        assert_matches_type(AsyncCursorPagination[VerificationPortalLink], verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncVerify) -> None:
        verification_portal_link = await async_client.verification_portal_links.list(
            fields_verification_portal_link=["portal"],
            filter_portal_property_manager_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            filter_portal_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            page_cursor="page[cursor]",
            page_size=0,
        )
        assert_matches_type(AsyncCursorPagination[VerificationPortalLink], verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_portal_links.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal_link = await response.parse()
        assert_matches_type(AsyncCursorPagination[VerificationPortalLink], verification_portal_link, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_portal_links.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal_link = await response.parse()
            assert_matches_type(
                AsyncCursorPagination[VerificationPortalLink], verification_portal_link, path=["response"]
            )

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_delete(self, async_client: AsyncVerify) -> None:
        verification_portal_link = await async_client.verification_portal_links.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert verification_portal_link is None

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_portal_links.with_raw_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal_link = await response.parse()
        assert verification_portal_link is None

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_portal_links.with_streaming_response.delete(
            "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal_link = await response.parse()
            assert verification_portal_link is None

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_delete(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_portal_links.with_raw_response.delete(
                "",
            )
