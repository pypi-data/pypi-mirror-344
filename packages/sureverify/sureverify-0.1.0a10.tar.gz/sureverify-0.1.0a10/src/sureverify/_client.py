# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, Union, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    NOT_GIVEN,
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
)
from ._utils import is_given, get_async_library
from ._version import __version__
from .resources import (
    units,
    policies,
    addresses,
    residents,
    attachments,
    communities,
    property_managers,
    webhook_endpoints,
    verification_portals,
    verification_sessions,
    verification_case_inputs,
    verification_portal_links,
)
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import VerifyError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)
from .resources.verification_cases import verification_cases

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Verify", "AsyncVerify", "Client", "AsyncClient"]


class Verify(SyncAPIClient):
    addresses: addresses.AddressesResource
    communities: communities.CommunitiesResource
    policies: policies.PoliciesResource
    property_managers: property_managers.PropertyManagersResource
    residents: residents.ResidentsResource
    units: units.UnitsResource
    verification_case_inputs: verification_case_inputs.VerificationCaseInputsResource
    verification_cases: verification_cases.VerificationCasesResource
    verification_portal_links: verification_portal_links.VerificationPortalLinksResource
    verification_portals: verification_portals.VerificationPortalsResource
    verification_sessions: verification_sessions.VerificationSessionsResource
    webhook_endpoints: webhook_endpoints.WebhookEndpointsResource
    attachments: attachments.AttachmentsResource
    with_raw_response: VerifyWithRawResponse
    with_streaming_response: VerifyWithStreamedResponse

    # client options
    bearer_token: str

    def __init__(
        self,
        *,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Verify client instance.

        This automatically infers the `bearer_token` argument from the `VERIFY_BEARER_TOKEN` environment variable if it is not provided.
        """
        if bearer_token is None:
            bearer_token = os.environ.get("VERIFY_BEARER_TOKEN")
        if bearer_token is None:
            raise VerifyError(
                "The bearer_token client option must be set either by passing bearer_token to the client or by setting the VERIFY_BEARER_TOKEN environment variable"
            )
        self.bearer_token = bearer_token

        if base_url is None:
            base_url = os.environ.get("VERIFY_BASE_URL")
        if base_url is None:
            base_url = f"https://api.sureverify.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.addresses = addresses.AddressesResource(self)
        self.communities = communities.CommunitiesResource(self)
        self.policies = policies.PoliciesResource(self)
        self.property_managers = property_managers.PropertyManagersResource(self)
        self.residents = residents.ResidentsResource(self)
        self.units = units.UnitsResource(self)
        self.verification_case_inputs = verification_case_inputs.VerificationCaseInputsResource(self)
        self.verification_cases = verification_cases.VerificationCasesResource(self)
        self.verification_portal_links = verification_portal_links.VerificationPortalLinksResource(self)
        self.verification_portals = verification_portals.VerificationPortalsResource(self)
        self.verification_sessions = verification_sessions.VerificationSessionsResource(self)
        self.webhook_endpoints = webhook_endpoints.WebhookEndpointsResource(self)
        self.attachments = attachments.AttachmentsResource(self)
        self.with_raw_response = VerifyWithRawResponse(self)
        self.with_streaming_response = VerifyWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        return {"Authorization": f"Bearer {bearer_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            bearer_token=bearer_token or self.bearer_token,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncVerify(AsyncAPIClient):
    addresses: addresses.AsyncAddressesResource
    communities: communities.AsyncCommunitiesResource
    policies: policies.AsyncPoliciesResource
    property_managers: property_managers.AsyncPropertyManagersResource
    residents: residents.AsyncResidentsResource
    units: units.AsyncUnitsResource
    verification_case_inputs: verification_case_inputs.AsyncVerificationCaseInputsResource
    verification_cases: verification_cases.AsyncVerificationCasesResource
    verification_portal_links: verification_portal_links.AsyncVerificationPortalLinksResource
    verification_portals: verification_portals.AsyncVerificationPortalsResource
    verification_sessions: verification_sessions.AsyncVerificationSessionsResource
    webhook_endpoints: webhook_endpoints.AsyncWebhookEndpointsResource
    attachments: attachments.AsyncAttachmentsResource
    with_raw_response: AsyncVerifyWithRawResponse
    with_streaming_response: AsyncVerifyWithStreamedResponse

    # client options
    bearer_token: str

    def __init__(
        self,
        *,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: Union[float, Timeout, None, NotGiven] = NOT_GIVEN,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncVerify client instance.

        This automatically infers the `bearer_token` argument from the `VERIFY_BEARER_TOKEN` environment variable if it is not provided.
        """
        if bearer_token is None:
            bearer_token = os.environ.get("VERIFY_BEARER_TOKEN")
        if bearer_token is None:
            raise VerifyError(
                "The bearer_token client option must be set either by passing bearer_token to the client or by setting the VERIFY_BEARER_TOKEN environment variable"
            )
        self.bearer_token = bearer_token

        if base_url is None:
            base_url = os.environ.get("VERIFY_BASE_URL")
        if base_url is None:
            base_url = f"https://api.sureverify.com"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self.addresses = addresses.AsyncAddressesResource(self)
        self.communities = communities.AsyncCommunitiesResource(self)
        self.policies = policies.AsyncPoliciesResource(self)
        self.property_managers = property_managers.AsyncPropertyManagersResource(self)
        self.residents = residents.AsyncResidentsResource(self)
        self.units = units.AsyncUnitsResource(self)
        self.verification_case_inputs = verification_case_inputs.AsyncVerificationCaseInputsResource(self)
        self.verification_cases = verification_cases.AsyncVerificationCasesResource(self)
        self.verification_portal_links = verification_portal_links.AsyncVerificationPortalLinksResource(self)
        self.verification_portals = verification_portals.AsyncVerificationPortalsResource(self)
        self.verification_sessions = verification_sessions.AsyncVerificationSessionsResource(self)
        self.webhook_endpoints = webhook_endpoints.AsyncWebhookEndpointsResource(self)
        self.attachments = attachments.AsyncAttachmentsResource(self)
        self.with_raw_response = AsyncVerifyWithRawResponse(self)
        self.with_streaming_response = AsyncVerifyWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        return {"Authorization": f"Bearer {bearer_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = NOT_GIVEN,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = NOT_GIVEN,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            bearer_token=bearer_token or self.bearer_token,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class VerifyWithRawResponse:
    def __init__(self, client: Verify) -> None:
        self.addresses = addresses.AddressesResourceWithRawResponse(client.addresses)
        self.communities = communities.CommunitiesResourceWithRawResponse(client.communities)
        self.policies = policies.PoliciesResourceWithRawResponse(client.policies)
        self.property_managers = property_managers.PropertyManagersResourceWithRawResponse(client.property_managers)
        self.residents = residents.ResidentsResourceWithRawResponse(client.residents)
        self.units = units.UnitsResourceWithRawResponse(client.units)
        self.verification_case_inputs = verification_case_inputs.VerificationCaseInputsResourceWithRawResponse(
            client.verification_case_inputs
        )
        self.verification_cases = verification_cases.VerificationCasesResourceWithRawResponse(client.verification_cases)
        self.verification_portal_links = verification_portal_links.VerificationPortalLinksResourceWithRawResponse(
            client.verification_portal_links
        )
        self.verification_portals = verification_portals.VerificationPortalsResourceWithRawResponse(
            client.verification_portals
        )
        self.verification_sessions = verification_sessions.VerificationSessionsResourceWithRawResponse(
            client.verification_sessions
        )
        self.webhook_endpoints = webhook_endpoints.WebhookEndpointsResourceWithRawResponse(client.webhook_endpoints)
        self.attachments = attachments.AttachmentsResourceWithRawResponse(client.attachments)


class AsyncVerifyWithRawResponse:
    def __init__(self, client: AsyncVerify) -> None:
        self.addresses = addresses.AsyncAddressesResourceWithRawResponse(client.addresses)
        self.communities = communities.AsyncCommunitiesResourceWithRawResponse(client.communities)
        self.policies = policies.AsyncPoliciesResourceWithRawResponse(client.policies)
        self.property_managers = property_managers.AsyncPropertyManagersResourceWithRawResponse(
            client.property_managers
        )
        self.residents = residents.AsyncResidentsResourceWithRawResponse(client.residents)
        self.units = units.AsyncUnitsResourceWithRawResponse(client.units)
        self.verification_case_inputs = verification_case_inputs.AsyncVerificationCaseInputsResourceWithRawResponse(
            client.verification_case_inputs
        )
        self.verification_cases = verification_cases.AsyncVerificationCasesResourceWithRawResponse(
            client.verification_cases
        )
        self.verification_portal_links = verification_portal_links.AsyncVerificationPortalLinksResourceWithRawResponse(
            client.verification_portal_links
        )
        self.verification_portals = verification_portals.AsyncVerificationPortalsResourceWithRawResponse(
            client.verification_portals
        )
        self.verification_sessions = verification_sessions.AsyncVerificationSessionsResourceWithRawResponse(
            client.verification_sessions
        )
        self.webhook_endpoints = webhook_endpoints.AsyncWebhookEndpointsResourceWithRawResponse(
            client.webhook_endpoints
        )
        self.attachments = attachments.AsyncAttachmentsResourceWithRawResponse(client.attachments)


class VerifyWithStreamedResponse:
    def __init__(self, client: Verify) -> None:
        self.addresses = addresses.AddressesResourceWithStreamingResponse(client.addresses)
        self.communities = communities.CommunitiesResourceWithStreamingResponse(client.communities)
        self.policies = policies.PoliciesResourceWithStreamingResponse(client.policies)
        self.property_managers = property_managers.PropertyManagersResourceWithStreamingResponse(
            client.property_managers
        )
        self.residents = residents.ResidentsResourceWithStreamingResponse(client.residents)
        self.units = units.UnitsResourceWithStreamingResponse(client.units)
        self.verification_case_inputs = verification_case_inputs.VerificationCaseInputsResourceWithStreamingResponse(
            client.verification_case_inputs
        )
        self.verification_cases = verification_cases.VerificationCasesResourceWithStreamingResponse(
            client.verification_cases
        )
        self.verification_portal_links = verification_portal_links.VerificationPortalLinksResourceWithStreamingResponse(
            client.verification_portal_links
        )
        self.verification_portals = verification_portals.VerificationPortalsResourceWithStreamingResponse(
            client.verification_portals
        )
        self.verification_sessions = verification_sessions.VerificationSessionsResourceWithStreamingResponse(
            client.verification_sessions
        )
        self.webhook_endpoints = webhook_endpoints.WebhookEndpointsResourceWithStreamingResponse(
            client.webhook_endpoints
        )
        self.attachments = attachments.AttachmentsResourceWithStreamingResponse(client.attachments)


class AsyncVerifyWithStreamedResponse:
    def __init__(self, client: AsyncVerify) -> None:
        self.addresses = addresses.AsyncAddressesResourceWithStreamingResponse(client.addresses)
        self.communities = communities.AsyncCommunitiesResourceWithStreamingResponse(client.communities)
        self.policies = policies.AsyncPoliciesResourceWithStreamingResponse(client.policies)
        self.property_managers = property_managers.AsyncPropertyManagersResourceWithStreamingResponse(
            client.property_managers
        )
        self.residents = residents.AsyncResidentsResourceWithStreamingResponse(client.residents)
        self.units = units.AsyncUnitsResourceWithStreamingResponse(client.units)
        self.verification_case_inputs = (
            verification_case_inputs.AsyncVerificationCaseInputsResourceWithStreamingResponse(
                client.verification_case_inputs
            )
        )
        self.verification_cases = verification_cases.AsyncVerificationCasesResourceWithStreamingResponse(
            client.verification_cases
        )
        self.verification_portal_links = (
            verification_portal_links.AsyncVerificationPortalLinksResourceWithStreamingResponse(
                client.verification_portal_links
            )
        )
        self.verification_portals = verification_portals.AsyncVerificationPortalsResourceWithStreamingResponse(
            client.verification_portals
        )
        self.verification_sessions = verification_sessions.AsyncVerificationSessionsResourceWithStreamingResponse(
            client.verification_sessions
        )
        self.webhook_endpoints = webhook_endpoints.AsyncWebhookEndpointsResourceWithStreamingResponse(
            client.webhook_endpoints
        )
        self.attachments = attachments.AsyncAttachmentsResourceWithStreamingResponse(client.attachments)


Client = Verify

AsyncClient = AsyncVerify
