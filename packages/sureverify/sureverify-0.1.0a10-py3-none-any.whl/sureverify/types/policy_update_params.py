# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Iterable, Optional
from datetime import date
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo
from .policy_coverage_request_param import PolicyCoverageRequestParam

__all__ = [
    "PolicyUpdateParams",
    "Data",
    "DataRelationships",
    "DataRelationshipsResident",
    "DataRelationshipsResidentData",
    "DataRelationshipsInterestedPartyAddress",
    "DataRelationshipsInterestedPartyAddressData",
    "DataRelationshipsLeaseAddress",
    "DataRelationshipsLeaseAddressData",
    "DataAttributes",
]


class PolicyUpdateParams(TypedDict, total=False):
    data: Required[Data]


class DataRelationshipsResidentData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Resident"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsResident(TypedDict, total=False):
    data: Required[DataRelationshipsResidentData]


class DataRelationshipsInterestedPartyAddressData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Address"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsInterestedPartyAddress(TypedDict, total=False):
    data: Required[DataRelationshipsInterestedPartyAddressData]


class DataRelationshipsLeaseAddressData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["Address"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsLeaseAddress(TypedDict, total=False):
    data: Required[DataRelationshipsLeaseAddressData]


class DataRelationships(TypedDict, total=False):
    resident: Required[DataRelationshipsResident]
    """The identifier of the related object."""

    interested_party_address: Optional[DataRelationshipsInterestedPartyAddress]
    """The identifier of the related object."""

    lease_address: Optional[DataRelationshipsLeaseAddress]
    """The identifier of the related object."""


class DataAttributes(TypedDict, total=False):
    additional_insured_names: Optional[str]

    carrier: Optional[str]

    coverages: Iterable[PolicyCoverageRequestParam]

    currency: Optional[str]

    deductible: Optional[str]

    effective_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]

    expiration_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]

    external_reference: Optional[str]

    interested_party_email: Optional[str]

    interested_party_name: Optional[str]

    is_sold_by_sure: bool

    liability_limit: Optional[str]

    personal_property_limit: Optional[str]

    policy_number: Optional[str]

    policy_status: Optional[str]

    premium: Optional[str]

    premium_for_fees: Optional[str]

    primary_insured_name: Optional[str]

    underwriter: Optional[str]


class Data(TypedDict, total=False):
    id: Required[str]

    relationships: Required[DataRelationships]

    type: Required[Literal["Policy"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    attributes: DataAttributes
