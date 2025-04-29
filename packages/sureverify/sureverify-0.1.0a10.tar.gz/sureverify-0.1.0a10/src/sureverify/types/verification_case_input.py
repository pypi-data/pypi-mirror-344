# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from datetime import date, datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "VerificationCaseInput",
    "Relationships",
    "RelationshipsCase",
    "RelationshipsCaseData",
    "RelationshipsAddress",
    "RelationshipsAddressData",
    "Attributes",
]


class RelationshipsCaseData(BaseModel):
    id: str

    type: Literal["VerificationCase"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsCase(BaseModel):
    data: Optional[RelationshipsCaseData] = None


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
    case: RelationshipsCase
    """The identifier of the related object."""

    address: Optional[RelationshipsAddress] = None
    """The identifier of the related object."""


class Attributes(BaseModel):
    carrier: Optional[str] = None

    created_at: Optional[datetime] = None

    effective_date: Optional[date] = None

    email: Optional[str] = None
    """We may contact you for verification needs."""

    expiration_date: Optional[date] = None

    first_name: Optional[str] = None
    """First and last name as written on your policy."""

    last_name: Optional[str] = None

    liability_coverage_amount: Optional[str] = None

    phone_number: Optional[str] = None

    policy_number: Optional[str] = None

    updated_at: Optional[datetime] = None


class VerificationCaseInput(BaseModel):
    id: str

    relationships: Relationships

    type: Literal["VerificationCaseInput"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    attributes: Optional[Attributes] = None
