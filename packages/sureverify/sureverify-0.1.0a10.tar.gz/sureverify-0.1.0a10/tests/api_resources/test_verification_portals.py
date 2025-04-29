# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sureverify import Verify, AsyncVerify
from tests.utils import assert_matches_type
from sureverify.types import (
    VerificationPortal,
    VerificationPortalResponse,
)
from sureverify.pagination import SyncCursorPagination, AsyncCursorPagination

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestVerificationPortals:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Verify) -> None:
        verification_portal = client.verification_portals.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationPortal",
            },
        )
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Verify) -> None:
        verification_portal = client.verification_portals.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationPortal",
                "attributes": {
                    "logo": b"raw file contents",
                    "muted_color": "#Afd",
                    "only_docs_form": True,
                    "primary_color": "#Afd",
                    "secondary_color": "#Afd",
                    "show_purchase_flow": True,
                    "slug": "slug",
                    "title": "title",
                },
            },
        )
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Verify) -> None:
        response = client.verification_portals.with_raw_response.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationPortal",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal = response.parse()
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Verify) -> None:
        with client.verification_portals.with_streaming_response.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationPortal",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal = response.parse()
            assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Verify) -> None:
        verification_portal = client.verification_portals.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Verify) -> None:
        verification_portal = client.verification_portals.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_verification_portal=["property_manager"],
            include=["property_manager"],
        )
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Verify) -> None:
        response = client.verification_portals.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal = response.parse()
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Verify) -> None:
        with client.verification_portals.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal = response.parse()
            assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_portals.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: Verify) -> None:
        verification_portal = client.verification_portals.update(
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
                "type": "VerificationPortal",
            },
        )
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: Verify) -> None:
        verification_portal = client.verification_portals.update(
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
                "type": "VerificationPortal",
                "attributes": {
                    "logo": b"raw file contents",
                    "muted_color": "#Afd",
                    "only_docs_form": True,
                    "primary_color": "#Afd",
                    "secondary_color": "#Afd",
                    "show_purchase_flow": True,
                    "slug": "slug",
                    "title": "title",
                },
            },
        )
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: Verify) -> None:
        response = client.verification_portals.with_raw_response.update(
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
                "type": "VerificationPortal",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal = response.parse()
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: Verify) -> None:
        with client.verification_portals.with_streaming_response.update(
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
                "type": "VerificationPortal",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal = response.parse()
            assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.verification_portals.with_raw_response.update(
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
                    "type": "VerificationPortal",
                },
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Verify) -> None:
        verification_portal = client.verification_portals.list()
        assert_matches_type(SyncCursorPagination[VerificationPortal], verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Verify) -> None:
        verification_portal = client.verification_portals.list(
            fields_verification_portal=["property_manager"],
            filter_property_manager_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            include=["property_manager"],
            page_cursor="page[cursor]",
            page_size=0,
        )
        assert_matches_type(SyncCursorPagination[VerificationPortal], verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Verify) -> None:
        response = client.verification_portals.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal = response.parse()
        assert_matches_type(SyncCursorPagination[VerificationPortal], verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Verify) -> None:
        with client.verification_portals.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal = response.parse()
            assert_matches_type(SyncCursorPagination[VerificationPortal], verification_portal, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncVerificationPortals:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncVerify) -> None:
        verification_portal = await async_client.verification_portals.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationPortal",
            },
        )
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncVerify) -> None:
        verification_portal = await async_client.verification_portals.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationPortal",
                "attributes": {
                    "logo": b"raw file contents",
                    "muted_color": "#Afd",
                    "only_docs_form": True,
                    "primary_color": "#Afd",
                    "secondary_color": "#Afd",
                    "show_purchase_flow": True,
                    "slug": "slug",
                    "title": "title",
                },
            },
        )
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_portals.with_raw_response.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationPortal",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal = await response.parse()
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_portals.with_streaming_response.create(
            data={
                "relationships": {
                    "property_manager": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "PropertyManager",
                        }
                    }
                },
                "type": "VerificationPortal",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal = await response.parse()
            assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncVerify) -> None:
        verification_portal = await async_client.verification_portals.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncVerify) -> None:
        verification_portal = await async_client.verification_portals.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_verification_portal=["property_manager"],
            include=["property_manager"],
        )
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_portals.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal = await response.parse()
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_portals.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal = await response.parse()
            assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_portals.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncVerify) -> None:
        verification_portal = await async_client.verification_portals.update(
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
                "type": "VerificationPortal",
            },
        )
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncVerify) -> None:
        verification_portal = await async_client.verification_portals.update(
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
                "type": "VerificationPortal",
                "attributes": {
                    "logo": b"raw file contents",
                    "muted_color": "#Afd",
                    "only_docs_form": True,
                    "primary_color": "#Afd",
                    "secondary_color": "#Afd",
                    "show_purchase_flow": True,
                    "slug": "slug",
                    "title": "title",
                },
            },
        )
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_portals.with_raw_response.update(
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
                "type": "VerificationPortal",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal = await response.parse()
        assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_portals.with_streaming_response.update(
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
                "type": "VerificationPortal",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal = await response.parse()
            assert_matches_type(VerificationPortalResponse, verification_portal, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.verification_portals.with_raw_response.update(
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
                    "type": "VerificationPortal",
                },
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncVerify) -> None:
        verification_portal = await async_client.verification_portals.list()
        assert_matches_type(AsyncCursorPagination[VerificationPortal], verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncVerify) -> None:
        verification_portal = await async_client.verification_portals.list(
            fields_verification_portal=["property_manager"],
            filter_property_manager_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            include=["property_manager"],
            page_cursor="page[cursor]",
            page_size=0,
        )
        assert_matches_type(AsyncCursorPagination[VerificationPortal], verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncVerify) -> None:
        response = await async_client.verification_portals.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        verification_portal = await response.parse()
        assert_matches_type(AsyncCursorPagination[VerificationPortal], verification_portal, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncVerify) -> None:
        async with async_client.verification_portals.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            verification_portal = await response.parse()
            assert_matches_type(AsyncCursorPagination[VerificationPortal], verification_portal, path=["response"])

        assert cast(Any, response.is_closed) is True
