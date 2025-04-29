# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "UnitRequestDataParam",
    "Attributes",
    "Relationships",
    "RelationshipsCommunity",
    "RelationshipsCommunityData",
    "RelationshipsAddress",
    "RelationshipsAddressData",
]


class Attributes(TypedDict, total=False):
    unit_number: Required[str]

    external_ref: Optional[str]
    """A custom identifier that you can assign to this record.

    This can be useful for tracking records across different platforms or databases
    that you use to manage your properties.
    """

    is_active: bool

    notes: Optional[str]
    """
    Optional field for adding any additional comments, or important details about
    this record.
    """


class RelationshipsCommunityData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Community"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsCommunity(TypedDict, total=False):
    data: Required[RelationshipsCommunityData]


class RelationshipsAddressData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Address"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsAddress(TypedDict, total=False):
    data: Required[RelationshipsAddressData]


class Relationships(TypedDict, total=False):
    community: Required[RelationshipsCommunity]
    """The identifier of the related object."""

    address: Optional[RelationshipsAddress]
    """The identifier of the related object."""


class UnitRequestDataParam(TypedDict, total=False):
    attributes: Required[Attributes]

    relationships: Required[Relationships]

    type: Required[Literal["Unit"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """
