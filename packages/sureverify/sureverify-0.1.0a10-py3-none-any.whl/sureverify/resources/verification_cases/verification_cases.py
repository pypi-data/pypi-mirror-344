# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Optional
from typing_extensions import Literal

import httpx

from ...types import (
    verification_case_list_params,
    verification_case_create_params,
    verification_case_update_params,
    verification_case_retrieve_params,
)
from ..._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncCursorPagination, AsyncCursorPagination
from .update_status import (
    UpdateStatusResource,
    AsyncUpdateStatusResource,
    UpdateStatusResourceWithRawResponse,
    AsyncUpdateStatusResourceWithRawResponse,
    UpdateStatusResourceWithStreamingResponse,
    AsyncUpdateStatusResourceWithStreamingResponse,
)
from ..._base_client import AsyncPaginator, make_request_options
from ...types.verification_case import VerificationCase
from ...types.verification_case_response import VerificationCaseResponse
from ...types.verification_case_request_data_param import VerificationCaseRequestDataParam

__all__ = ["VerificationCasesResource", "AsyncVerificationCasesResource"]


class VerificationCasesResource(SyncAPIResource):
    @cached_property
    def update_status(self) -> UpdateStatusResource:
        return UpdateStatusResource(self._client)

    @cached_property
    def with_raw_response(self) -> VerificationCasesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return VerificationCasesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VerificationCasesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return VerificationCasesResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: VerificationCaseRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationCaseResponse:
        """
        Create a Verification Case

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._post(
            "/api/v1/verification-cases",
            body=maybe_transform({"data": data}, verification_case_create_params.VerificationCaseCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationCaseResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        fields_verification_case: List[
            Literal[
                "status",
                "source",
                "external_reference",
                "property_manager",
                "portal",
                "unit",
                "community",
                "resident",
                "policy",
                "attachments",
                "decision",
                "decision_reason",
                "submitted_at",
                "due_at",
                "receipt_reference",
                "notes",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["property_manager", "portal", "unit", "community", "resident", "policy", "attachments"]]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationCaseResponse:
        """
        Retrieve a Verification Case

        Args:
          fields_verification_case: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/verification-cases/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_verification_case": fields_verification_case,
                        "include": include,
                    },
                    verification_case_retrieve_params.VerificationCaseRetrieveParams,
                ),
            ),
            cast_to=VerificationCaseResponse,
        )

    def update(
        self,
        id: str,
        *,
        data: verification_case_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationCaseResponse:
        """
        Update a Verification Case

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
            f"/api/v1/verification-cases/{id}",
            body=maybe_transform({"data": data}, verification_case_update_params.VerificationCaseUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationCaseResponse,
        )

    def list(
        self,
        *,
        fields_verification_case: List[
            Literal[
                "status",
                "source",
                "external_reference",
                "property_manager",
                "portal",
                "unit",
                "community",
                "resident",
                "policy",
                "attachments",
                "decision",
                "decision_reason",
                "submitted_at",
                "due_at",
                "receipt_reference",
                "notes",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        filter_community_id: Optional[str] | NotGiven = NOT_GIVEN,
        filter_property_manager_id: str | NotGiven = NOT_GIVEN,
        filter_resident_id: Optional[str] | NotGiven = NOT_GIVEN,
        include: List[Literal["property_manager", "portal", "unit", "community", "resident", "policy", "attachments"]]
        | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPagination[VerificationCase]:
        """
        List Verification Cases

        Args:
          fields_verification_case: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          filter_community_id: The property or apartment complex where this verification case originated.

          filter_property_manager_id: The property management company handling this verification.

          filter_resident_id: The resident whose insurance is being verified.

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
            "/api/v1/verification-cases",
            page=SyncCursorPagination[VerificationCase],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_verification_case": fields_verification_case,
                        "filter_community_id": filter_community_id,
                        "filter_property_manager_id": filter_property_manager_id,
                        "filter_resident_id": filter_resident_id,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    verification_case_list_params.VerificationCaseListParams,
                ),
            ),
            model=VerificationCase,
        )

    def enqueue_processing(
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
        When a case is enqueued for processing, it will be processed in the background
        by VerifyAI. This process usually takes up to a few minutes to complete.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/api/v1/verification-cases/{id}/enqueue-processing",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def reset_checks(
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
        Reset results and checks

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/api/v1/verification-cases/{id}/reset-checks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    def send_reminder_email(
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
        """This will send a reminder email to the resident.

        Only send if the case is in the
        'new' status.This is to ensure that the resident is aware of the case and can
        complete it in a timely manner.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            f"/api/v1/verification-cases/{id}/send-reminder-email",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncVerificationCasesResource(AsyncAPIResource):
    @cached_property
    def update_status(self) -> AsyncUpdateStatusResource:
        return AsyncUpdateStatusResource(self._client)

    @cached_property
    def with_raw_response(self) -> AsyncVerificationCasesResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncVerificationCasesResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVerificationCasesResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return AsyncVerificationCasesResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: VerificationCaseRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationCaseResponse:
        """
        Create a Verification Case

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._post(
            "/api/v1/verification-cases",
            body=await async_maybe_transform(
                {"data": data}, verification_case_create_params.VerificationCaseCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationCaseResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        fields_verification_case: List[
            Literal[
                "status",
                "source",
                "external_reference",
                "property_manager",
                "portal",
                "unit",
                "community",
                "resident",
                "policy",
                "attachments",
                "decision",
                "decision_reason",
                "submitted_at",
                "due_at",
                "receipt_reference",
                "notes",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["property_manager", "portal", "unit", "community", "resident", "policy", "attachments"]]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationCaseResponse:
        """
        Retrieve a Verification Case

        Args:
          fields_verification_case: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/verification-cases/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "fields_verification_case": fields_verification_case,
                        "include": include,
                    },
                    verification_case_retrieve_params.VerificationCaseRetrieveParams,
                ),
            ),
            cast_to=VerificationCaseResponse,
        )

    async def update(
        self,
        id: str,
        *,
        data: verification_case_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationCaseResponse:
        """
        Update a Verification Case

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
            f"/api/v1/verification-cases/{id}",
            body=await async_maybe_transform(
                {"data": data}, verification_case_update_params.VerificationCaseUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationCaseResponse,
        )

    def list(
        self,
        *,
        fields_verification_case: List[
            Literal[
                "status",
                "source",
                "external_reference",
                "property_manager",
                "portal",
                "unit",
                "community",
                "resident",
                "policy",
                "attachments",
                "decision",
                "decision_reason",
                "submitted_at",
                "due_at",
                "receipt_reference",
                "notes",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        filter_community_id: Optional[str] | NotGiven = NOT_GIVEN,
        filter_property_manager_id: str | NotGiven = NOT_GIVEN,
        filter_resident_id: Optional[str] | NotGiven = NOT_GIVEN,
        include: List[Literal["property_manager", "portal", "unit", "community", "resident", "policy", "attachments"]]
        | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[VerificationCase, AsyncCursorPagination[VerificationCase]]:
        """
        List Verification Cases

        Args:
          fields_verification_case: endpoint return only specific fields in the response on a per-type basis by
              including a fields[TYPE] query parameter.

          filter_community_id: The property or apartment complex where this verification case originated.

          filter_property_manager_id: The property management company handling this verification.

          filter_resident_id: The resident whose insurance is being verified.

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
            "/api/v1/verification-cases",
            page=AsyncCursorPagination[VerificationCase],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_verification_case": fields_verification_case,
                        "filter_community_id": filter_community_id,
                        "filter_property_manager_id": filter_property_manager_id,
                        "filter_resident_id": filter_resident_id,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    verification_case_list_params.VerificationCaseListParams,
                ),
            ),
            model=VerificationCase,
        )

    async def enqueue_processing(
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
        When a case is enqueued for processing, it will be processed in the background
        by VerifyAI. This process usually takes up to a few minutes to complete.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/api/v1/verification-cases/{id}/enqueue-processing",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def reset_checks(
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
        Reset results and checks

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/api/v1/verification-cases/{id}/reset-checks",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )

    async def send_reminder_email(
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
        """This will send a reminder email to the resident.

        Only send if the case is in the
        'new' status.This is to ensure that the resident is aware of the case and can
        complete it in a timely manner.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            f"/api/v1/verification-cases/{id}/send-reminder-email",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class VerificationCasesResourceWithRawResponse:
    def __init__(self, verification_cases: VerificationCasesResource) -> None:
        self._verification_cases = verification_cases

        self.create = to_raw_response_wrapper(
            verification_cases.create,
        )
        self.retrieve = to_raw_response_wrapper(
            verification_cases.retrieve,
        )
        self.update = to_raw_response_wrapper(
            verification_cases.update,
        )
        self.list = to_raw_response_wrapper(
            verification_cases.list,
        )
        self.enqueue_processing = to_raw_response_wrapper(
            verification_cases.enqueue_processing,
        )
        self.reset_checks = to_raw_response_wrapper(
            verification_cases.reset_checks,
        )
        self.send_reminder_email = to_raw_response_wrapper(
            verification_cases.send_reminder_email,
        )

    @cached_property
    def update_status(self) -> UpdateStatusResourceWithRawResponse:
        return UpdateStatusResourceWithRawResponse(self._verification_cases.update_status)


class AsyncVerificationCasesResourceWithRawResponse:
    def __init__(self, verification_cases: AsyncVerificationCasesResource) -> None:
        self._verification_cases = verification_cases

        self.create = async_to_raw_response_wrapper(
            verification_cases.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            verification_cases.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            verification_cases.update,
        )
        self.list = async_to_raw_response_wrapper(
            verification_cases.list,
        )
        self.enqueue_processing = async_to_raw_response_wrapper(
            verification_cases.enqueue_processing,
        )
        self.reset_checks = async_to_raw_response_wrapper(
            verification_cases.reset_checks,
        )
        self.send_reminder_email = async_to_raw_response_wrapper(
            verification_cases.send_reminder_email,
        )

    @cached_property
    def update_status(self) -> AsyncUpdateStatusResourceWithRawResponse:
        return AsyncUpdateStatusResourceWithRawResponse(self._verification_cases.update_status)


class VerificationCasesResourceWithStreamingResponse:
    def __init__(self, verification_cases: VerificationCasesResource) -> None:
        self._verification_cases = verification_cases

        self.create = to_streamed_response_wrapper(
            verification_cases.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            verification_cases.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            verification_cases.update,
        )
        self.list = to_streamed_response_wrapper(
            verification_cases.list,
        )
        self.enqueue_processing = to_streamed_response_wrapper(
            verification_cases.enqueue_processing,
        )
        self.reset_checks = to_streamed_response_wrapper(
            verification_cases.reset_checks,
        )
        self.send_reminder_email = to_streamed_response_wrapper(
            verification_cases.send_reminder_email,
        )

    @cached_property
    def update_status(self) -> UpdateStatusResourceWithStreamingResponse:
        return UpdateStatusResourceWithStreamingResponse(self._verification_cases.update_status)


class AsyncVerificationCasesResourceWithStreamingResponse:
    def __init__(self, verification_cases: AsyncVerificationCasesResource) -> None:
        self._verification_cases = verification_cases

        self.create = async_to_streamed_response_wrapper(
            verification_cases.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            verification_cases.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            verification_cases.update,
        )
        self.list = async_to_streamed_response_wrapper(
            verification_cases.list,
        )
        self.enqueue_processing = async_to_streamed_response_wrapper(
            verification_cases.enqueue_processing,
        )
        self.reset_checks = async_to_streamed_response_wrapper(
            verification_cases.reset_checks,
        )
        self.send_reminder_email = async_to_streamed_response_wrapper(
            verification_cases.send_reminder_email,
        )

    @cached_property
    def update_status(self) -> AsyncUpdateStatusResourceWithStreamingResponse:
        return AsyncUpdateStatusResourceWithStreamingResponse(self._verification_cases.update_status)
