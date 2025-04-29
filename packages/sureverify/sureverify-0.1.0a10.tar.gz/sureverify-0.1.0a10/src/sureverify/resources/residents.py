# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import (
    resident_list_params,
    resident_create_params,
    resident_update_params,
    resident_retrieve_params,
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
from ..types.resident import Resident
from ..types.resident_response import ResidentResponse
from ..types.resident_request_data_param import ResidentRequestDataParam

__all__ = ["ResidentsResource", "AsyncResidentsResource"]


class ResidentsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ResidentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return ResidentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ResidentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return ResidentsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: ResidentRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ResidentResponse:
        """
        Create a Resident

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._post(
            "/api/v1/residents",
            body=maybe_transform({"data": data}, resident_create_params.ResidentCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResidentResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        fields_resident: List[
            Literal[
                "community",
                "unit",
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "lease_start_date",
                "lease_end_date",
                "in_compliance_since",
                "out_of_compliance_since",
                "last_notified_at",
                "notes",
                "external_ref",
                "current_policy",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["community", "unit"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ResidentResponse:
        """
        Retrieve a Resident

        Args:
          fields_resident: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/residents/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_resident": fields_resident,
                        "include": include,
                    },
                    resident_retrieve_params.ResidentRetrieveParams,
                ),
            ),
            cast_to=ResidentResponse,
        )

    def update(
        self,
        id: str,
        *,
        data: resident_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ResidentResponse:
        """
        Update a Resident

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
            f"/api/v1/residents/{id}",
            body=maybe_transform({"data": data}, resident_update_params.ResidentUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResidentResponse,
        )

    def list(
        self,
        *,
        fields_resident: List[
            Literal[
                "community",
                "unit",
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "lease_start_date",
                "lease_end_date",
                "in_compliance_since",
                "out_of_compliance_since",
                "last_notified_at",
                "notes",
                "external_ref",
                "current_policy",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        filter_community_property_manager_id: str | NotGiven = NOT_GIVEN,
        filter_community_id: str | NotGiven = NOT_GIVEN,
        filter_unit_id: str | NotGiven = NOT_GIVEN,
        include: List[Literal["community", "unit"]] | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPagination[Resident]:
        """
        List Residents

        Args:
          fields_resident: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          filter_community_id: The property or apartment complex where the resident lives.

          filter_unit_id: The specific apartment or unit number assigned to this resident.

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
            "/api/v1/residents",
            page=SyncCursorPagination[Resident],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_resident": fields_resident,
                        "filter_community_property_manager_id": filter_community_property_manager_id,
                        "filter_community_id": filter_community_id,
                        "filter_unit_id": filter_unit_id,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    resident_list_params.ResidentListParams,
                ),
            ),
            model=Resident,
        )


class AsyncResidentsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncResidentsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncResidentsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncResidentsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return AsyncResidentsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: ResidentRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ResidentResponse:
        """
        Create a Resident

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._post(
            "/api/v1/residents",
            body=await async_maybe_transform({"data": data}, resident_create_params.ResidentCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResidentResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        fields_resident: List[
            Literal[
                "community",
                "unit",
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "lease_start_date",
                "lease_end_date",
                "in_compliance_since",
                "out_of_compliance_since",
                "last_notified_at",
                "notes",
                "external_ref",
                "current_policy",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["community", "unit"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ResidentResponse:
        """
        Retrieve a Resident

        Args:
          fields_resident: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/residents/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "fields_resident": fields_resident,
                        "include": include,
                    },
                    resident_retrieve_params.ResidentRetrieveParams,
                ),
            ),
            cast_to=ResidentResponse,
        )

    async def update(
        self,
        id: str,
        *,
        data: resident_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> ResidentResponse:
        """
        Update a Resident

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
            f"/api/v1/residents/{id}",
            body=await async_maybe_transform({"data": data}, resident_update_params.ResidentUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ResidentResponse,
        )

    def list(
        self,
        *,
        fields_resident: List[
            Literal[
                "community",
                "unit",
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "lease_start_date",
                "lease_end_date",
                "in_compliance_since",
                "out_of_compliance_since",
                "last_notified_at",
                "notes",
                "external_ref",
                "current_policy",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        filter_community_property_manager_id: str | NotGiven = NOT_GIVEN,
        filter_community_id: str | NotGiven = NOT_GIVEN,
        filter_unit_id: str | NotGiven = NOT_GIVEN,
        include: List[Literal["community", "unit"]] | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[Resident, AsyncCursorPagination[Resident]]:
        """
        List Residents

        Args:
          fields_resident: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          filter_community_id: The property or apartment complex where the resident lives.

          filter_unit_id: The specific apartment or unit number assigned to this resident.

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
            "/api/v1/residents",
            page=AsyncCursorPagination[Resident],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_resident": fields_resident,
                        "filter_community_property_manager_id": filter_community_property_manager_id,
                        "filter_community_id": filter_community_id,
                        "filter_unit_id": filter_unit_id,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    resident_list_params.ResidentListParams,
                ),
            ),
            model=Resident,
        )


class ResidentsResourceWithRawResponse:
    def __init__(self, residents: ResidentsResource) -> None:
        self._residents = residents

        self.create = to_raw_response_wrapper(
            residents.create,
        )
        self.retrieve = to_raw_response_wrapper(
            residents.retrieve,
        )
        self.update = to_raw_response_wrapper(
            residents.update,
        )
        self.list = to_raw_response_wrapper(
            residents.list,
        )


class AsyncResidentsResourceWithRawResponse:
    def __init__(self, residents: AsyncResidentsResource) -> None:
        self._residents = residents

        self.create = async_to_raw_response_wrapper(
            residents.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            residents.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            residents.update,
        )
        self.list = async_to_raw_response_wrapper(
            residents.list,
        )


class ResidentsResourceWithStreamingResponse:
    def __init__(self, residents: ResidentsResource) -> None:
        self._residents = residents

        self.create = to_streamed_response_wrapper(
            residents.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            residents.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            residents.update,
        )
        self.list = to_streamed_response_wrapper(
            residents.list,
        )


class AsyncResidentsResourceWithStreamingResponse:
    def __init__(self, residents: AsyncResidentsResource) -> None:
        self._residents = residents

        self.create = async_to_streamed_response_wrapper(
            residents.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            residents.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            residents.update,
        )
        self.list = async_to_streamed_response_wrapper(
            residents.list,
        )
