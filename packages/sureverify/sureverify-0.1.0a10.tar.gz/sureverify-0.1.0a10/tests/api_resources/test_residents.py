# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from sureverify import Verify, AsyncVerify
from tests.utils import assert_matches_type
from sureverify.types import (
    Resident,
    ResidentResponse,
)
from sureverify.pagination import SyncCursorPagination, AsyncCursorPagination

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestResidents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    def test_method_create(self, client: Verify) -> None:
        resident = client.residents.create(
            data={
                "attributes": {
                    "first_name": "x",
                    "last_name": "x",
                },
                "relationships": {
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "Resident",
            },
        )
        assert_matches_type(ResidentResponse, resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_create(self, client: Verify) -> None:
        response = client.residents.with_raw_response.create(
            data={
                "attributes": {
                    "first_name": "x",
                    "last_name": "x",
                },
                "relationships": {
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "Resident",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resident = response.parse()
        assert_matches_type(ResidentResponse, resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_create(self, client: Verify) -> None:
        with client.residents.with_streaming_response.create(
            data={
                "attributes": {
                    "first_name": "x",
                    "last_name": "x",
                },
                "relationships": {
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "Resident",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resident = response.parse()
            assert_matches_type(ResidentResponse, resident, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve(self, client: Verify) -> None:
        resident = client.residents.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ResidentResponse, resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_retrieve_with_all_params(self, client: Verify) -> None:
        resident = client.residents.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_resident=["community"],
            include=["community"],
        )
        assert_matches_type(ResidentResponse, resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_retrieve(self, client: Verify) -> None:
        response = client.residents.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resident = response.parse()
        assert_matches_type(ResidentResponse, resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_retrieve(self, client: Verify) -> None:
        with client.residents.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resident = response.parse()
            assert_matches_type(ResidentResponse, resident, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_retrieve(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.residents.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_update(self, client: Verify) -> None:
        resident = client.residents.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {
                    "first_name": "x",
                    "last_name": "x",
                },
                "relationships": {
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "Resident",
            },
        )
        assert_matches_type(ResidentResponse, resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_update(self, client: Verify) -> None:
        response = client.residents.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {
                    "first_name": "x",
                    "last_name": "x",
                },
                "relationships": {
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "Resident",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resident = response.parse()
        assert_matches_type(ResidentResponse, resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_update(self, client: Verify) -> None:
        with client.residents.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {
                    "first_name": "x",
                    "last_name": "x",
                },
                "relationships": {
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "Resident",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resident = response.parse()
            assert_matches_type(ResidentResponse, resident, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    def test_path_params_update(self, client: Verify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.residents.with_raw_response.update(
                id="",
                data={
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "attributes": {
                        "first_name": "x",
                        "last_name": "x",
                    },
                    "relationships": {
                        "community": {
                            "data": {
                                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                                "type": "Community",
                            }
                        },
                        "unit": {
                            "data": {
                                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                                "type": "Unit",
                            }
                        },
                    },
                    "type": "Resident",
                },
            )

    @pytest.mark.skip()
    @parametrize
    def test_method_list(self, client: Verify) -> None:
        resident = client.residents.list()
        assert_matches_type(SyncCursorPagination[Resident], resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_method_list_with_all_params(self, client: Verify) -> None:
        resident = client.residents.list(
            fields_resident=["community"],
            filter_community_property_manager_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            filter_community_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            filter_unit_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            include=["community"],
            page_cursor="page[cursor]",
            page_size=0,
        )
        assert_matches_type(SyncCursorPagination[Resident], resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_raw_response_list(self, client: Verify) -> None:
        response = client.residents.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resident = response.parse()
        assert_matches_type(SyncCursorPagination[Resident], resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    def test_streaming_response_list(self, client: Verify) -> None:
        with client.residents.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resident = response.parse()
            assert_matches_type(SyncCursorPagination[Resident], resident, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncResidents:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_create(self, async_client: AsyncVerify) -> None:
        resident = await async_client.residents.create(
            data={
                "attributes": {
                    "first_name": "x",
                    "last_name": "x",
                },
                "relationships": {
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "Resident",
            },
        )
        assert_matches_type(ResidentResponse, resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncVerify) -> None:
        response = await async_client.residents.with_raw_response.create(
            data={
                "attributes": {
                    "first_name": "x",
                    "last_name": "x",
                },
                "relationships": {
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "Resident",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resident = await response.parse()
        assert_matches_type(ResidentResponse, resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncVerify) -> None:
        async with async_client.residents.with_streaming_response.create(
            data={
                "attributes": {
                    "first_name": "x",
                    "last_name": "x",
                },
                "relationships": {
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "Resident",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resident = await response.parse()
            assert_matches_type(ResidentResponse, resident, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve(self, async_client: AsyncVerify) -> None:
        resident = await async_client.residents.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )
        assert_matches_type(ResidentResponse, resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncVerify) -> None:
        resident = await async_client.residents.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            fields_resident=["community"],
            include=["community"],
        )
        assert_matches_type(ResidentResponse, resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncVerify) -> None:
        response = await async_client.residents.with_raw_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resident = await response.parse()
        assert_matches_type(ResidentResponse, resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncVerify) -> None:
        async with async_client.residents.with_streaming_response.retrieve(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resident = await response.parse()
            assert_matches_type(ResidentResponse, resident, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.residents.with_raw_response.retrieve(
                id="",
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_update(self, async_client: AsyncVerify) -> None:
        resident = await async_client.residents.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {
                    "first_name": "x",
                    "last_name": "x",
                },
                "relationships": {
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "Resident",
            },
        )
        assert_matches_type(ResidentResponse, resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_update(self, async_client: AsyncVerify) -> None:
        response = await async_client.residents.with_raw_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {
                    "first_name": "x",
                    "last_name": "x",
                },
                "relationships": {
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "Resident",
            },
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resident = await response.parse()
        assert_matches_type(ResidentResponse, resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_update(self, async_client: AsyncVerify) -> None:
        async with async_client.residents.with_streaming_response.update(
            id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            data={
                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                "attributes": {
                    "first_name": "x",
                    "last_name": "x",
                },
                "relationships": {
                    "community": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Community",
                        }
                    },
                    "unit": {
                        "data": {
                            "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                            "type": "Unit",
                        }
                    },
                },
                "type": "Resident",
            },
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resident = await response.parse()
            assert_matches_type(ResidentResponse, resident, path=["response"])

        assert cast(Any, response.is_closed) is True

    @pytest.mark.skip()
    @parametrize
    async def test_path_params_update(self, async_client: AsyncVerify) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.residents.with_raw_response.update(
                id="",
                data={
                    "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                    "attributes": {
                        "first_name": "x",
                        "last_name": "x",
                    },
                    "relationships": {
                        "community": {
                            "data": {
                                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                                "type": "Community",
                            }
                        },
                        "unit": {
                            "data": {
                                "id": "182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
                                "type": "Unit",
                            }
                        },
                    },
                    "type": "Resident",
                },
            )

    @pytest.mark.skip()
    @parametrize
    async def test_method_list(self, async_client: AsyncVerify) -> None:
        resident = await async_client.residents.list()
        assert_matches_type(AsyncCursorPagination[Resident], resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncVerify) -> None:
        resident = await async_client.residents.list(
            fields_resident=["community"],
            filter_community_property_manager_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            filter_community_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            filter_unit_id="182bd5e5-6e1a-4fe4-a799-aa6d9a6ab26e",
            include=["community"],
            page_cursor="page[cursor]",
            page_size=0,
        )
        assert_matches_type(AsyncCursorPagination[Resident], resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_raw_response_list(self, async_client: AsyncVerify) -> None:
        response = await async_client.residents.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        resident = await response.parse()
        assert_matches_type(AsyncCursorPagination[Resident], resident, path=["response"])

    @pytest.mark.skip()
    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncVerify) -> None:
        async with async_client.residents.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            resident = await response.parse()
            assert_matches_type(AsyncCursorPagination[Resident], resident, path=["response"])

        assert cast(Any, response.is_closed) is True
