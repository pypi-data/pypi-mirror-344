# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sureverify import Verify, AsyncVerify
from tests.utils import assert_matches_type
from sureverify.types import (
    Address,
    AddressResponse,
)
from sureverify.pagination import SyncCursorPagination, AsyncCursorPagination

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAddresses:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Verify) -> None:
        address = client.addresses.create(
            data={"type": "Address"},
        )
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create_with_all_params(self, client: Verify) -> None:
        address = client.addresses.create(
            data={
                "type": "Address",
                "attributes": {
                    "city": "city",
                    "line1": "x",
                    "line2": "line2",
                    "postal": "postal",
                    "state_code": "AL",
                },
            },
        )
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Verify) -> None:
        response = client.addresses.with_raw_response.create(
            data={"type": "Address"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        address = response.parse()
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Verify) -> None:
        with client.addresses.with_streaming_response.create(
            data={"type": "Address"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            address = response.parse()
            assert_matches_type(AddressResponse, address, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Verify) -> None:
        address = client.addresses.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Verify) -> None:
        address = client.addresses.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_address=["line1"],
        )
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Verify) -> None:
        response = client.addresses.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        address = response.parse()
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Verify) -> None:
        with client.addresses.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            address = response.parse()
            assert_matches_type(AddressResponse, address, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.addresses.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: Verify) -> None:
        address = client.addresses.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "type": "Address",
            },
        )
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_update_with_all_params(self, client: Verify) -> None:
        address = client.addresses.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "type": "Address",
                "attributes": {
                    "city": "city",
                    "line1": "x",
                    "line2": "line2",
                    "postal": "postal",
                    "state_code": "AL",
                },
            },
        )
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: Verify) -> None:
        response = client.addresses.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "type": "Address",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        address = response.parse()
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: Verify) -> None:
        with client.addresses.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "type": "Address",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            address = response.parse()
            assert_matches_type(AddressResponse, address, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.addresses.with_raw_response.update(
                id="",
                data={
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "type": "Address",
                },
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Verify) -> None:
        address = client.addresses.list()
        assert_matches_type(SyncCursorPagination[Address], address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Verify) -> None:
        address = client.addresses.list(
            fields_address=["line1"],
            page_cursor="page[cursor]",
            page_size=0,
        )
        assert_matches_type(SyncCursorPagination[Address], address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Verify) -> None:
        response = client.addresses.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        address = response.parse()
        assert_matches_type(SyncCursorPagination[Address], address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Verify) -> None:
        with client.addresses.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            address = response.parse()
            assert_matches_type(SyncCursorPagination[Address], address, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAddresses:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncVerify) -> None:
        address = await async_client.addresses.create(
            data={"type": "Address"},
        )
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncVerify) -> None:
        address = await async_client.addresses.create(
            data={
                "type": "Address",
                "attributes": {
                    "city": "city",
                    "line1": "x",
                    "line2": "line2",
                    "postal": "postal",
                    "state_code": "AL",
                },
            },
        )
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncVerify) -> None:
        response = await async_client.addresses.with_raw_response.create(
            data={"type": "Address"},
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        address = await response.parse()
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncVerify) -> None:
        async with async_client.addresses.with_streaming_response.create(
            data={"type": "Address"},
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            address = await response.parse()
            assert_matches_type(AddressResponse, address, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncVerify) -> None:
        address = await async_client.addresses.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncVerify) -> None:
        address = await async_client.addresses.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_address=["line1"],
        )
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncVerify) -> None:
        response = await async_client.addresses.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        address = await response.parse()
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncVerify) -> None:
        async with async_client.addresses.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            address = await response.parse()
            assert_matches_type(AddressResponse, address, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.addresses.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncVerify) -> None:
        address = await async_client.addresses.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "type": "Address",
            },
        )
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_update_with_all_params(self, async_client: AsyncVerify) -> None:
        address = await async_client.addresses.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "type": "Address",
                "attributes": {
                    "city": "city",
                    "line1": "x",
                    "line2": "line2",
                    "postal": "postal",
                    "state_code": "AL",
                },
            },
        )
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncVerify) -> None:
        response = await async_client.addresses.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "type": "Address",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        address = await response.parse()
        assert_matches_type(AddressResponse, address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncVerify) -> None:
        async with async_client.addresses.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "type": "Address",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            address = await response.parse()
            assert_matches_type(AddressResponse, address, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.addresses.with_raw_response.update(
                id="",
                data={
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "type": "Address",
                },
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncVerify) -> None:
        address = await async_client.addresses.list()
        assert_matches_type(AsyncCursorPagination[Address], address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncVerify) -> None:
        address = await async_client.addresses.list(
            fields_address=["line1"],
            page_cursor="page[cursor]",
            page_size=0,
        )
        assert_matches_type(AsyncCursorPagination[Address], address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncVerify) -> None:
        response = await async_client.addresses.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        address = await response.parse()
        assert_matches_type(AsyncCursorPagination[Address], address, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncVerify) -> None:
        async with async_client.addresses.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            address = await response.parse()
            assert_matches_type(AsyncCursorPagination[Address], address, path=["response"])

        assert cast(Any, response.is_closed) is True
