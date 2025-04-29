# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "Unit",
    "Attributes",
    "Relationships",
    "RelationshipsCommunity",
    "RelationshipsCommunityData",
    "RelationshipsAddress",
    "RelationshipsAddressData",
]


class Attributes(BaseModel):
    unit_number: str

    created_at: Optional[datetime] = None

    external_ref: Optional[str] = None
    """A custom identifier that you can assign to this record.

    This can be useful for tracking records across different platforms or databases
    that you use to manage your properties.
    """

    is_active: Optional[bool] = None

    notes: Optional[str] = None
    """
    Optional field for adding any additional comments, or important details about
    this record.
    """

    updated_at: Optional[datetime] = None


class RelationshipsCommunityData(BaseModel):
    id: str

    type: Literal["Community"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsCommunity(BaseModel):
    data: Optional[RelationshipsCommunityData] = None


class RelationshipsAddressData(BaseModel):
    id: str

    type: Literal["Address"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsAddress(BaseModel):
    data: Optional[RelationshipsAddressData] = None


class Relationships(BaseModel):
    community: RelationshipsCommunity
    """The identifier of the related object."""

    address: Optional[RelationshipsAddress] = None
    """The identifier of the related object."""


class Unit(BaseModel):
    id: str

    attributes: Attributes

    relationships: Relationships

    type: Literal["Unit"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """
