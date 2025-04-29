# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal

import httpx

from ..types import (
    property_manager_list_params,
    property_manager_create_params,
    property_manager_update_params,
    property_manager_retrieve_params,
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
from ..types.property_manager import PropertyManager
from ..types.property_manager_response import PropertyManagerResponse
from ..types.property_manager_request_data_param import PropertyManagerRequestDataParam

__all__ = ["PropertyManagersResource", "AsyncPropertyManagersResource"]


class PropertyManagersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PropertyManagersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return PropertyManagersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PropertyManagersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return PropertyManagersResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        data: PropertyManagerRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PropertyManagerResponse:
        """
        Create a Property Manager

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return self._post(
            "/api/v1/property-managers",
            body=maybe_transform({"data": data}, property_manager_create_params.PropertyManagerCreateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PropertyManagerResponse,
        )

    def retrieve(
        self,
        id: str,
        *,
        fields_property_manager: List[
            Literal[
                "name",
                "slug",
                "is_active",
                "notes",
                "interest_email_address",
                "interest_name",
                "interest_mailbox",
                "contact_name",
                "contact_email_address",
                "contact_address",
                "contact_phone_number",
                "admin_review_required",
                "admin_review_required_only_for_non_compliant",
                "allow_overriding",
                "force_admin_review_if_overridden",
                "allow_partial_name_and_unit_match",
                "allow_new_units",
                "allow_new_residents",
                "allow_new_policies_from_carriers",
                "allow_invalid_address",
                "force_coverage_term_to_overlap_with_lease",
                "force_extra_confirmation_on_verification_submission",
                "send_email_when_no_verification_started",
                "send_email_when_case_incomplete",
                "send_email_when_case_submitted",
                "send_email_when_case_compliant",
                "send_email_when_case_non_compliant",
                "send_email_when_compliance_is_expiring_soon",
                "send_email_when_becoming_non_compliant",
                "send_email_when_new_policy_is_added",
                "send_email_when_policy_updated",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["interest_mailbox", "contact_address"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PropertyManagerResponse:
        """
        Retrieve a Property Manager

        Args:
          fields_property_manager: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/property-managers/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_property_manager": fields_property_manager,
                        "include": include,
                    },
                    property_manager_retrieve_params.PropertyManagerRetrieveParams,
                ),
            ),
            cast_to=PropertyManagerResponse,
        )

    def update(
        self,
        id: str,
        *,
        data: property_manager_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PropertyManagerResponse:
        """
        Update a Property Manager

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
            f"/api/v1/property-managers/{id}",
            body=maybe_transform({"data": data}, property_manager_update_params.PropertyManagerUpdateParams),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PropertyManagerResponse,
        )

    def list(
        self,
        *,
        fields_property_manager: List[
            Literal[
                "name",
                "slug",
                "is_active",
                "notes",
                "interest_email_address",
                "interest_name",
                "interest_mailbox",
                "contact_name",
                "contact_email_address",
                "contact_address",
                "contact_phone_number",
                "admin_review_required",
                "admin_review_required_only_for_non_compliant",
                "allow_overriding",
                "force_admin_review_if_overridden",
                "allow_partial_name_and_unit_match",
                "allow_new_units",
                "allow_new_residents",
                "allow_new_policies_from_carriers",
                "allow_invalid_address",
                "force_coverage_term_to_overlap_with_lease",
                "force_extra_confirmation_on_verification_submission",
                "send_email_when_no_verification_started",
                "send_email_when_case_incomplete",
                "send_email_when_case_submitted",
                "send_email_when_case_compliant",
                "send_email_when_case_non_compliant",
                "send_email_when_compliance_is_expiring_soon",
                "send_email_when_becoming_non_compliant",
                "send_email_when_new_policy_is_added",
                "send_email_when_policy_updated",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["interest_mailbox", "contact_address"]] | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncCursorPagination[PropertyManager]:
        """
        List Property Managers

        Args:
          fields_property_manager: endpoint return only specific fields in the response on a per-type basis by
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
            "/api/v1/property-managers",
            page=SyncCursorPagination[PropertyManager],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_property_manager": fields_property_manager,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    property_manager_list_params.PropertyManagerListParams,
                ),
            ),
            model=PropertyManager,
        )


class AsyncPropertyManagersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPropertyManagersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/sureapp/verify-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPropertyManagersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPropertyManagersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/sureapp/verify-python#with_streaming_response
        """
        return AsyncPropertyManagersResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        data: PropertyManagerRequestDataParam,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PropertyManagerResponse:
        """
        Create a Property Manager

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "application/vnd.api+json", **(extra_headers or {})}
        return await self._post(
            "/api/v1/property-managers",
            body=await async_maybe_transform(
                {"data": data}, property_manager_create_params.PropertyManagerCreateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PropertyManagerResponse,
        )

    async def retrieve(
        self,
        id: str,
        *,
        fields_property_manager: List[
            Literal[
                "name",
                "slug",
                "is_active",
                "notes",
                "interest_email_address",
                "interest_name",
                "interest_mailbox",
                "contact_name",
                "contact_email_address",
                "contact_address",
                "contact_phone_number",
                "admin_review_required",
                "admin_review_required_only_for_non_compliant",
                "allow_overriding",
                "force_admin_review_if_overridden",
                "allow_partial_name_and_unit_match",
                "allow_new_units",
                "allow_new_residents",
                "allow_new_policies_from_carriers",
                "allow_invalid_address",
                "force_coverage_term_to_overlap_with_lease",
                "force_extra_confirmation_on_verification_submission",
                "send_email_when_no_verification_started",
                "send_email_when_case_incomplete",
                "send_email_when_case_submitted",
                "send_email_when_case_compliant",
                "send_email_when_case_non_compliant",
                "send_email_when_compliance_is_expiring_soon",
                "send_email_when_becoming_non_compliant",
                "send_email_when_new_policy_is_added",
                "send_email_when_policy_updated",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["interest_mailbox", "contact_address"]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PropertyManagerResponse:
        """
        Retrieve a Property Manager

        Args:
          fields_property_manager: endpoint return only specific fields in the response on a per-type basis by
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
            f"/api/v1/property-managers/{id}",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "fields_property_manager": fields_property_manager,
                        "include": include,
                    },
                    property_manager_retrieve_params.PropertyManagerRetrieveParams,
                ),
            ),
            cast_to=PropertyManagerResponse,
        )

    async def update(
        self,
        id: str,
        *,
        data: property_manager_update_params.Data,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> PropertyManagerResponse:
        """
        Update a Property Manager

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
            f"/api/v1/property-managers/{id}",
            body=await async_maybe_transform(
                {"data": data}, property_manager_update_params.PropertyManagerUpdateParams
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=PropertyManagerResponse,
        )

    def list(
        self,
        *,
        fields_property_manager: List[
            Literal[
                "name",
                "slug",
                "is_active",
                "notes",
                "interest_email_address",
                "interest_name",
                "interest_mailbox",
                "contact_name",
                "contact_email_address",
                "contact_address",
                "contact_phone_number",
                "admin_review_required",
                "admin_review_required_only_for_non_compliant",
                "allow_overriding",
                "force_admin_review_if_overridden",
                "allow_partial_name_and_unit_match",
                "allow_new_units",
                "allow_new_residents",
                "allow_new_policies_from_carriers",
                "allow_invalid_address",
                "force_coverage_term_to_overlap_with_lease",
                "force_extra_confirmation_on_verification_submission",
                "send_email_when_no_verification_started",
                "send_email_when_case_incomplete",
                "send_email_when_case_submitted",
                "send_email_when_case_compliant",
                "send_email_when_case_non_compliant",
                "send_email_when_compliance_is_expiring_soon",
                "send_email_when_becoming_non_compliant",
                "send_email_when_new_policy_is_added",
                "send_email_when_policy_updated",
                "created_at",
                "updated_at",
            ]
        ]
        | NotGiven = NOT_GIVEN,
        include: List[Literal["interest_mailbox", "contact_address"]] | NotGiven = NOT_GIVEN,
        page_cursor: str | NotGiven = NOT_GIVEN,
        page_size: int | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[PropertyManager, AsyncCursorPagination[PropertyManager]]:
        """
        List Property Managers

        Args:
          fields_property_manager: endpoint return only specific fields in the response on a per-type basis by
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
            "/api/v1/property-managers",
            page=AsyncCursorPagination[PropertyManager],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "fields_property_manager": fields_property_manager,
                        "include": include,
                        "page_cursor": page_cursor,
                        "page_size": page_size,
                    },
                    property_manager_list_params.PropertyManagerListParams,
                ),
            ),
            model=PropertyManager,
        )


class PropertyManagersResourceWithRawResponse:
    def __init__(self, property_managers: PropertyManagersResource) -> None:
        self._property_managers = property_managers

        self.create = to_raw_response_wrapper(
            property_managers.create,
        )
        self.retrieve = to_raw_response_wrapper(
            property_managers.retrieve,
        )
        self.update = to_raw_response_wrapper(
            property_managers.update,
        )
        self.list = to_raw_response_wrapper(
            property_managers.list,
        )


class AsyncPropertyManagersResourceWithRawResponse:
    def __init__(self, property_managers: AsyncPropertyManagersResource) -> None:
        self._property_managers = property_managers

        self.create = async_to_raw_response_wrapper(
            property_managers.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            property_managers.retrieve,
        )
        self.update = async_to_raw_response_wrapper(
            property_managers.update,
        )
        self.list = async_to_raw_response_wrapper(
            property_managers.list,
        )


class PropertyManagersResourceWithStreamingResponse:
    def __init__(self, property_managers: PropertyManagersResource) -> None:
        self._property_managers = property_managers

        self.create = to_streamed_response_wrapper(
            property_managers.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            property_managers.retrieve,
        )
        self.update = to_streamed_response_wrapper(
            property_managers.update,
        )
        self.list = to_streamed_response_wrapper(
            property_managers.list,
        )


class AsyncPropertyManagersResourceWithStreamingResponse:
    def __init__(self, property_managers: AsyncPropertyManagersResource) -> None:
        self._property_managers = property_managers

        self.create = async_to_streamed_response_wrapper(
            property_managers.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            property_managers.retrieve,
        )
        self.update = async_to_streamed_response_wrapper(
            property_managers.update,
        )
        self.list = async_to_streamed_response_wrapper(
            property_managers.list,
        )
