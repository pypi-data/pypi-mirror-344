# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List
from typing_extensions import Literal, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["WebhookEndpointRetrieveParams"]


class WebhookEndpointRetrieveParams(TypedDict, total=False):
    fields_webhook_endpoint: Annotated[
        List[
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
        ],
        PropertyInfo(alias="fields[WebhookEndpoint]"),
    ]
    """
    endpoint return only specific fields in the response on a per-type basis by
    including a fields[TYPE] query parameter.
    """
