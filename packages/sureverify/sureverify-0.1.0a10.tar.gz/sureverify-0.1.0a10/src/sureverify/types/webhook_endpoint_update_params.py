# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .webhook_header_request_param import WebhookHeaderRequestParam
from .webhook_event_type_request_param import WebhookEventTypeRequestParam

__all__ = [
    "WebhookEndpointUpdateParams",
    "Data",
    "DataAttributes",
    "DataRelationships",
    "DataRelationshipsPropertyManagers",
    "DataRelationshipsPropertyManagersData",
]


class WebhookEndpointUpdateParams(TypedDict, total=False):
    data: Required[Data]


class DataAttributes(TypedDict, total=False):
    name: Required[str]

    subscribed_events: Required[Iterable[WebhookEventTypeRequestParam]]

    url: Required[str]
    """URL to send webhook events to"""

    headers: Iterable[WebhookHeaderRequestParam]

    is_active: bool


class DataRelationshipsPropertyManagersData(TypedDict, total=False):
    id: Required[str]
    """The identifier of the related object."""

    type: Required[Literal["PropertyManager"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsPropertyManagers(TypedDict, total=False):
    data: Required[Iterable[DataRelationshipsPropertyManagersData]]


class DataRelationships(TypedDict, total=False):
    property_managers: DataRelationshipsPropertyManagers
    """A related resource object from type PropertyManager"""


class Data(TypedDict, total=False):
    id: Required[str]

    attributes: Required[DataAttributes]

    type: Required[Literal["WebhookEndpoint"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    relationships: DataRelationships
