# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import (
    verification_portal_link_list_params,
    verification_portal_link_create_params,
    verification_portal_link_update_params,
    verification_portal_link_retrieve_params,
)
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
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
from ..types.verification_portal_link import VerificationPortalLink
from ..types.verification_portal_link_response import VerificationPortalLinkResponse
from ..types.verification_portal_link_request_data_param import VerificationPortalLinkRequestDataParam

__all__ = ["VerificationPortalLinksResource", "AsyncVerificationPortalLinksResource"]


class VerificationPortalLinksResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VerificationPortalLinksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return VerificationPortalLinksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VerificationPortalLinksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return VerificationPortalLinksResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: VerificationPortalLinkRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationPortalLinkResponse:
        """
        Create a Verification Portal Link

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._post(
            "/api/v1/verification-portal-links",
            body=maybe_transform(
                {"data": data}, verification_portal_link_create_params.VerificationPortalLinkCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationPortalLinkResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        fields_verification_portal_link: List[Literal["portal", "title", "url", "weight", "location"]]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationPortalLinkResponse:
        """
        Retrieve a Verification Portal Link

        Args:
          fields_verification_portal_link: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/verification-portal-links/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"fields_verification_portal_link": fields_verification_portal_link},
                    verification_portal_link_retrieve_params.VerificationPortalLinkRetrieveParams,
                ),
            ),
            cast_to=VerificationPortalLinkResponse,
        )

    def update(
        self,
        id: str,
        *,
        data: verification_portal_link_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationPortalLinkResponse:
        """
        Update a Verification Portal Link

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
            f"/api/v1/verification-portal-links/{id}",
            body=maybe_transform(
                {"data": data}, verification_portal_link_update_params.VerificationPortalLinkUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationPortalLinkResponse,
        )

    def list(
        self,
        *,
        fields_verification_portal_link: List[Literal["portal", "title", "url", "weight", "location"]]
        | NotGiven = NOT_GIVEN,
        filter_portal_property_manager_id: str | NotGiven = NOT_GIVEN,
        filter_portal_id: str | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPagination[VerificationPortalLink]:
        """
        List Verification Portal Links

        Args:
          fields_verification_portal_link: endpoint return only specific fields in the response on a per-type basis by
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
            "/api/v1/verification-portal-links",
            page=SyncCursorPagination[VerificationPortalLink],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_verification_portal_link": fields_verification_portal_link,
                        "filter_portal_property_manager_id": filter_portal_property_manager_id,
                        "filter_portal_id": filter_portal_id,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    verification_portal_link_list_params.VerificationPortalLinkListParams,
                ),
            ),
            model=VerificationPortalLink,
        )

    def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete a Verification Portal Link

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._delete(
            f"/api/v1/verification-portal-links/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncVerificationPortalLinksResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVerificationPortalLinksResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncVerificationPortalLinksResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVerificationPortalLinksResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return AsyncVerificationPortalLinksResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: VerificationPortalLinkRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationPortalLinkResponse:
        """
        Create a Verification Portal Link

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._post(
            "/api/v1/verification-portal-links",
            body=await async_maybe_transform(
                {"data": data}, verification_portal_link_create_params.VerificationPortalLinkCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationPortalLinkResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        fields_verification_portal_link: List[Literal["portal", "title", "url", "weight", "location"]]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationPortalLinkResponse:
        """
        Retrieve a Verification Portal Link

        Args:
          fields_verification_portal_link: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/verification-portal-links/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"fields_verification_portal_link": fields_verification_portal_link},
                    verification_portal_link_retrieve_params.VerificationPortalLinkRetrieveParams,
                ),
            ),
            cast_to=VerificationPortalLinkResponse,
        )

    async def update(
        self,
        id: str,
        *,
        data: verification_portal_link_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationPortalLinkResponse:
        """
        Update a Verification Portal Link

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
            f"/api/v1/verification-portal-links/{id}",
            body=await async_maybe_transform(
                {"data": data}, verification_portal_link_update_params.VerificationPortalLinkUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationPortalLinkResponse,
        )

    def list(
        self,
        *,
        fields_verification_portal_link: List[Literal["portal", "title", "url", "weight", "location"]]
        | NotGiven = NOT_GIVEN,
        filter_portal_property_manager_id: str | NotGiven = NOT_GIVEN,
        filter_portal_id: str | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[VerificationPortalLink, AsyncCursorPagination[VerificationPortalLink]]:
        """
        List Verification Portal Links

        Args:
          fields_verification_portal_link: endpoint return only specific fields in the response on a per-type basis by
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
            "/api/v1/verification-portal-links",
            page=AsyncCursorPagination[VerificationPortalLink],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_verification_portal_link": fields_verification_portal_link,
                        "filter_portal_property_manager_id": filter_portal_property_manager_id,
                        "filter_portal_id": filter_portal_id,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    verification_portal_link_list_params.VerificationPortalLinkListParams,
                ),
            ),
            model=VerificationPortalLink,
        )

    async def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Delete a Verification Portal Link

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._delete(
            f"/api/v1/verification-portal-links/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class VerificationPortalLinksResourceWithRawResponse:
    def __init__(self, verification_portal_links: VerificationPortalLinksResource) -> None:
        self._verification_portal_links = verification_portal_links

        self.create = to_raw_response_wrapper(
            verification_portal_links.create,
        )
        self.retrieve = to_raw_response_wrapper(
            verification_portal_links.retrieve,
        )
        self.update = to_raw_response_wrapper(
            verification_portal_links.update,
        )
        self.list = to_raw_response_wrapper(
            verification_portal_links.list,
        )
        self.delete = to_raw_response_wrapper(
            verification_portal_links.delete,
        )


class AsyncVerificationPortalLinksResourceWithRawResponse:
    def __init__(self, verification_portal_links: AsyncVerificationPortalLinksResource) -> None:
        self._verification_portal_links = verification_portal_links

        self.create = async_to_raw_response_wrapper(
            verification_portal_links.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            verification_portal_links.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            verification_portal_links.update,
        )
        self.list = async_to_raw_response_wrapper(
            verification_portal_links.list,
        )
        self.delete = async_to_raw_response_wrapper(
            verification_portal_links.delete,
        )


class VerificationPortalLinksResourceWithStreamingResponse:
    def __init__(self, verification_portal_links: VerificationPortalLinksResource) -> None:
        self._verification_portal_links = verification_portal_links

        self.create = to_streamed_response_wrapper(
            verification_portal_links.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            verification_portal_links.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            verification_portal_links.update,
        )
        self.list = to_streamed_response_wrapper(
            verification_portal_links.list,
        )
        self.delete = to_streamed_response_wrapper(
            verification_portal_links.delete,
        )


class AsyncVerificationPortalLinksResourceWithStreamingResponse:
    def __init__(self, verification_portal_links: AsyncVerificationPortalLinksResource) -> None:
        self._verification_portal_links = verification_portal_links

        self.create = async_to_streamed_response_wrapper(
            verification_portal_links.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            verification_portal_links.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            verification_portal_links.update,
        )
        self.list = async_to_streamed_response_wrapper(
            verification_portal_links.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            verification_portal_links.delete,
        )
