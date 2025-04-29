# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import (
    community_list_params,
    community_create_params,
    community_update_params,
    community_retrieve_params,
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
from ..types.community import Community
from ..types.community_response import CommunityResponse
from ..types.community_request_data_param import CommunityRequestDataParam

__all__ = ["CommunitiesResource", "AsyncCommunitiesResource"]


class CommunitiesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CommunitiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return CommunitiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CommunitiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return CommunitiesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: CommunityRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommunityResponse:
        """
        Create a Community

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._post(
            "/api/v1/communities",
            body=maybe_transform({"data": data}, community_create_params.CommunityCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CommunityResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        fields_community: List[
            Literal[
                "property_manager",
                "name",
                "slug",
                "address",
                "is_active",
                "notes",
                "external_ref",
                "contact_name",
                "contact_email_address",
                "contact_phone_number",
                "contact_address",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["property_manager", "address", "contact_address"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommunityResponse:
        """
        Retrieve a Community

        Args:
          fields_community: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/communities/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_community": fields_community,
                        "include": include,
                    },
                    community_retrieve_params.CommunityRetrieveParams,
                ),
            ),
            cast_to=CommunityResponse,
        )

    def update(
        self,
        id: str,
        *,
        data: community_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommunityResponse:
        """
        Update a Community

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
            f"/api/v1/communities/{id}",
            body=maybe_transform({"data": data}, community_update_params.CommunityUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CommunityResponse,
        )

    def list(
        self,
        *,
        fields_community: List[
            Literal[
                "property_manager",
                "name",
                "slug",
                "address",
                "is_active",
                "notes",
                "external_ref",
                "contact_name",
                "contact_email_address",
                "contact_phone_number",
                "contact_address",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        filter_property_manager_id: str | NotGiven = NOT_GIVEN,
        include: List[Literal["property_manager", "address", "contact_address"]] | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPagination[Community]:
        """
        List Communities

        Args:
          fields_community: endpoint return only specific fields in the response on a per-type basis by
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
            "/api/v1/communities",
            page=SyncCursorPagination[Community],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_community": fields_community,
                        "filter_property_manager_id": filter_property_manager_id,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    community_list_params.CommunityListParams,
                ),
            ),
            model=Community,
        )


class AsyncCommunitiesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCommunitiesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCommunitiesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCommunitiesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return AsyncCommunitiesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: CommunityRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommunityResponse:
        """
        Create a Community

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._post(
            "/api/v1/communities",
            body=await async_maybe_transform({"data": data}, community_create_params.CommunityCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CommunityResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        fields_community: List[
            Literal[
                "property_manager",
                "name",
                "slug",
                "address",
                "is_active",
                "notes",
                "external_ref",
                "contact_name",
                "contact_email_address",
                "contact_phone_number",
                "contact_address",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["property_manager", "address", "contact_address"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommunityResponse:
        """
        Retrieve a Community

        Args:
          fields_community: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/communities/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "fields_community": fields_community,
                        "include": include,
                    },
                    community_retrieve_params.CommunityRetrieveParams,
                ),
            ),
            cast_to=CommunityResponse,
        )

    async def update(
        self,
        id: str,
        *,
        data: community_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> CommunityResponse:
        """
        Update a Community

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
            f"/api/v1/communities/{id}",
            body=await async_maybe_transform({"data": data}, community_update_params.CommunityUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CommunityResponse,
        )

    def list(
        self,
        *,
        fields_community: List[
            Literal[
                "property_manager",
                "name",
                "slug",
                "address",
                "is_active",
                "notes",
                "external_ref",
                "contact_name",
                "contact_email_address",
                "contact_phone_number",
                "contact_address",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        filter_property_manager_id: str | NotGiven = NOT_GIVEN,
        include: List[Literal["property_manager", "address", "contact_address"]] | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[Community, AsyncCursorPagination[Community]]:
        """
        List Communities

        Args:
          fields_community: endpoint return only specific fields in the response on a per-type basis by
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
            "/api/v1/communities",
            page=AsyncCursorPagination[Community],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_community": fields_community,
                        "filter_property_manager_id": filter_property_manager_id,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    community_list_params.CommunityListParams,
                ),
            ),
            model=Community,
        )


class CommunitiesResourceWithRawResponse:
    def __init__(self, communities: CommunitiesResource) -> None:
        self._communities = communities

        self.create = to_raw_response_wrapper(
            communities.create,
        )
        self.retrieve = to_raw_response_wrapper(
            communities.retrieve,
        )
        self.update = to_raw_response_wrapper(
            communities.update,
        )
        self.list = to_raw_response_wrapper(
            communities.list,
        )


class AsyncCommunitiesResourceWithRawResponse:
    def __init__(self, communities: AsyncCommunitiesResource) -> None:
        self._communities = communities

        self.create = async_to_raw_response_wrapper(
            communities.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            communities.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            communities.update,
        )
        self.list = async_to_raw_response_wrapper(
            communities.list,
        )


class CommunitiesResourceWithStreamingResponse:
    def __init__(self, communities: CommunitiesResource) -> None:
        self._communities = communities

        self.create = to_streamed_response_wrapper(
            communities.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            communities.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            communities.update,
        )
        self.list = to_streamed_response_wrapper(
            communities.list,
        )


class AsyncCommunitiesResourceWithStreamingResponse:
    def __init__(self, communities: AsyncCommunitiesResource) -> None:
        self._communities = communities

        self.create = async_to_streamed_response_wrapper(
            communities.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            communities.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            communities.update,
        )
        self.list = async_to_streamed_response_wrapper(
            communities.list,
        )
