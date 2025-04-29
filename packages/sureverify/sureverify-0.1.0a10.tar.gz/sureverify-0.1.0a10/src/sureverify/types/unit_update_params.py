# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, TypedDict

__all__ = [
    "UnitUpdateParams",
    "Data",
    "DataAttributes",
    "DataRelationships",
    "DataRelationshipsCommunity",
    "DataRelationshipsCommunityData",
    "DataRelationshipsAddress",
    "DataRelationshipsAddressData",
]


class UnitUpdateParams(TypedDict, total=False):
    data: Required[Data]


class DataAttributes(TypedDict, total=False):
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


class DataRelationshipsCommunityData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Community"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsCommunity(TypedDict, total=False):
    data: Required[DataRelationshipsCommunityData]


class DataRelationshipsAddressData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Address"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsAddress(TypedDict, total=False):
    data: Required[DataRelationshipsAddressData]


class DataRelationships(TypedDict, total=False):
    community: Required[DataRelationshipsCommunity]
    """The identifier of the related object."""

    address: Optional[DataRelationshipsAddress]
    """The identifier of the related object."""


class Data(TypedDict, total=False):
    id: Required[str]

    attributes: Required[DataAttributes]

    relationships: Required[DataRelationships]

    type: Required[Literal["Unit"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """
