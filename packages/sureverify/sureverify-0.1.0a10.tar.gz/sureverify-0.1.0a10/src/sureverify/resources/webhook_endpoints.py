# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import (
    webhook_endpoint_list_params,
    webhook_endpoint_create_params,
    webhook_endpoint_update_params,
    webhook_endpoint_retrieve_params,
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
from ..types.webhook_endpoint import WebhookEndpoint
from ..types.webhook_endpoint_response import WebhookEndpointResponse
from ..types.webhook_endpoint_request_data_param import WebhookEndpointRequestDataParam

__all__ = ["WebhookEndpointsResource", "AsyncWebhookEndpointsResource"]


class WebhookEndpointsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> WebhookEndpointsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return WebhookEndpointsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> WebhookEndpointsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return WebhookEndpointsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: WebhookEndpointRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookEndpointResponse:
        """
        Create a Webhook Endpoint

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._post(
            "/api/v1/webhook-endpoints",
            body=maybe_transform({"data": data}, webhook_endpoint_create_params.WebhookEndpointCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookEndpointResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        fields_webhook_endpoint: List[
            Literal[
                "name",
                "url",
                "is_active",
                "error_count",
                "property_managers",
                "headers",
                "subscribed_events",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookEndpointResponse:
        """
        Retrieve a Webhook Endpoint

        Args:
          fields_webhook_endpoint: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/webhook-endpoints/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"fields_webhook_endpoint": fields_webhook_endpoint},
                    webhook_endpoint_retrieve_params.WebhookEndpointRetrieveParams,
                ),
            ),
            cast_to=WebhookEndpointResponse,
        )

    def update(
        self,
        id: str,
        *,
        data: webhook_endpoint_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookEndpointResponse:
        """
        Update a Webhook Endpoint

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
            f"/api/v1/webhook-endpoints/{id}",
            body=maybe_transform({"data": data}, webhook_endpoint_update_params.WebhookEndpointUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookEndpointResponse,
        )

    def list(
        self,
        *,
        fields_webhook_endpoint: List[
            Literal[
                "name",
                "url",
                "is_active",
                "error_count",
                "property_managers",
                "headers",
                "subscribed_events",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPagination[WebhookEndpoint]:
        """
        List Webhook Endpoints

        Args:
          fields_webhook_endpoint: endpoint return only specific fields in the response on a per-type basis by
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
            "/api/v1/webhook-endpoints",
            page=SyncCursorPagination[WebhookEndpoint],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_webhook_endpoint": fields_webhook_endpoint,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    webhook_endpoint_list_params.WebhookEndpointListParams,
                ),
            ),
            model=WebhookEndpoint,
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
        Delete a Webhook Endpoint

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
            f"/api/v1/webhook-endpoints/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncWebhookEndpointsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncWebhookEndpointsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncWebhookEndpointsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncWebhookEndpointsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return AsyncWebhookEndpointsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: WebhookEndpointRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookEndpointResponse:
        """
        Create a Webhook Endpoint

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._post(
            "/api/v1/webhook-endpoints",
            body=await async_maybe_transform(
                {"data": data}, webhook_endpoint_create_params.WebhookEndpointCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookEndpointResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        fields_webhook_endpoint: List[
            Literal[
                "name",
                "url",
                "is_active",
                "error_count",
                "property_managers",
                "headers",
                "subscribed_events",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookEndpointResponse:
        """
        Retrieve a Webhook Endpoint

        Args:
          fields_webhook_endpoint: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/webhook-endpoints/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"fields_webhook_endpoint": fields_webhook_endpoint},
                    webhook_endpoint_retrieve_params.WebhookEndpointRetrieveParams,
                ),
            ),
            cast_to=WebhookEndpointResponse,
        )

    async def update(
        self,
        id: str,
        *,
        data: webhook_endpoint_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> WebhookEndpointResponse:
        """
        Update a Webhook Endpoint

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
            f"/api/v1/webhook-endpoints/{id}",
            body=await async_maybe_transform(
                {"data": data}, webhook_endpoint_update_params.WebhookEndpointUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=WebhookEndpointResponse,
        )

    def list(
        self,
        *,
        fields_webhook_endpoint: List[
            Literal[
                "name",
                "url",
                "is_active",
                "error_count",
                "property_managers",
                "headers",
                "subscribed_events",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[WebhookEndpoint, AsyncCursorPagination[WebhookEndpoint]]:
        """
        List Webhook Endpoints

        Args:
          fields_webhook_endpoint: endpoint return only specific fields in the response on a per-type basis by
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
            "/api/v1/webhook-endpoints",
            page=AsyncCursorPagination[WebhookEndpoint],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_webhook_endpoint": fields_webhook_endpoint,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    webhook_endpoint_list_params.WebhookEndpointListParams,
                ),
            ),
            model=WebhookEndpoint,
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
        Delete a Webhook Endpoint

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
            f"/api/v1/webhook-endpoints/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class WebhookEndpointsResourceWithRawResponse:
    def __init__(self, webhook_endpoints: WebhookEndpointsResource) -> None:
        self._webhook_endpoints = webhook_endpoints

        self.create = to_raw_response_wrapper(
            webhook_endpoints.create,
        )
        self.retrieve = to_raw_response_wrapper(
            webhook_endpoints.retrieve,
        )
        self.update = to_raw_response_wrapper(
            webhook_endpoints.update,
        )
        self.list = to_raw_response_wrapper(
            webhook_endpoints.list,
        )
        self.delete = to_raw_response_wrapper(
            webhook_endpoints.delete,
        )


class AsyncWebhookEndpointsResourceWithRawResponse:
    def __init__(self, webhook_endpoints: AsyncWebhookEndpointsResource) -> None:
        self._webhook_endpoints = webhook_endpoints

        self.create = async_to_raw_response_wrapper(
            webhook_endpoints.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            webhook_endpoints.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            webhook_endpoints.update,
        )
        self.list = async_to_raw_response_wrapper(
            webhook_endpoints.list,
        )
        self.delete = async_to_raw_response_wrapper(
            webhook_endpoints.delete,
        )


class WebhookEndpointsResourceWithStreamingResponse:
    def __init__(self, webhook_endpoints: WebhookEndpointsResource) -> None:
        self._webhook_endpoints = webhook_endpoints

        self.create = to_streamed_response_wrapper(
            webhook_endpoints.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            webhook_endpoints.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            webhook_endpoints.update,
        )
        self.list = to_streamed_response_wrapper(
            webhook_endpoints.list,
        )
        self.delete = to_streamed_response_wrapper(
            webhook_endpoints.delete,
        )


class AsyncWebhookEndpointsResourceWithStreamingResponse:
    def __init__(self, webhook_endpoints: AsyncWebhookEndpointsResource) -> None:
        self._webhook_endpoints = webhook_endpoints

        self.create = async_to_streamed_response_wrapper(
            webhook_endpoints.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            webhook_endpoints.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            webhook_endpoints.update,
        )
        self.list = async_to_streamed_response_wrapper(
            webhook_endpoints.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            webhook_endpoints.delete,
        )
