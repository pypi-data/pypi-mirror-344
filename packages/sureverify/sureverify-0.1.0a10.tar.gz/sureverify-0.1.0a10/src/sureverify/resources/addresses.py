# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import (
    address_list_params,
    address_create_params,
    address_update_params,
    address_retrieve_params,
)
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
from .._base_client import AsyncPaginator, make_request_options
from ..types.address import Address
from ..types.address_response import AddressResponse
from ..types.address_request_data_param import AddressRequestDataParam

__all__ = ["AddressesResource", "AsyncAddressesResource"]


class AddressesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AddressesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return AddressesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AddressesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return AddressesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: AddressRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AddressResponse:
        """
        Create an Address

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._post(
            "/api/v1/addresses",
            body=maybe_transform({"data": data}, address_create_params.AddressCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AddressResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        fields_address: List[Literal["line1", "line2", "city", "state_code", "postal", "created_at", "updated_at"]]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AddressResponse:
        """
        Retrieve an Address

        Args:
          fields_address: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._get(
            f"/api/v1/addresses/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"fields_address": fields_address}, address_retrieve_params.AddressRetrieveParams
                ),
            ),
            cast_to=AddressResponse,
        )

    def update(
        self,
        id: str,
        *,
        data: address_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AddressResponse:
        """
        Update an Address

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
            f"/api/v1/addresses/{id}",
            body=maybe_transform({"data": data}, address_update_params.AddressUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AddressResponse,
        )

    def list(
        self,
        *,
        fields_address: List[Literal["line1", "line2", "city", "state_code", "postal", "created_at", "updated_at"]]
        | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPagination[Address]:
        """
        List Addresses

        Args:
          fields_address: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          page_cursor: The pagination cursor value.

          page_size: Number of results to return per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._get_api_list(
            "/api/v1/addresses",
            page=SyncCursorPagination[Address],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_address": fields_address,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    address_list_params.AddressListParams,
                ),
            ),
            model=Address,
        )


class AsyncAddressesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncAddressesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncAddressesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncAddressesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return AsyncAddressesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: AddressRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AddressResponse:
        """
        Create an Address

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._post(
            "/api/v1/addresses",
            body=await async_maybe_transform({"data": data}, address_create_params.AddressCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AddressResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        fields_address: List[Literal["line1", "line2", "city", "state_code", "postal", "created_at", "updated_at"]]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AddressResponse:
        """
        Retrieve an Address

        Args:
          fields_address: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._get(
            f"/api/v1/addresses/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"fields_address": fields_address}, address_retrieve_params.AddressRetrieveParams
                ),
            ),
            cast_to=AddressResponse,
        )

    async def update(
        self,
        id: str,
        *,
        data: address_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AddressResponse:
        """
        Update an Address

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
            f"/api/v1/addresses/{id}",
            body=await async_maybe_transform({"data": data}, address_update_params.AddressUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=AddressResponse,
        )

    def list(
        self,
        *,
        fields_address: List[Literal["line1", "line2", "city", "state_code", "postal", "created_at", "updated_at"]]
        | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[Address, AsyncCursorPagination[Address]]:
        """
        List Addresses

        Args:
          fields_address: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          page_cursor: The pagination cursor value.

          page_size: Number of results to return per page.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._get_api_list(
            "/api/v1/addresses",
            page=AsyncCursorPagination[Address],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_address": fields_address,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    address_list_params.AddressListParams,
                ),
            ),
            model=Address,
        )


class AddressesResourceWithRawResponse:
    def __init__(self, addresses: AddressesResource) -> None:
        self._addresses = addresses

        self.create = to_raw_response_wrapper(
            addresses.create,
        )
        self.retrieve = to_raw_response_wrapper(
            addresses.retrieve,
        )
        self.update = to_raw_response_wrapper(
            addresses.update,
        )
        self.list = to_raw_response_wrapper(
            addresses.list,
        )


class AsyncAddressesResourceWithRawResponse:
    def __init__(self, addresses: AsyncAddressesResource) -> None:
        self._addresses = addresses

        self.create = async_to_raw_response_wrapper(
            addresses.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            addresses.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            addresses.update,
        )
        self.list = async_to_raw_response_wrapper(
            addresses.list,
        )


class AddressesResourceWithStreamingResponse:
    def __init__(self, addresses: AddressesResource) -> None:
        self._addresses = addresses

        self.create = to_streamed_response_wrapper(
            addresses.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            addresses.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            addresses.update,
        )
        self.list = to_streamed_response_wrapper(
            addresses.list,
        )


class AsyncAddressesResourceWithStreamingResponse:
    def __init__(self, addresses: AsyncAddressesResource) -> None:
        self._addresses = addresses

        self.create = async_to_streamed_response_wrapper(
            addresses.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            addresses.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            addresses.update,
        )
        self.list = async_to_streamed_response_wrapper(
            addresses.list,
        )
