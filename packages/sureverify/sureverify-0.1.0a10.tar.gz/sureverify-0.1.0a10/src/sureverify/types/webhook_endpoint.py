# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "WebhookEndpoint",
    "Attributes",
    "AttributesSubscribedEvent",
    "AttributesHeader",
    "Relationships",
    "RelationshipsPropertyManagers",
    "RelationshipsPropertyManagersData",
]


class AttributesSubscribedEvent(BaseModel):
    key: Literal[
        "case.submitted",
        "case.compliant",
        "case.non_compliant",
        "resident.expiring_soon",
        "resident.becoming_non_compliant",
        "policy.new",
        "policy.updated",
    ]
    """
    - `case.submitted` - Portal Case Submitted
    - `case.compliant` - Portal Case Compliant
    - `case.non_compliant` - Portal Case Non-Compliant
    - `resident.expiring_soon` - Compliance Expiring Soon
    - `resident.becoming_non_compliant` - Becoming Non-Compliant
    - `policy.new` - New Policy Added
    - `policy.updated` - Policy Updated
    """


class AttributesHeader(BaseModel):
    key: str
    """Header name (e.g. 'Authorization')"""

    value: str
    """Header value (e.g. 'Bearer token123')"""


class Attributes(BaseModel):
    name: str

    subscribed_events: List[AttributesSubscribedEvent]

    url: str
    """URL to send webhook events to"""

    created_at: Optional[datetime] = None

    error_count: Optional[int] = None

    headers: Optional[List[AttributesHeader]] = None

    is_active: Optional[bool] = None

    updated_at: Optional[datetime] = None


class RelationshipsPropertyManagersData(BaseModel):
    id: str
    """The identifier of the related object."""

    type: Literal["PropertyManager"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsPropertyManagers(BaseModel):
    data: Optional[List[RelationshipsPropertyManagersData]] = None


class Relationships(BaseModel):
    property_managers: Optional[RelationshipsPropertyManagers] = None
    """A related resource object from type PropertyManager"""


class WebhookEndpoint(BaseModel):
    id: str

    attributes: Attributes

    type: Literal["WebhookEndpoint"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    relationships: Optional[Relationships] = None
