# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal

import httpx

from ..types import (
    verification_case_input_list_params,
    verification_case_input_create_params,
    verification_case_input_update_params,
    verification_case_input_retrieve_params,
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
from ..types.verification_case_input import VerificationCaseInput
from ..types.verification_case_input_response import VerificationCaseInputResponse
from ..types.verification_case_input_request_data_param import VerificationCaseInputRequestDataParam

__all__ = ["VerificationCaseInputsResource", "AsyncVerificationCaseInputsResource"]


class VerificationCaseInputsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VerificationCaseInputsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return VerificationCaseInputsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VerificationCaseInputsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return VerificationCaseInputsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: VerificationCaseInputRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationCaseInputResponse:
        """
        Create a Verification Case Input

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._post(
            "/api/v1/verification-case-inputs",
            body=maybe_transform(
                {"data": data}, verification_case_input_create_params.VerificationCaseInputCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationCaseInputResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        fields_verification_case_input: List[
            Literal[
                "case",
                "carrier",
                "policy_number",
                "effective_date",
                "expiration_date",
                "liability_coverage_amount",
                "address",
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["address", "case"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationCaseInputResponse:
        """
        Retrieve a Verification Case Input

        Args:
          fields_verification_case_input: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/verification-case-inputs/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_verification_case_input": fields_verification_case_input,
                        "include": include,
                    },
                    verification_case_input_retrieve_params.VerificationCaseInputRetrieveParams,
                ),
            ),
            cast_to=VerificationCaseInputResponse,
        )

    def update(
        self,
        id: str,
        *,
        data: verification_case_input_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationCaseInputResponse:
        """
        Update a Verification Case Input

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
            f"/api/v1/verification-case-inputs/{id}",
            body=maybe_transform(
                {"data": data}, verification_case_input_update_params.VerificationCaseInputUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationCaseInputResponse,
        )

    def list(
        self,
        *,
        fields_verification_case_input: List[
            Literal[
                "case",
                "carrier",
                "policy_number",
                "effective_date",
                "expiration_date",
                "liability_coverage_amount",
                "address",
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        filter_case_community_id: Optional[str] | NotGiven = NOT_GIVEN,
        filter_case_property_manager_id: str | NotGiven = NOT_GIVEN,
        filter_case_id: str | NotGiven = NOT_GIVEN,
        include: List[Literal["address", "case"]] | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPagination[VerificationCaseInput]:
        """
        List Verification Case Inputs

        Args:
          fields_verification_case_input: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          filter_case_community_id: The property or apartment complex where this verification case originated.

          filter_case_property_manager_id: The property management company handling this verification.

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
            "/api/v1/verification-case-inputs",
            page=SyncCursorPagination[VerificationCaseInput],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_verification_case_input": fields_verification_case_input,
                        "filter_case_community_id": filter_case_community_id,
                        "filter_case_property_manager_id": filter_case_property_manager_id,
                        "filter_case_id": filter_case_id,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    verification_case_input_list_params.VerificationCaseInputListParams,
                ),
            ),
            model=VerificationCaseInput,
        )


class AsyncVerificationCaseInputsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVerificationCaseInputsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncVerificationCaseInputsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVerificationCaseInputsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return AsyncVerificationCaseInputsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: VerificationCaseInputRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationCaseInputResponse:
        """
        Create a Verification Case Input

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._post(
            "/api/v1/verification-case-inputs",
            body=await async_maybe_transform(
                {"data": data}, verification_case_input_create_params.VerificationCaseInputCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationCaseInputResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        fields_verification_case_input: List[
            Literal[
                "case",
                "carrier",
                "policy_number",
                "effective_date",
                "expiration_date",
                "liability_coverage_amount",
                "address",
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["address", "case"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationCaseInputResponse:
        """
        Retrieve a Verification Case Input

        Args:
          fields_verification_case_input: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/verification-case-inputs/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "fields_verification_case_input": fields_verification_case_input,
                        "include": include,
                    },
                    verification_case_input_retrieve_params.VerificationCaseInputRetrieveParams,
                ),
            ),
            cast_to=VerificationCaseInputResponse,
        )

    async def update(
        self,
        id: str,
        *,
        data: verification_case_input_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationCaseInputResponse:
        """
        Update a Verification Case Input

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
            f"/api/v1/verification-case-inputs/{id}",
            body=await async_maybe_transform(
                {"data": data}, verification_case_input_update_params.VerificationCaseInputUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationCaseInputResponse,
        )

    def list(
        self,
        *,
        fields_verification_case_input: List[
            Literal[
                "case",
                "carrier",
                "policy_number",
                "effective_date",
                "expiration_date",
                "liability_coverage_amount",
                "address",
                "first_name",
                "last_name",
                "email",
                "phone_number",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        filter_case_community_id: Optional[str] | NotGiven = NOT_GIVEN,
        filter_case_property_manager_id: str | NotGiven = NOT_GIVEN,
        filter_case_id: str | NotGiven = NOT_GIVEN,
        include: List[Literal["address", "case"]] | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[VerificationCaseInput, AsyncCursorPagination[VerificationCaseInput]]:
        """
        List Verification Case Inputs

        Args:
          fields_verification_case_input: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          filter_case_community_id: The property or apartment complex where this verification case originated.

          filter_case_property_manager_id: The property management company handling this verification.

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
            "/api/v1/verification-case-inputs",
            page=AsyncCursorPagination[VerificationCaseInput],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_verification_case_input": fields_verification_case_input,
                        "filter_case_community_id": filter_case_community_id,
                        "filter_case_property_manager_id": filter_case_property_manager_id,
                        "filter_case_id": filter_case_id,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    verification_case_input_list_params.VerificationCaseInputListParams,
                ),
            ),
            model=VerificationCaseInput,
        )


class VerificationCaseInputsResourceWithRawResponse:
    def __init__(self, verification_case_inputs: VerificationCaseInputsResource) -> None:
        self._verification_case_inputs = verification_case_inputs

        self.create = to_raw_response_wrapper(
            verification_case_inputs.create,
        )
        self.retrieve = to_raw_response_wrapper(
            verification_case_inputs.retrieve,
        )
        self.update = to_raw_response_wrapper(
            verification_case_inputs.update,
        )
        self.list = to_raw_response_wrapper(
            verification_case_inputs.list,
        )


class AsyncVerificationCaseInputsResourceWithRawResponse:
    def __init__(self, verification_case_inputs: AsyncVerificationCaseInputsResource) -> None:
        self._verification_case_inputs = verification_case_inputs

        self.create = async_to_raw_response_wrapper(
            verification_case_inputs.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            verification_case_inputs.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            verification_case_inputs.update,
        )
        self.list = async_to_raw_response_wrapper(
            verification_case_inputs.list,
        )


class VerificationCaseInputsResourceWithStreamingResponse:
    def __init__(self, verification_case_inputs: VerificationCaseInputsResource) -> None:
        self._verification_case_inputs = verification_case_inputs

        self.create = to_streamed_response_wrapper(
            verification_case_inputs.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            verification_case_inputs.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            verification_case_inputs.update,
        )
        self.list = to_streamed_response_wrapper(
            verification_case_inputs.list,
        )


class AsyncVerificationCaseInputsResourceWithStreamingResponse:
    def __init__(self, verification_case_inputs: AsyncVerificationCaseInputsResource) -> None:
        self._verification_case_inputs = verification_case_inputs

        self.create = async_to_streamed_response_wrapper(
            verification_case_inputs.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            verification_case_inputs.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            verification_case_inputs.update,
        )
        self.list = async_to_streamed_response_wrapper(
            verification_case_inputs.list,
        )
