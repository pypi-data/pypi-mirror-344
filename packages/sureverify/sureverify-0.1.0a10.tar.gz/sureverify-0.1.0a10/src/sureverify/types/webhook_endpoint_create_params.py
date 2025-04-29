# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .webhook_endpoint_request_data_param import WebhookEndpointRequestDataParam

__all__ = ["WebhookEndpointCreateParams"]


class WebhookEndpointCreateParams(TypedDict, total=False):
    data: Required[WebhookEndpointRequestDataParam]
