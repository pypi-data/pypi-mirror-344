# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import (
    verification_portal_list_params,
    verification_portal_create_params,
    verification_portal_update_params,
    verification_portal_retrieve_params,
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
from ..types.verification_portal import VerificationPortal
from ..types.verification_portal_response import VerificationPortalResponse
from ..types.verification_portal_request_data_param import VerificationPortalRequestDataParam

__all__ = ["VerificationPortalsResource", "AsyncVerificationPortalsResource"]


class VerificationPortalsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VerificationPortalsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return VerificationPortalsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VerificationPortalsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return VerificationPortalsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: VerificationPortalRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationPortalResponse:
        """
        Create a Verification Portal

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._post(
            "/api/v1/verification-portals",
            body=maybe_transform({"data": data}, verification_portal_create_params.VerificationPortalCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationPortalResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        fields_verification_portal: List[
            Literal[
                "property_manager",
                "title",
                "slug",
                "logo",
                "primary_color",
                "secondary_color",
                "muted_color",
                "show_purchase_flow",
                "only_docs_form",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["property_manager"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationPortalResponse:
        """
        Retrieve a Verification Portal

        Args:
          fields_verification_portal: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/verification-portals/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_verification_portal": fields_verification_portal,
                        "include": include,
                    },
                    verification_portal_retrieve_params.VerificationPortalRetrieveParams,
                ),
            ),
            cast_to=VerificationPortalResponse,
        )

    def update(
        self,
        id: str,
        *,
        data: verification_portal_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationPortalResponse:
        """
        Update a Verification Portal

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
            f"/api/v1/verification-portals/{id}",
            body=maybe_transform({"data": data}, verification_portal_update_params.VerificationPortalUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationPortalResponse,
        )

    def list(
        self,
        *,
        fields_verification_portal: List[
            Literal[
                "property_manager",
                "title",
                "slug",
                "logo",
                "primary_color",
                "secondary_color",
                "muted_color",
                "show_purchase_flow",
                "only_docs_form",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        filter_property_manager_id: str | NotGiven = NOT_GIVEN,
        include: List[Literal["property_manager"]] | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPagination[VerificationPortal]:
        """
        List Verification Portals

        Args:
          fields_verification_portal: endpoint return only specific fields in the response on a per-type basis by
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
            "/api/v1/verification-portals",
            page=SyncCursorPagination[VerificationPortal],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_verification_portal": fields_verification_portal,
                        "filter_property_manager_id": filter_property_manager_id,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    verification_portal_list_params.VerificationPortalListParams,
                ),
            ),
            model=VerificationPortal,
        )


class AsyncVerificationPortalsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVerificationPortalsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncVerificationPortalsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVerificationPortalsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return AsyncVerificationPortalsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: VerificationPortalRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationPortalResponse:
        """
        Create a Verification Portal

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._post(
            "/api/v1/verification-portals",
            body=await async_maybe_transform(
                {"data": data}, verification_portal_create_params.VerificationPortalCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationPortalResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        fields_verification_portal: List[
            Literal[
                "property_manager",
                "title",
                "slug",
                "logo",
                "primary_color",
                "secondary_color",
                "muted_color",
                "show_purchase_flow",
                "only_docs_form",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["property_manager"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationPortalResponse:
        """
        Retrieve a Verification Portal

        Args:
          fields_verification_portal: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/verification-portals/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "fields_verification_portal": fields_verification_portal,
                        "include": include,
                    },
                    verification_portal_retrieve_params.VerificationPortalRetrieveParams,
                ),
            ),
            cast_to=VerificationPortalResponse,
        )

    async def update(
        self,
        id: str,
        *,
        data: verification_portal_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationPortalResponse:
        """
        Update a Verification Portal

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
            f"/api/v1/verification-portals/{id}",
            body=await async_maybe_transform(
                {"data": data}, verification_portal_update_params.VerificationPortalUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationPortalResponse,
        )

    def list(
        self,
        *,
        fields_verification_portal: List[
            Literal[
                "property_manager",
                "title",
                "slug",
                "logo",
                "primary_color",
                "secondary_color",
                "muted_color",
                "show_purchase_flow",
                "only_docs_form",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        filter_property_manager_id: str | NotGiven = NOT_GIVEN,
        include: List[Literal["property_manager"]] | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[VerificationPortal, AsyncCursorPagination[VerificationPortal]]:
        """
        List Verification Portals

        Args:
          fields_verification_portal: endpoint return only specific fields in the response on a per-type basis by
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
            "/api/v1/verification-portals",
            page=AsyncCursorPagination[VerificationPortal],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_verification_portal": fields_verification_portal,
                        "filter_property_manager_id": filter_property_manager_id,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    verification_portal_list_params.VerificationPortalListParams,
                ),
            ),
            model=VerificationPortal,
        )


class VerificationPortalsResourceWithRawResponse:
    def __init__(self, verification_portals: VerificationPortalsResource) -> None:
        self._verification_portals = verification_portals

        self.create = to_raw_response_wrapper(
            verification_portals.create,
        )
        self.retrieve = to_raw_response_wrapper(
            verification_portals.retrieve,
        )
        self.update = to_raw_response_wrapper(
            verification_portals.update,
        )
        self.list = to_raw_response_wrapper(
            verification_portals.list,
        )


class AsyncVerificationPortalsResourceWithRawResponse:
    def __init__(self, verification_portals: AsyncVerificationPortalsResource) -> None:
        self._verification_portals = verification_portals

        self.create = async_to_raw_response_wrapper(
            verification_portals.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            verification_portals.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            verification_portals.update,
        )
        self.list = async_to_raw_response_wrapper(
            verification_portals.list,
        )


class VerificationPortalsResourceWithStreamingResponse:
    def __init__(self, verification_portals: VerificationPortalsResource) -> None:
        self._verification_portals = verification_portals

        self.create = to_streamed_response_wrapper(
            verification_portals.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            verification_portals.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            verification_portals.update,
        )
        self.list = to_streamed_response_wrapper(
            verification_portals.list,
        )


class AsyncVerificationPortalsResourceWithStreamingResponse:
    def __init__(self, verification_portals: AsyncVerificationPortalsResource) -> None:
        self._verification_portals = verification_portals

        self.create = async_to_streamed_response_wrapper(
            verification_portals.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            verification_portals.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            verification_portals.update,
        )
        self.list = async_to_streamed_response_wrapper(
            verification_portals.list,
        )
