# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import (
    policy_list_params,
    policy_create_params,
    policy_update_params,
    policy_retrieve_params,
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
from ..types.policy import Policy
from ..types.policy_response import PolicyResponse
from ..types.policy_request_data_param import PolicyRequestDataParam

__all__ = ["PoliciesResource", "AsyncPoliciesResource"]


class PoliciesResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PoliciesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return PoliciesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PoliciesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return PoliciesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: PolicyRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PolicyResponse:
        """
        Create a Policy

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._post(
            "/api/v1/policies",
            body=maybe_transform({"data": data}, policy_create_params.PolicyCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PolicyResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        fields_policy: List[
            Literal[
                "external_reference",
                "policy_status",
                "carrier",
                "underwriter",
                "policy_number",
                "effective_date",
                "expiration_date",
                "deductible",
                "personal_property_limit",
                "liability_limit",
                "premium",
                "currency",
                "premium_for_fees",
                "primary_insured_name",
                "additional_insured_names",
                "lease_address",
                "interested_party_name",
                "interested_party_email",
                "interested_party_address",
                "resident",
                "is_sold_by_sure",
                "coverages",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["lease_address", "interested_party_address", "resident"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PolicyResponse:
        """
        Retrieve a Policy

        Args:
          fields_policy: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/policies/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_policy": fields_policy,
                        "include": include,
                    },
                    policy_retrieve_params.PolicyRetrieveParams,
                ),
            ),
            cast_to=PolicyResponse,
        )

    def update(
        self,
        id: str,
        *,
        data: policy_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PolicyResponse:
        """
        Update a Policy

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
            f"/api/v1/policies/{id}",
            body=maybe_transform({"data": data}, policy_update_params.PolicyUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PolicyResponse,
        )

    def list(
        self,
        *,
        fields_policy: List[
            Literal[
                "external_reference",
                "policy_status",
                "carrier",
                "underwriter",
                "policy_number",
                "effective_date",
                "expiration_date",
                "deductible",
                "personal_property_limit",
                "liability_limit",
                "premium",
                "currency",
                "premium_for_fees",
                "primary_insured_name",
                "additional_insured_names",
                "lease_address",
                "interested_party_name",
                "interested_party_email",
                "interested_party_address",
                "resident",
                "is_sold_by_sure",
                "coverages",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        filter_resident_community_property_manager_id: str | NotGiven = NOT_GIVEN,
        filter_resident_community_id: str | NotGiven = NOT_GIVEN,
        filter_resident_id: str | NotGiven = NOT_GIVEN,
        include: List[Literal["lease_address", "interested_party_address", "resident"]] | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPagination[Policy]:
        """
        List Policies

        Args:
          fields_policy: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          filter_resident_community_id: The property or apartment complex where the resident lives.

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
            "/api/v1/policies",
            page=SyncCursorPagination[Policy],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_policy": fields_policy,
                        "filter_resident_community_property_manager_id": filter_resident_community_property_manager_id,
                        "filter_resident_community_id": filter_resident_community_id,
                        "filter_resident_id": filter_resident_id,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    policy_list_params.PolicyListParams,
                ),
            ),
            model=Policy,
        )


class AsyncPoliciesResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPoliciesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPoliciesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPoliciesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return AsyncPoliciesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: PolicyRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PolicyResponse:
        """
        Create a Policy

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._post(
            "/api/v1/policies",
            body=await async_maybe_transform({"data": data}, policy_create_params.PolicyCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PolicyResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        fields_policy: List[
            Literal[
                "external_reference",
                "policy_status",
                "carrier",
                "underwriter",
                "policy_number",
                "effective_date",
                "expiration_date",
                "deductible",
                "personal_property_limit",
                "liability_limit",
                "premium",
                "currency",
                "premium_for_fees",
                "primary_insured_name",
                "additional_insured_names",
                "lease_address",
                "interested_party_name",
                "interested_party_email",
                "interested_party_address",
                "resident",
                "is_sold_by_sure",
                "coverages",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["lease_address", "interested_party_address", "resident"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PolicyResponse:
        """
        Retrieve a Policy

        Args:
          fields_policy: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/policies/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "fields_policy": fields_policy,
                        "include": include,
                    },
                    policy_retrieve_params.PolicyRetrieveParams,
                ),
            ),
            cast_to=PolicyResponse,
        )

    async def update(
        self,
        id: str,
        *,
        data: policy_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PolicyResponse:
        """
        Update a Policy

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
            f"/api/v1/policies/{id}",
            body=await async_maybe_transform({"data": data}, policy_update_params.PolicyUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PolicyResponse,
        )

    def list(
        self,
        *,
        fields_policy: List[
            Literal[
                "external_reference",
                "policy_status",
                "carrier",
                "underwriter",
                "policy_number",
                "effective_date",
                "expiration_date",
                "deductible",
                "personal_property_limit",
                "liability_limit",
                "premium",
                "currency",
                "premium_for_fees",
                "primary_insured_name",
                "additional_insured_names",
                "lease_address",
                "interested_party_name",
                "interested_party_email",
                "interested_party_address",
                "resident",
                "is_sold_by_sure",
                "coverages",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        filter_resident_community_property_manager_id: str | NotGiven = NOT_GIVEN,
        filter_resident_community_id: str | NotGiven = NOT_GIVEN,
        filter_resident_id: str | NotGiven = NOT_GIVEN,
        include: List[Literal["lease_address", "interested_party_address", "resident"]] | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[Policy, AsyncCursorPagination[Policy]]:
        """
        List Policies

        Args:
          fields_policy: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          filter_resident_community_id: The property or apartment complex where the resident lives.

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
            "/api/v1/policies",
            page=AsyncCursorPagination[Policy],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_policy": fields_policy,
                        "filter_resident_community_property_manager_id": filter_resident_community_property_manager_id,
                        "filter_resident_community_id": filter_resident_community_id,
                        "filter_resident_id": filter_resident_id,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    policy_list_params.PolicyListParams,
                ),
            ),
            model=Policy,
        )


class PoliciesResourceWithRawResponse:
    def __init__(self, policies: PoliciesResource) -> None:
        self._policies = policies

        self.create = to_raw_response_wrapper(
            policies.create,
        )
        self.retrieve = to_raw_response_wrapper(
            policies.retrieve,
        )
        self.update = to_raw_response_wrapper(
            policies.update,
        )
        self.list = to_raw_response_wrapper(
            policies.list,
        )


class AsyncPoliciesResourceWithRawResponse:
    def __init__(self, policies: AsyncPoliciesResource) -> None:
        self._policies = policies

        self.create = async_to_raw_response_wrapper(
            policies.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            policies.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            policies.update,
        )
        self.list = async_to_raw_response_wrapper(
            policies.list,
        )


class PoliciesResourceWithStreamingResponse:
    def __init__(self, policies: PoliciesResource) -> None:
        self._policies = policies

        self.create = to_streamed_response_wrapper(
            policies.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            policies.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            policies.update,
        )
        self.list = to_streamed_response_wrapper(
            policies.list,
        )


class AsyncPoliciesResourceWithStreamingResponse:
    def __init__(self, policies: AsyncPoliciesResource) -> None:
        self._policies = policies

        self.create = async_to_streamed_response_wrapper(
            policies.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            policies.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            policies.update,
        )
        self.list = async_to_streamed_response_wrapper(
            policies.list,
        )
