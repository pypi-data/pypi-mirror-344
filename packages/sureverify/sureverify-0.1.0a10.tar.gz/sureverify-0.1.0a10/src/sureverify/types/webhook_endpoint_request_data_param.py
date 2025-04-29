# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Literal, Required, TypedDict

from .webhook_header_request_param import WebhookHeaderRequestParam
from .webhook_event_type_request_param import WebhookEventTypeRequestParam

__all__ = [
    "WebhookEndpointRequestDataParam",
    "Attributes",
    "Relationships",
    "RelationshipsPropertyManagers",
    "RelationshipsPropertyManagersData",
]


class Attributes(TypedDict, total=False):
    name: Required[str]

    subscribed_events: Required[Iterable[WebhookEventTypeRequestParam]]

    url: Required[str]
    """URL to send webhook events to"""

    headers: Iterable[WebhookHeaderRequestParam]

    is_active: bool


class RelationshipsPropertyManagersData(TypedDict, total=False):
    id: Required[str]
    """The identifier of the related object."""

    type: Required[Literal["PropertyManager"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsPropertyManagers(TypedDict, total=False):
    data: Required[Iterable[RelationshipsPropertyManagersData]]


class Relationships(TypedDict, total=False):
    property_managers: RelationshipsPropertyManagers
    """A related resource object from type PropertyManager"""


class WebhookEndpointRequestDataParam(TypedDict, total=False):
    attributes: Required[Attributes]

    type: Required[Literal["WebhookEndpoint"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    relationships: Relationships
