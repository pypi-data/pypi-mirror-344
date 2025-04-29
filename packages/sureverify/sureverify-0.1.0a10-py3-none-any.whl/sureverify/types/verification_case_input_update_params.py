# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union, Optional
from datetime import date
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = [
    "VerificationCaseInputUpdateParams",
    "Data",
    "DataRelationships",
    "DataRelationshipsCase",
    "DataRelationshipsCaseData",
    "DataRelationshipsAddress",
    "DataRelationshipsAddressData",
    "DataAttributes",
]


class VerificationCaseInputUpdateParams(TypedDict, total=False):
    data: Required[Data]


class DataRelationshipsCaseData(TypedDict, total=False):
    id: Required[str]

    type: Required[Literal["VerificationCase"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """


class DataRelationshipsCase(TypedDict, total=False):
    data: Required[DataRelationshipsCaseData]


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
    case: Required[DataRelationshipsCase]
    """The identifier of the related object."""

    address: Optional[DataRelationshipsAddress]
    """The identifier of the related object."""


class DataAttributes(TypedDict, total=False):
    carrier: Optional[str]

    effective_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]

    email: Optional[str]
    """We may contact you for verification needs."""

    expiration_date: Annotated[Union[str, date, None], PropertyInfo(format="iso8601")]

    first_name: Optional[str]
    """First and last name as written on your policy."""

    last_name: Optional[str]

    liability_coverage_amount: Optional[str]

    phone_number: Optional[str]

    policy_number: Optional[str]


class Data(TypedDict, total=False):
    id: Required[str]

    relationships: Required[DataRelationships]

    type: Required[Literal["VerificationCaseInput"]]
    """
    The [type](https://jsonapi.org/format/#document-resource-object-identification)
    member is used to describe resource objects that share common attributes and
    relationships.
    """

    attributes: DataAttributes
