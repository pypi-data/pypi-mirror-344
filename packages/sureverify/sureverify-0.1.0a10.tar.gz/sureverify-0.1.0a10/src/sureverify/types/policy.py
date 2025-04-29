# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import date, datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "Policy",
    "Relationships",
    "RelationshipsResident",
    "RelationshipsResidentData",
    "RelationshipsInterestedPartyAddress",
    "RelationshipsInterestedPartyAddressData",
    "RelationshipsLeaseAddress",
    "RelationshipsLeaseAddressData",
    "Attributes",
    "AttributesCoverage",
    "AttributesCoverageAttributes",
]


class RelationshipsResidentData(BaseModel):
    id: str

    type: Literal["Resident"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsResident(BaseModel):
    data: Optional[RelationshipsResidentData] = None


class RelationshipsInterestedPartyAddressData(BaseModel):
    id: str

    type: Literal["Address"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsInterestedPartyAddress(BaseModel):
    data: Optional[RelationshipsInterestedPartyAddressData] = None


class RelationshipsLeaseAddressData(BaseModel):
    id: str

    type: Literal["Address"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class RelationshipsLeaseAddress(BaseModel):
    data: Optional[RelationshipsLeaseAddressData] = None


class Relationships(BaseModel):
    resident: RelationshipsResident
    """The identifier of the related object."""

    interested_party_address: Optional[RelationshipsInterestedPartyAddress] = None
    """The identifier of the related object."""

    lease_address: Optional[RelationshipsLeaseAddress] = None
    """The identifier of the related object."""


class AttributesCoverageAttributes(BaseModel):
    name: str

    included: Optional[bool] = None

    limit: Optional[float] = None

    notes: Optional[str] = None
    """
    Optional field for adding any additional comments, or important details about
    this record.
    """


class AttributesCoverage(BaseModel):
    id: object

    attributes: AttributesCoverageAttributes

    type: Literal["PolicyCoverage"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class Attributes(BaseModel):
    additional_insured_names: Optional[str] = None

    carrier: Optional[str] = None

    coverages: Optional[List[AttributesCoverage]] = None

    created_at: Optional[datetime] = None

    currency: Optional[str] = None

    deductible: Optional[str] = None

    effective_date: Optional[date] = None

    expiration_date: Optional[date] = None

    external_reference: Optional[str] = None

    interested_party_email: Optional[str] = None

    interested_party_name: Optional[str] = None

    is_sold_by_sure: Optional[bool] = None

    liability_limit: Optional[str] = None

    personal_property_limit: Optional[str] = None

    policy_number: Optional[str] = None

    policy_status: Optional[str] = None

    premium: Optional[str] = None

    premium_for_fees: Optional[str] = None

    primary_insured_name: Optional[str] = None

    underwriter: Optional[str] = None

    updated_at: Optional[datetime] = None


class Policy(BaseModel):
    id: str

    relationships: Relationships

    type: Literal["Policy"]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    attributes: Optional[Attributes] = None
