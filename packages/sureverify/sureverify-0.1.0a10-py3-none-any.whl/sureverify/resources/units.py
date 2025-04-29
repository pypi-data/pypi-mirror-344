# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import unit_list_params, unit_create_params, unit_update_params, unit_retrieve_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..pagination import SyncCursorPagination, AsyncCursorPagination
from ..types.unit import Unit
from .._base_client import AsyncPaginator, make_request_options
from ..types.unit_response import UnitResponse
from ..types.unit_request_data_param import UnitRequestDataParam

__all__ = ["UnitsResource", "AsyncUnitsResource"]


class UnitsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UnitsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return UnitsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UnitsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return UnitsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: UnitRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UnitResponse:
        """
        Create a Unit

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._post(
            "/api/v1/units",
            body=maybe_transform({"data": data}, unit_create_params.UnitCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UnitResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        fields_unit: List[
            Literal[
                "community", "unit_number", "address", "notes", "external_ref", "is_active", "created_at", "updated_at"
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["community", "address"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UnitResponse:
        """
        Retrieve a Unit

        Args:
          fields_unit: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          include: include query parameter to allow the client to customize which related resources
              should be returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._get(
            f"/api/v1/units/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_unit": fields_unit,
                        "include": include,
                    },
                    unit_retrieve_params.UnitRetrieveParams,
                ),
            ),
            cast_to=UnitResponse,
        )

    def update(
        self,
        id: str,
        *,
        data: unit_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UnitResponse:
        """
        Update a Unit

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._patch(
            f"/api/v1/units/{id}",
            body=maybe_transform({"data": data}, unit_update_params.UnitUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UnitResponse,
        )

    def list(
        self,
        *,
        fields_unit: List[
            Literal[
                "community", "unit_number", "address", "notes", "external_ref", "is_active", "created_at", "updated_at"
            ]
        ]
        | NotGiven = NOT_GIVEN,
        filter_community_property_manager_id: str | NotGiven = NOT_GIVEN,
        filter_community_id: str | NotGiven = NOT_GIVEN,
        include: List[Literal["community", "address"]] | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPagination[Unit]:
        """
        List Units

        Args:
          fields_unit: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          include: include query parameter to allow the client to customize which related resources
              should be returned.

          page_cursor: The pagination cursor value.

          page_size: Number of results to return per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._get_api_list(
            "/api/v1/units",
            page=SyncCursorPagination[Unit],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_unit": fields_unit,
                        "filter_community_property_manager_id": filter_community_property_manager_id,
                        "filter_community_id": filter_community_id,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    unit_list_params.UnitListParams,
                ),
            ),
            model=Unit,
        )


class AsyncUnitsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUnitsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUnitsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUnitsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return AsyncUnitsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: UnitRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UnitResponse:
        """
        Create a Unit

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._post(
            "/api/v1/units",
            body=await async_maybe_transform({"data": data}, unit_create_params.UnitCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UnitResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        fields_unit: List[
            Literal[
                "community", "unit_number", "address", "notes", "external_ref", "is_active", "created_at", "updated_at"
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["community", "address"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UnitResponse:
        """
        Retrieve a Unit

        Args:
          fields_unit: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          include: include query parameter to allow the client to customize which related resources
              should be returned.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._get(
            f"/api/v1/units/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "fields_unit": fields_unit,
                        "include": include,
                    },
                    unit_retrieve_params.UnitRetrieveParams,
                ),
            ),
            cast_to=UnitResponse,
        )

    async def update(
        self,
        id: str,
        *,
        data: unit_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UnitResponse:
        """
        Update a Unit

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._patch(
            f"/api/v1/units/{id}",
            body=await async_maybe_transform({"data": data}, unit_update_params.UnitUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UnitResponse,
        )

    def list(
        self,
        *,
        fields_unit: List[
            Literal[
                "community", "unit_number", "address", "notes", "external_ref", "is_active", "created_at", "updated_at"
            ]
        ]
        | NotGiven = NOT_GIVEN,
        filter_community_property_manager_id: str | NotGiven = NOT_GIVEN,
        filter_community_id: str | NotGiven = NOT_GIVEN,
        include: List[Literal["community", "address"]] | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[Unit, AsyncCursorPagination[Unit]]:
        """
        List Units

        Args:
          fields_unit: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          include: include query parameter to allow the client to customize which related resources
              should be returned.

          page_cursor: The pagination cursor value.

          page_size: Number of results to return per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._get_api_list(
            "/api/v1/units",
            page=AsyncCursorPagination[Unit],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_unit": fields_unit,
                        "filter_community_property_manager_id": filter_community_property_manager_id,
                        "filter_community_id": filter_community_id,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    unit_list_params.UnitListParams,
                ),
            ),
            model=Unit,
        )


class UnitsResourceWithRawResponse:
    def __init__(self, units: UnitsResource) -> None:
        self._units = units

        self.create = to_raw_response_wrapper(
            units.create,
        )
        self.retrieve = to_raw_response_wrapper(
            units.retrieve,
        )
        self.update = to_raw_response_wrapper(
            units.update,
        )
        self.list = to_raw_response_wrapper(
            units.list,
        )


class AsyncUnitsResourceWithRawResponse:
    def __init__(self, units: AsyncUnitsResource) -> None:
        self._units = units

        self.create = async_to_raw_response_wrapper(
            units.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            units.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            units.update,
        )
        self.list = async_to_raw_response_wrapper(
            units.list,
        )


class UnitsResourceWithStreamingResponse:
    def __init__(self, units: UnitsResource) -> None:
        self._units = units

        self.create = to_streamed_response_wrapper(
            units.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            units.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            units.update,
        )
        self.list = to_streamed_response_wrapper(
            units.list,
        )


class AsyncUnitsResourceWithStreamingResponse:
    def __init__(self, units: AsyncUnitsResource) -> None:
        self._units = units

        self.create = async_to_streamed_response_wrapper(
            units.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            units.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            units.update,
        )
        self.list = async_to_streamed_response_wrapper(
            units.list,
        )
