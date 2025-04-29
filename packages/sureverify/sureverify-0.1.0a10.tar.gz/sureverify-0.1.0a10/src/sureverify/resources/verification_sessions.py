# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import (
    verification_session_create_params,
    verification_session_retrieve_params,
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
from .._base_client import make_request_options
from ..types.verification_session_response import VerificationSessionResponse
from ..types.verification_session_request_data_param import VerificationSessionRequestDataParam

__all__ = ["VerificationSessionsResource", "AsyncVerificationSessionsResource"]


class VerificationSessionsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> VerificationSessionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return VerificationSessionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> VerificationSessionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return VerificationSessionsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: VerificationSessionRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationSessionResponse:
        """
        Create a Verification Session

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._post(
            "/api/v1/verification-sessions",
            body=maybe_transform({"data": data}, verification_session_create_params.VerificationSessionCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationSessionResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        fields_verification_session: List[
            Literal[
                "case",
                "expires_at",
                "created_at",
                "request",
                "hosted_url",
                "embedded_token",
                "property_manager",
                "community",
                "unit",
                "resident",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationSessionResponse:
        """
        Retrieve a Verification Session

        Args:
          fields_verification_session: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/verification-sessions/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"fields_verification_session": fields_verification_session},
                    verification_session_retrieve_params.VerificationSessionRetrieveParams,
                ),
            ),
            cast_to=VerificationSessionResponse,
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
        Delete a Verification Session

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
            f"/api/v1/verification-sessions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncVerificationSessionsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncVerificationSessionsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncVerificationSessionsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncVerificationSessionsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return AsyncVerificationSessionsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: VerificationSessionRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationSessionResponse:
        """
        Create a Verification Session

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._post(
            "/api/v1/verification-sessions",
            body=await async_maybe_transform(
                {"data": data}, verification_session_create_params.VerificationSessionCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=VerificationSessionResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        fields_verification_session: List[
            Literal[
                "case",
                "expires_at",
                "created_at",
                "request",
                "hosted_url",
                "embedded_token",
                "property_manager",
                "community",
                "unit",
                "resident",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> VerificationSessionResponse:
        """
        Retrieve a Verification Session

        Args:
          fields_verification_session: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/verification-sessions/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"fields_verification_session": fields_verification_session},
                    verification_session_retrieve_params.VerificationSessionRetrieveParams,
                ),
            ),
            cast_to=VerificationSessionResponse,
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
        Delete a Verification Session

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
            f"/api/v1/verification-sessions/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class VerificationSessionsResourceWithRawResponse:
    def __init__(self, verification_sessions: VerificationSessionsResource) -> None:
        self._verification_sessions = verification_sessions

        self.create = to_raw_response_wrapper(
            verification_sessions.create,
        )
        self.retrieve = to_raw_response_wrapper(
            verification_sessions.retrieve,
        )
        self.delete = to_raw_response_wrapper(
            verification_sessions.delete,
        )


class AsyncVerificationSessionsResourceWithRawResponse:
    def __init__(self, verification_sessions: AsyncVerificationSessionsResource) -> None:
        self._verification_sessions = verification_sessions

        self.create = async_to_raw_response_wrapper(
            verification_sessions.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            verification_sessions.retrieve,
        )
        self.delete = async_to_raw_response_wrapper(
            verification_sessions.delete,
        )


class VerificationSessionsResourceWithStreamingResponse:
    def __init__(self, verification_sessions: VerificationSessionsResource) -> None:
        self._verification_sessions = verification_sessions

        self.create = to_streamed_response_wrapper(
            verification_sessions.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            verification_sessions.retrieve,
        )
        self.delete = to_streamed_response_wrapper(
            verification_sessions.delete,
        )


class AsyncVerificationSessionsResourceWithStreamingResponse:
    def __init__(self, verification_sessions: AsyncVerificationSessionsResource) -> None:
        self._verification_sessions = verification_sessions

        self.create = async_to_streamed_response_wrapper(
            verification_sessions.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            verification_sessions.retrieve,
        )
        self.delete = async_to_streamed_response_wrapper(
            verification_sessions.delete,
        )
