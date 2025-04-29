# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import date, datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "Resident",
    "Attributes",
    "Relationships",
    "RelationshipsCommunity",
    "RelationshipsCommunityData",
    "RelationshipsUnit",
    "RelationshipsUnitData",
    "RelationshipsCurrentPolicy",
    "RelationshipsCurrentPolicyData",
]


class Attributes(BaseModel):
    first_name: str
    """The resident's legal first name or given name."""

    last_name: str
    """The resident's legal last name or family name."""

    created_at: Optional[datetime] = None

    email: Optional[str] = None
    """
    Primary email address used for sending notifications and communications to the
    resident.
    """

    external_ref: Optional[str] = None
    """A custom identifier that you can assign to this record.

    This can be useful for tracking records across different platforms or databases
    that you use to manage your properties.
    """

    in_compliance_since: Optional[date] = None
    """The date when the resident's insurance coverage first met all requirements."""

    last_notified_at: Optional[datetime] = None
    """The most recent date and time when any notification was sent to this resident."""

    lease_end_date: Optional[date] = None
    """The date when the resident's lease agreement expires."""

    lease_start_date: Optional[date] = None
    """The date when the resident's lease agreement begins."""

    notes: Optional[str] = None
    """
    Optional field for adding any additional comments, or important details about
    this record.
    """

    out_of_compliance_since: Optional[date] = None
    """The date when the resident's insurance coverage stopped meeting requirements."""

    phone_number: Optional[str] = None
    """Primary contact number for reaching the resident."""

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


class RelationshipsUnitData(BaseModel):
    id: str

    type: Literal["Unit"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsUnit(BaseModel):
    data: Optional[RelationshipsUnitData] = None


class RelationshipsCurrentPolicyData(BaseModel):
    id: str

    type: Literal["Policy"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsCurrentPolicy(BaseModel):
    data: Optional[RelationshipsCurrentPolicyData] = None


class Relationships(BaseModel):
    community: RelationshipsCommunity
    """The identifier of the related object."""

    unit: RelationshipsUnit
    """The identifier of the related object."""

    current_policy: Optional[RelationshipsCurrentPolicy] = None
    """The identifier of the related object."""


class Resident(BaseModel):
    id: str

    attributes: Attributes

    relationships: Relationships

    type: Literal["Resident"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """
